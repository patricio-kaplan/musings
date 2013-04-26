from myhdl import *
import getopt
import sys
import random
import verilated_wrap
import reader_freq

try:   opts,args=getopt.getopt(sys.argv[1:], 'ds:', ['read_freq='])
except getopt.GetoptError as err:
	print err
	print "usage: ", sys.argv[0], ' [-d] [-s seed] '
	sys.exit(2)

dump=0
seed=0x1234
for i,a in opts: 
	if i=='-d': 
		print " note: dump is on"
	 	dump=1	
 	elif i=='-s':
	 	seed=int(a)
		print " note: seed is ", seed
 	elif i=='--read_freq':
		read_freq_type=a
		print "read_freq_type=",read_freq_type



if dump: 
	import verilated_vcd_c_wrap
	import fifo_wrap_dump
else: 
	print " note: dump is off"
	import fifo_wrap

exp_fifo=[] # empty list
total_flits=100
flits_to_inject=Signal(total_flits)
flits_read=Signal(0)

def driver(clk,dut,flits_to_inject):
	# grab our own RNG
	myr = random.Random()
	myr.seed(seed)

	wrdl = range(0,dut.wr_data_len())

	@instance
	def write():
		print "initializing"
		dut.wr=0
		dut.rd=0
		dut.rst=1
		for i in range(4): yield clk.posedge
		dut.rst=0
		print "done initializing"
		data=0
		rdg = eval("reader_freq."+read_freq_type+"()")

		while True:
			yield clk.posedge
			if dut.full or not flits_to_inject:
				dut.wr=0
			else:
				dut.wr=1
				flit = [ myr.getrandbits(32) for i in wrdl ]
				for i in wrdl: dut.wr_data_set(i,flit[i])
				exp_fifo.append(flit)
				flits_to_inject.next=flits_to_inject-1
			if dut.empty:
				dut.rd=0
			else:
				dut.rd=rdg.next()

	return write

def checker(clk,dut,flits_read):
	# grab our own RNG
	myr = random.Random()
	myr.seed(seed)
	rddl = range(0,dut.rd_data_len())

	@always(clk.negedge)
	def read():
		print now(), "reading"
		if not dut.rst and dut.rd:
			flits_read.next=flits_read+1
			if flits_read>total_flits: print now(), " ERROR: read ", flits_read, " which is more than the ", total_flits, " expected"
			got = [ dut.rd_data_get(i) for i in rddl ]
			exp = exp_fifo.pop(0)
			if exp==got: print now(), " read data matched"
			else: print "ERROR: mistmatch: exp=",exp, " got=",got

	return read

def testbench():
	clk = Signal(intbv(0))

	if dump:
		verilated_wrap.traceEverOn(True)
		tracer = verilated_vcd_c_wrap.VerilatedVcdC()

	if dump: dut = fifo_wrap_dump.Vfifo("hello")
	else:    dut = fifo_wrap.Vfifo("hello")

	if dump:
		dut.trace(tracer,99,100)
		tracer.open('dump.vcd')

	dut.rst=1
	dut.clk=0

	@always(delay(10))
	def clkGen(): 
		if dump: tracer.dump(now())
		clk.next = not clk;

	@always(clk.posedge, clk.negedge)
	def dut_wrap():
		dut.clk=int(clk)
		dut.eval()

	@instance
	def stimulus():
		while flits_to_inject: yield clk.negedge
		timeout_count=100
		while flits_read<total_flits and timeout_count: 
			yield clk.negedge
			timeout_count-=1
		if not timeout_count: print "ERROR: timed out waiting for fifo to drain"
		if len(exp_fifo)>0: print "ERROR: exp fifo not empty"
		if dump: tracer.close()
		raise StopSimulation

	return clkGen, stimulus, dut_wrap, driver(clk,dut,flits_to_inject), checker(clk,dut,flits_read)


tb=testbench()	


Simulation(tb).run()
