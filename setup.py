long_description =  """\
This package is a small, fast implementation of an algorithm for
finding extremal rays of a polyhedral cone, with filtering.  It is
intended for finding normal surfaces in triangulated 3-manifolds, and
therefore does not implement various features that might be useful for
general extremal ray problems.

The setup is this.  Define the support of a vector v in R^n to be the
set of indices i such that v_i is non-zero.  We are given an integer
matrix M, typically with many more columns than rows, and a list of
"illegal supports".  The support of a vector is illegal if its support
contains one of the illegal supports on the list.

We want to find all the extremal rays of the cone
(Null space of M) intersect (positive orthant),
which are generated by vectors with legal support. (The restriction to
vector with legal support is what is meant by "filtering".)

The algorithm is due to Dave Letscher, and incorporates ideas of Komei
Fukuda's.
"""

import os, re, sys, sysconfig, shutil, subprocess, site
from setuptools import setup, Command, Extension

# Get version number from module
version = re.search("__version__ = '(.*)'",
                    open('python_src/__init__.py').read()).group(1)

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
    sources = ['cython_src/FXraysmodule.c', 'c_src/FXrays.c'],
    include_dirs = ['cython_src', 'c_src'], 
    extra_compile_args = extra_compile_args,
    extra_link_args = extra_link_args
)

class FXraysClean(Command):
    """
    Clean *all* the things!
    """
    user_options = []
    def initialize_options(self):
        pass 
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -rf build dist *.pyc cython_src/*.c FXrays.egg-info')

class FXraysTest(Command):
    user_options = []
    def initialize_options(self):
        pass 
    def finalize_options(self):
        pass
    def run(self):
        build_lib_dir = os.path.join(
            'build',
            'lib.{platform}-{version_info[0]}.{version_info[1]}'.format(
                platform=sysconfig.get_platform(),
                version_info=sys.version_info)
        )
        sys.path.insert(0, build_lib_dir)
        from FXrays.test import runtests
        results = runtests()
        print(results)
        status = 0 if results.failed == 0 else 1
        sys.exit(status)

class FXraysRelease(Command):
    # The -rX option modifies the wheel name by adding rcX to the version string.
    # This is for uploading to testpypi, which will not allow uploading two
    # wheels with the same name.
    user_options = [('rctag=', 'r', 'index for rc tag to be appended to version (e.g. -r2 -> rc2)')]
    def initialize_options(self):
        self.rctag = None
    def finalize_options(self):
        if self.rctag:
            self.rctag = 'rc%s'%self.rctag
    def run(self):
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('dist'):
            shutil.rmtree('dist')

        pythons = os.environ.get('PYTHONRELEASELIST', sys.executable).split(',')
        for python in pythons:
            try:
                subprocess.check_call([python, 'setup.py', 'build'])
            except subprocess.CalledProcessError:
                raise RuntimeError('Build failed for %s.'%python)
            try:
                subprocess.check_call([python, 'setup.py', 'test'])
            except subprocess.CalledProcessError:
                raise RuntimeError('Test failed for %s.'%python)
            try:
                subprocess.check_call([python, 'setup.py', 'bdist_wheel'])
            except subprocess.CalledProcessError:
                raise RuntimeError('Error building wheel for %s.'%python)
            
        if sys.platform.startswith('linux'):
            try:
                subprocess.check_call([python, 'setup.py', 'bdist_egg'])
            except subprocess.CalledProcessError:
                raise RuntimeError('Error building wheel for %s.'%python)
            
            # auditwheel generates names with more tags than allowed by pypi
            extra_tag = re.compile('linux_x86_64\.|linux_i686\.')
            # build wheels tagged as manylinux1
            for wheelname in [name for name in os.listdir('dist') if name.endswith('.whl')]:
                original_path = os.path.join('dist', wheelname)
                subprocess.check_call(['auditwheel', 'addtag', '-w', 'dist', original_path])
                os.remove(original_path)
        else:
            extra_tag = None
        version_tag = re.compile('-([^-]*)-')
        for wheel_name in [name for name in os.listdir('dist') if name.endswith('.whl')]:
            new_name = wheel_name
            if extra_tag:
                new_name = extra_tag.sub('', new_name, 1)
            if self.rctag:
                new_name = version_tag.sub('-\g<1>%s-'%self.rctag, new_name, 1)
            os.rename(os.path.join('dist', wheel_name), os.path.join('dist', new_name))

        try:
            subprocess.check_call([python, 'setup.py', 'sdist'])
        except subprocess.CalledProcessError:
            raise RuntimeError('Error building sdist archive for %s.'%python)

        sdist_version = re.compile('-([^-]*)(.tar.gz)|-([^-]*)(.zip)')
        for archive_name in [name for name in os.listdir('dist')
                             if name.endswith('tar.gz') or name.endswith('.zip')]:
            if self.rctag:
                new_name = sdist_version.sub('-\g<1>%s\g<2>'%self.rctag, archive_name, 1)
                os.rename(os.path.join('dist', archive_name), os.path.join('dist', new_name))

# If have Cython, check that .c files are up to date:

try:
    from Cython.Build import cythonize
    if 'clean' not in sys.argv:
        file = 'cython_src/FXraysmodule.pyx'
        if os.path.exists(file):
            cythonize([file])
except ImportError:
    pass 


setup(
    name = 'FXrays',
    version = version,
    description = 'Computes extremal rays with filtering',
    long_description = long_description,
    url = 'http://t3m.computop.org',
    author = 'Marc Culler and Nathan M. Dunfield',
    author_email = 'culler@uic.edu, nathan@dunfield.info',
    license='GPLv2+',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Mathematics',
        ],

    packages = ['FXrays'],
    package_dir = {'FXrays':'python_src'}, 
    ext_modules = [FXrays],
    cmdclass = {'clean':FXraysClean,
                'test':FXraysTest,
                'release':FXraysRelease},
    zip_safe=False, 
)



       


