# Basic Information

The DBM library has now a binding to the [Python](http://python.org/) language (version 2.x). This binding has been implemented using the [SWIG](http://www.swig.org/) interface generator.

See [this page](http://www.cs.aau.dk/~adavid/python/) for the full list of Python-related timed automata analysis tools and libraries.

# Release

Download: [python_dbm-0.1.tar.gz](http://www.cs.aau.dk/~adavid/UDBM/ureleases/python_dbm-0.1.tar.gz) (linux source, current stable version).  

Up-to-date source code can be found at [Launchpad code repository](https://launchpad.net/pydbm).

# Installing Under Linux

We tested Python binding on Linux only, GCC version 4.4.5\.

If you have problems with building the binding on a 64 bit system, then you probably need to add -fPIC option to CFLAGS in UPPAAL DBM Makefile.

Before installing this binding, you need to install:

1.  [UPPAAL DBM library](http://www.cs.aau.dk/~adavid/UDBM/)
2.  [SWIG](http://www.swig.org/) (we used SWIG Version 1.3.40)

It's assumed that UPPAAL DBM library headers are located in "/usr/local/uppaal/include", and library itself is located in "/usr/local/uppaal/lib". If it's not the case, please modify setup.py  

Please follow these steps:

*   python ./setup.py build
*   sudo python ./setup.py install (if you want to install globally) **or**
*   python ./setup install --user (if you want to install locally)

# Getting Started

Let's create new context with clock variables "x", "y", z":

``` python  
>>> from python_dbm import Context  
>>> c = Context(["x", "y", "z"], "c")  
```


Now we can declare federations of DBMs and operate them in natural way:

``` python
>>> a = (c.x < 10) & (c.x - c.y > 1)  
>>> b = (c.x < 20)  
>>> print a <= b    # is a included in b  
True  
>>> print a >= b    # is b included in a  
False  
>>> print a.up() | b  
(c.x < 20) | (c.x-c.y < 10 & c.x-c.z < 10 & c.y-c.x < -1)  
>>> print a | b  
(c.x < 20)  
```

You can see udbm.py for the complete list of implemented operations over federations of DBMs; test.py contains more examples of usage of this binding.
