#include <boost/python.hpp>
#include "../obj_dir/Vfifo.h"
#include "__array_1.pypp.hpp"
using namespace boost::python;

// #define ASIZE sizeof(&Vfifo::wr_data)/sizeof(WData)
#define ASIZE 8

struct abc_wrapper : abc, bp::wrapper< abc > {

    abc_wrapper(abc const & arg )
    : abc( arg )
      , bp::wrapper< abc >(){
        // copy constructor
        
    }

    abc_wrapper()
    : abc()
      , bp::wrapper< abc >(){
        // null constructor
        
    }

    static pyplusplus::containers::static_sized::array_1_t< int, 4>
    pyplusplus_aa_wrapper( ::abc & inst ){
        return pyplusplus::containers::static_sized::array_1_t< int, 4>( inst.aa );
    }

};



BOOST_PYTHON_MODULE(fifo_wrap)
{
    pyplusplus::containers::static_sized::register_array_1< WData, ASIZE  >( "__array_1_int_4" );

    class_<Vfifo, boost::noncopyable>("Vfifo", init<const char*>() )
		.def("eval", &Vfifo::eval)
		.def_readwrite("clk",&Vfifo::clk)
		.def_readwrite("rst",&Vfifo::rst)
		.def_readwrite("wr",&Vfifo::wr)
		.def_readwrite("rd",&Vfifo::rd)
		.def_readonly("empty",&Vfifo::empty)
		.def_readonly("full",&Vfifo::full);

    scope().attr("wr_data") = wr_data_wrapper();
}
