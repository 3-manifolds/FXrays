project('FXrays', 'cython', 'c')

py = import('python').find_installation(pure: false)
dep_py = py.dependency()

fxmod = py.extension_module(
    'FXraysmodule',
    sources : ['cython_src/FXraysmodule.pyx', 'c_src/FXrays.c'],
    include_directories : ['c_src'],
    dependencies : dep_py,
    subdir : 'FXrays',
    install : true,
)

python_sources = [
    'python_src/__init__.py',
    'python_src/_test.py',
    'python_src/test.py'
]

py.install_sources(
    python_sources,
    subdir : 'FXrays',
)
