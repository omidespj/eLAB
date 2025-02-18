#!/usr/bin/python
# -*- coding: utf-8 -*-
#=======================================================================================
# This File is part of Yantra: A lattice Boltzmann method based tool for multiscale/
# multiphyics simulations
#=======================================================================================

from setuptools import setup, Extension
import numpy as np
import os
import shutil
import subprocess
from os.path import join, isfile, splitext, abspath

def list_sources_and_modules(parent_folder, extensions=['.py', '.f90']):
    """Automatically finds Python and Fortran source files."""
    sources = []
    modules = []
    for root, _, files in os.walk(parent_folder):
        for fname in files:
            path = join(root, fname)
            name, ext = splitext(fname)
            if ext in extensions:
                sources.append(abspath(path))
                if ext == ".py":
                    modules.append(path.replace("/", ".").rstrip(".py"))
    return sources, modules

def compile_f2py_module(source_file, module_name):
    """Automatically compiles `.f90` files using `f2py`."""
    output_path = f"{module_name}.so"
    print(f"+++ Compiling {source_file} into {output_path} using f2py...")
    cmd = ["python3", "-m", "numpy.f2py", "-c", source_file, "-m", module_name, "-O3", "-fopenmp"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error compiling {source_file}:\n", result.stderr)
        raise RuntimeError(f"f2py compilation failed for {source_file}")

    print(f"+++ Successfully compiled {module_name}.so")

def run_setup():
    """Runs the automatic setup process including Fortran compilation."""
    # Write version
    version = "1.0.0-dev"
    with open(join("yantra", "version.py"), "w") as f:
        f.write(f"version = '{version}'")

    # Find Python and Fortran files
    fort_sources, py_modules = list_sources_and_modules("yantra")

    # Compile Fortran modules automatically
    f2py_modules = []
    for f90_file in [f for f in fort_sources if f.endswith(".f90")]:
        module_name = splitext(os.path.basename(f90_file))[0]
        compile_f2py_module(f90_file, module_name)
        f2py_modules.append(module_name)

    # Setup
    setup(
        name="yantra",
        version=version,
        author="Ravi A. Patel",
        author_email="ravee.a.patel@gmail.com",
        packages=["yantra"],
        py_modules=py_modules + f2py_modules,  # Include Fortran modules
        include_dirs=[np.get_include()],  # Ensure NumPy headers are included
        license="GPL V3 and later",
    )

    print("+++ Setup complete.")

if __name__ == "__main__":
    # Remove existing build directory
    if os.path.isdir("build"):
        shutil.rmtree("build")

    # Run setup
    run_setup()
