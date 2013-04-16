obj_dir/Vfifo: obj_dir/Vfifo.h
	cd obj_dir && make -f Vfifo.mk

obj_dir/Vfifo.h: Makefile fifo.v top.cc
	rm -rfv obj_dir
	mkdir obj_dir
	verilator -cc -exe top.cc --top-module fifo fifo.v
