#include <boost/python.hpp>
#include "Vfifo.h"
#ifdef DUMP
#include "verilated_vcd_c.h"
#endif
using namespace boost::python;


struct VfifoWrap : public Vfifo {
	VfifoWrap(const char* name):Vfifo(name) {} 
	int wr_data_len(void) const { return sizeof(wr_data)/sizeof(WData); }
	WData wr_data_get(int idx) const { 
		if (idx<0) { idx += wr_data_len(); }
		if ((idx>=0) && (idx<wr_data_len())) { return wr_data[idx]; }
		throw "WrDataGetIndexException";
	}
	void wr_data_set(int idx, const WData& d) { 
		if (idx<0) { idx += wr_data_len(); }
		if ((idx>=0) && (idx<wr_data_len())) { 
			wr_data[idx]=d;  
			return;
		}
		throw "WrDataSetIndexException";
	}
};

#ifdef DUMP
BOOST_PYTHON_MODULE(fifo_wrap_dump)
#else
BOOST_PYTHON_MODULE(fifo_wrap)
#endif
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
		#ifdef DUMP
		.def("trace", &VfifoWrap::trace)
		#endif
	;

}
