from distutils.core import setup, Extension
import os

FXrays = Extension("FXrays", sources = ["FXraysmodule.c"], extra_objects = ["FXrays.o"])

os.system('make FXrays.o')

setup( name = "FXrays",
       version = "1.0",
       description = "Computes extremal rays with filtering.",
       ext_modules = [FXrays],
       )



       


