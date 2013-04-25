#include <boost/python.hpp>
#include "../obj_dir/Vfifo.h"
using namespace boost::python;


struct VfifoWrap : public Vfifo {
	VfifoWrap(const char* name):Vfifo(name) {} 
	int wr_data_len(void) const { return sizeof(wr_data)/sizeof(WData); }
	WData wr_data_get(int idx) const { 
		if (idx<0) { idx += wr_data_len(); }
		if ((idx>=0) && (idx<wr_data_len())) { return wr_data[idx]; }
		throw "IndexException";
	}
	WData wr_data_set(const int idx, const WData& d) { wr_data[idx]=d; }	
};

BOOST_PYTHON_MODULE(fifo_wrap)
{

    class_<VfifoWrap, boost::noncopyable>("Vfifo", init<const char*>() )
		.def("eval", &VfifoWrap::eval)
		.def_readwrite("clk",&VfifoWrap::clk)
		.def_readwrite("rst",&VfifoWrap::rst)
		.def_readwrite("wr",&VfifoWrap::wr)
		.def_readwrite("rd",&VfifoWrap::rd)
		.def_readonly("empty",&VfifoWrap::empty)
		.def_readonly("full",&VfifoWrap::full)
		.def("wr_data_set", &VfifoWrap::wr_data_set)
		.def("wr_data_get", &VfifoWrap::wr_data_get)
		.def("wr_data_len", &VfifoWrap::wr_data_len)
	;

}
