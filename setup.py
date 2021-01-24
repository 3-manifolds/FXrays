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
from distutils.util import get_platform
from glob import glob


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
        for dir in ['build', 'dist', 'FXrays.egg-info']:
            shutil.rmtree(dir, ignore_errors=True)
        for file in glob('*.pyc') + glob('cython_src/*.c'):
            if os.path.exists(file):
                os.remove(file)

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
        sys.path.insert(0, os.path.abspath(build_lib_dir))
        from FXrays.test import runtests
        results = runtests()
        print(results)
        status = 0 if results.failed == 0 else 1
        sys.exit(status)

def check_call(args):
    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError:
        executable = args[0]
        command = [a for a in args if not a.startswith('-')][-1]
        raise RuntimeError(command + ' failed for ' + executable)
        
class FXraysRelease(Command):
    user_options = [('install', 'i', 'install the release into each Python')]
    def initialize_options(self):
        self.install = False
    def finalize_options(self):
        pass
    def run(self):
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('dist'):
            shutil.rmtree('dist')

        pythons = os.environ.get('RELEASE_PYTHONS', sys.executable).split(',')
        for python in pythons:
            check_call([python, 'setup.py', 'build'])
            check_call([python, 'setup.py', 'test'])
            if self.install:
                check_call([python, 'setup.py', 'pip_install'])
            else:
                check_call([python, 'setup.py', 'bdist_wheel'])

        # Build sdist using the *first* specified Python
        check_call([pythons[0], 'setup.py', 'sdist'])

        # Double-check the Linux wheels
        if sys.platform.startswith('linux'):
            for name in os.listdir('dist'):
                if name.endswith('.whl'):
                    subprocess.check_call(['auditwheel', 'repair', os.path.join('dist', name)])

class FXraysPipInstall(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        python = sys.executable
        check_call([python, 'setup.py', 'bdist_wheel'])
        egginfo = 'FXrays.egg-info'
        if os.path.exists(egginfo):
            shutil.rmtree(egginfo)
        wheels = glob('dist' + os.sep + '*.whl')
        new_wheel = max(wheels, key=os.path.getmtime)            
        check_call([python, '-m', 'pip', 'install',
                    '--upgrade', '--force-reinstall',
                    new_wheel])
        
                   

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
    python_requires = '>=3',
    description = 'Computes extremal rays with filtering',
    long_description = long_description,
    url = 'http://t3m.computop.org',
    author = 'Marc Culler and Nathan M. Dunfield',
    author_email = 'culler@marc-culler.info, nathan@dunfield.info',
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
                'release':FXraysRelease,
                'pip_install':FXraysPipInstall,
    },
    zip_safe=False, 
)



       


