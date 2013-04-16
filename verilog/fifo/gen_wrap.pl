use strict;
if (@ARGV!=1) { print "Usage: gen_wrap.pl <path to header file>\n"; return -1;}
my $path = $ARGV[0];
my ($module) = $ARGV[0] =~ /V(\w+)\.h$/ ;

if (!defined($module)) {
	print "ERROR: expect header file to be Vmodule.h";
	return -1;
}

my $fd;
open $fd, $path or die "can't open $path: $!\n";

print  <<EOF;
#include <boost/python.hpp>
#include "$path"
using namespace boost::python;

BOOST_PYTHON_MODULE($module\_wrap)
{
    class_<V$module, boost::noncopyable>("V$module", init<const char*>())
EOF

print "\t\t.def(\"eval\", \&V$module","::eval)";

while (<$fd>) {
	if (my ($dir,$width, $name) = /VL_(IN|OUT)(\d+)?\((\w+)/) {
		if ($dir eq "IN") {
			print "\n\t\t.def_readwrite(\"$name\",\&V$module","::","$name)";
		} else {
			print "\n\t\t.def_readonly(\"$name\",\&V$module","::","$name)";
		}
	}
}
print ";\n}\n"
