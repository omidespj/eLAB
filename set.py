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

def list_sources_and_modules(parent_folder, parent_package, extensions=['.py', '.f90']):
    """Automatically finds Python and Fortran source files."""
    result = {'source': [], 'module': []}
    for fname in os.listdir(parent_folder):
        path = join(parent_folder, fname)
        if isfile(path):
            name, ext = splitext(fname)
            if ext in extensions:
                result['source'].append(abspath(path))
                if ext == ".py":
                    result['module'].append(parent_package + '.' + name)
        else:
            sub_result = list_sources_and_modules(path, parent_package + '.' + fname, extensions)
            result['source'].extend(sub_result['source'])
            result['module'].extend(sub_result['module'])
    return result

def compile_f2py_module(source_file, module_name):
    """Compiles `.f90` Fortran source files using `f2py` automatically."""
    output_path = f"{module_name}.so"
    print(f"+++ Compiling {source_file} into {output_path} using f2py...")
    cmd = ["python3", "-m", "numpy.f2py", "-c", source_file, "-m", module_name, "-O3", "-fopenmp"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error compiling {source_file}:\n", result.stderr)
        raise RuntimeError(f"f2py compilation failed for {source_file}")

    print(f"+++ Successfully compiled {module_name}.so")

def get_ext_modules(name, source, args=[]):
    """Generates a list of compiled Fortran extensions for `setuptools`."""
    extra_compile_args = ["-fopenmp", "-O3"]
    extra_link_args = ["-lgomp"]
    
    ext_modules = []
    for module, src in zip(name, source):
        fext = Extension(
            name=module,
            sources=[src],
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            include_dirs=[np.get_include()]  # Ensure NumPy headers are included
        )
        ext_modules.append(fext)
    return ext_modules

def run_setup():
    """Runs the automatic setup process including Fortran compilation."""
    # Set version
    version = "1.0.0-dev"
    with open(join("yantra", "version.py"), "w") as f:
        f.write(f"version = '{version}'")

    # Find all Python and Fortran sources
    fort = list_sources_and_modules("yantra", "yantra", ['.f90'])
    py = list_sources_and_modules("yantra", "yantra", ['.py'])

    # Compile Fortran modules automatically using `f2py`
    f2py_modules = []
    for f90_file in fort['source']:
        module_name = splitext(os.path.basename(f90_file))[0]
        compile_f2py_module(f90_file, module_name)
        f2py_modules.append(module_name)

    # Build Fortran extension instances
    ext_modules = get_ext_modules(fort['module'], fort['source'])

    # Run setup
    setup(
        name="yantra",
        version=version,
        author="Ravi A. Patel",
        author_email="ravee.a.patel@gmail.com",
        py_modules=py['module'] + f2py_modules,  # Include Python and Fortran modules
        ext_modules=ext_modules,
        include_dirs=[np.get_include()],
        license="GPL V3 and later",
    )

    print("+++ Setup complete.")

if __name__ == "__main__":
    # Remove existing build directory
    if os.path.isdir("build"):
        shutil.rmtree("build")

    # Run setup
    run_setup()
