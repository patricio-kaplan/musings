from distutils.core import setup, Extension
import os

os.environ['ARCHFLAGS']='-arch x86_64'

module1 = Extension('fifo_wrap',
                    sources = ['fifo_wrap.cpp'],
		    include_dirs=['/Users/patriciokaplan/Downloads/boost_1_53_0'
				 ,'/Users/patriciokaplan/Downloads/verilator-3.846/include'
				 ],
		    libraries=['boost_python'],
		    library_dirs=['/Users/patriciokaplan/Downloads/boost_1_53_0/stage/lib'],
		   )

setup (name = 'fifo_wrap',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])
