import sys
from setuptools import setup, Extension
from Cython.Build import cythonize

extra_link_args = []
extra_compile_args = []
if sys.platform.startswith('win'):
    # NOTE: this is for msvc not mingw32
    # There are issues with mingw64 linking agains msvcrt.
    extra_compile_args = ['/Ox']
else:
    extra_compile_args=['-O3', '-funroll-loops']

if sys.platform.startswith('linux'):
    extra_link_args=['-Wl,-Bsymbolic-functions', '-Wl,-Bsymbolic']
else:
    extra_link_args=[]

FXrays = Extension(
    name = 'FXrays.FXraysmodule',
    sources = ['cython_src/FXraysmodule.pyx', 'c_src/FXrays.c'],
    include_dirs = ['cython_src', 'c_src'],
    extra_compile_args = extra_compile_args,
    extra_link_args = extra_link_args
)


setup(
    packages = ['FXrays', 'FXrays.cython_src'],
    package_dir = {'FXrays':'python_src', 'FXrays.cython_src':'cython_src'},
    ext_modules = cythonize([FXrays]),
    package_data = {'FXrays.cython_src':['FXraysmodule.pyx']},
    zip_safe=False,
)
