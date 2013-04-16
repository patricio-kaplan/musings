#include <boost/python.hpp>
#include "../obj_dir/Vfifo.h"
#include "../include/verilated_vcd_c.h"
using namespace boost::python;

BOOST_PYTHON_MODULE(fifo_wrap)
{
    class_<Vfifo, boost::noncopyable>("Vfifo", init<const char*>())
		.def("eval", &Vfifo::eval)
		.def("trace", &Vfifo::trace)
		.def_readwrite("clk",&Vfifo::clk)
		.def_readwrite("rst",&Vfifo::rst)
		.def_readwrite("wr",&Vfifo::wr)
		.def_readwrite("rd",&Vfifo::rd)
		.def_readonly("empty",&Vfifo::empty)
		.def_readonly("full",&Vfifo::full)
		.def_readwrite("wr_data",&Vfifo::wr_data)
		.def_readonly("rd_data",&Vfifo::rd_data);
}
