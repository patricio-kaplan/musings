from myhdl import *
import sys

sys.path.append('/home/patricio/Documents/musings_gen/verilog/fifo/src')
import verilated_wrap
import verilated_vcd_c_wrap
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

		while True:
			dut.wr=1
			dut.wr_data+=1
			yield clk.negedge

	return body

def testbench():
	clk = Signal(intbv(0))

	verilated_wrap.traceEverOn(True)
	tracer = verilated_vcd_c_wrap.VerilatedVcdC()
	dut = fifo_wrap.Vfifo("hello")
	dut.trace(tracer,99,100)
	tracer.open('dump.vcd')

	dut.rst=1
	dut.clk=0

	@always(delay(10))
	def clkGen(): 
		tracer.dump(now())
		clk.next = not clk;

	@always(clk.posedge, clk.negedge)
	def dut_wrap():
		dut.clk=int(clk)
		dut.eval()

	d = driver(clk, dut)

	@instance
	def stimulus():
		for i in range (10): yield clk.negedge
		tracer.close()
		raise StopSimulation

	return clkGen, stimulus, dut_wrap, d


tb=testbench()	


Simulation(tb).run()
