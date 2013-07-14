from distutils.core import setup, Extension
import os

FXrays = Extension("FXrays", sources = ["FXraysmodule.c", "FXrays.c"],
                   extra_compile_args=["-O3", "-funroll-loops"])

setup( name = "FXrays",
       version = "1.0",
       description = "Computes extremal rays with filtering.",
       ext_modules = [FXrays],
       )



       


