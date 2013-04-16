#include <boost/python.hpp>
#include "../include/verilated.h"

BOOST_PYTHON_MODULE(verilated_wrap)
{
	using namespace boost::python;
	def("traceEverOn", &Verilated::traceEverOn);
}
