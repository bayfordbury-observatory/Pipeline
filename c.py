import numpy
import ctypes


from numpy.ctypeslib import ndpointer

lib = ctypes.cdll.LoadLibrary("py.so")
fun = lib.cfun
fun.restype = None
fun.argtypes = [ndpointer(ctypes.c_short, flags="C_CONTIGUOUS"), ctypes.c_size_t, ndpointer(ctypes.c_short, flags="C_CONTIGUOUS")]



indata = numpy.ones((8,8),dtype="int16")
outdata = numpy.empty((8,8),dtype="int16")

fun(indata, indata.size, outdata)


print 'indata: %s' % indata
print 'indatasize: %s' % indata.size
print 'outdata: %s' % outdata