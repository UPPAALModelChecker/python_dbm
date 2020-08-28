from distutils.core import setup, Extension

setup(
        name = 'python_dbm',
        version = '0.1',
        package_dir = {'python_dbm': ''},
        packages = ['python_dbm'],
        ext_modules = [
            Extension("_udbm_int", 
            sources=["udbm_int.i"], 
            swig_opts=['-c++'],
            include_dirs=['/usr/local/uppaal/include'],
            libraries=['udbm'],
            library_dirs=['/usr/local/uppaal/lib'])
        ]

     )
