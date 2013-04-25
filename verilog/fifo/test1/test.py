from myhdl import *
import getopt
import sys

try:
	opts,args=getopt.getopt(sys.argv[1:], 'd')
except getopt.GetoptError as err:
	print err
	print "usage: ", sys.argv[0], ' [-d] '
	sys.exit(2)

dump=0
for i,a in opts: 
	if i=='-d': 
		print " note: dump is on"
	 	dump=1

import verilated_wrap

if dump: 
	import verilated_vcd_c_wrap
	import fifo_wrap_dump
else: 
	print " note: dump is off"
	import fifo_wrap



def driver(clk,dut):
	@instance
	def body():
		print "initializing"
		dut.wr=0
		dut.rd=0
		dut.rst=1
		for i in range(4): yield clk.negedge
		dut.rst=0
		print "done initializing"
		data=0

		while True:
			dut.wr=1
			for i in range(0,dut.wr_data_len()): 
				dut.wr_data_set(i,data)
				data+=1
			yield clk.negedge

	return body

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

	d = driver(clk, dut)

	@instance
	def stimulus():
		for i in range (10): yield clk.negedge
		if dump: tracer.close()
		raise StopSimulation

	return clkGen, stimulus, dut_wrap, d


tb=testbench()	


Simulation(tb).run()
