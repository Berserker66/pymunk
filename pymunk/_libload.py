"""This module contain functions used to load the chipmunk dll/lib file"""
__version__ = "$Id$"

import os.path
import platform
import sys, imp, os
 
def load_library(ffi, libname, debug_lib=True):
    # lib gets loaded from
    # 32bit python: pymunk/libchipmunk.so, libchipmunk.dylib or chipmunk.dll
    # 64 bit python pymunk/libchipmunk64.so, libchipmunk.dylib or chipmunk64.dll
    
    s = platform.system()
    if sys.maxsize > 2**32:
        arch = "64"
    else:
        arch = "32"
        
    path = os.path.dirname(os.path.abspath(__file__))
    
    try:
        if hasattr(sys, "frozen") or \
            hasattr(sys, "importers") or \
            hasattr(imp, "is_frozen") and imp.is_frozen("__main__"):
            if 'site-packages.zip' in __file__:
                path = os.path.join(os.path.dirname(os.getcwd()), 'Frameworks')
            else:
                path = os.path.dirname(os.path.abspath(sys.executable))
    except:
        pass
    
    if arch == "64":
        arch_param = "64"
    else:
        arch_param = ""
    
    if s in ('Linux', 'FreeBSD'):
        libfn = "lib%s%s.so" % (libname, arch_param)
        
    elif s in ('Windows', 'Microsoft'):
        libfn = "%s%s.dll" % (libname, arch_param)
        
    elif s == 'Darwin':
        libfn = "lib%s.dylib" % libname
        
    # we use *nix library naming as default
    else: 
        libfn = "lib%s.so" % libname
        
    libfn = os.path.join(path, libfn)
    
    
    if debug_lib:
        print ("Loading chipmunk for %s (%sbit) [%s]" % (s, arch, libfn))
    try:
        lib = ffi.dlopen(libfn)
    except OSError: 
        print ("""
Failed to load pymunk library.

This error usually means that you don't have a compiled version of chipmunk in 
the correct spot where pymunk can find it. pymunk does not include precompiled 
chipmunk library files for all platforms. 

The good news is that it is usually enough (at least on *nix and OS X) to 
simply run the compile command first before installing and then retry again:

You compile chipmunk with
> python setup.py build_clib
and then continue as usual with 
> python setup.py install
> cd examples
> python basic_test.py

(for complete instructions please see the readme file)

If it still doesnt work, please report as a bug on the issue tracker at 
https://github.com/viblo/pymunk/issues
Remember to include information about your OS, which version of python you use 
and the version of pymunk you tried to run. A description of what you did to 
trigger the error is also good. Please include the exception traceback if any 
(usually found below this message).
""")
        raise
    return lib
