#!/usr/bin/python
# -*- coding: utf-8 -*-
#=======================================================================================
#This File is part of Yantra: A lattice Boltzmann method based tool for multiscale/
#multiphyics simulations
#=======================================================================================

from setuptools import setup, Extension
import numpy as np
from os import listdir
from os.path import join, isfile, splitext
import sys, os
import shutil

def list_sources_and_modules(parent_folder, parent_package, extensions=['py'],
                             prefix='', exclude=[], result=None):
    """Creates list of sources and module names by going through the parent folder"""
    if result is None:
        result = {'source': [], 'module': []}
    for fname in listdir(parent_folder):
        path = join(parent_folder, fname)
        acceptable = path not in exclude and fname not in exclude
        acceptable = acceptable and "_ignore" not in fname
        if acceptable:
            if isfile(path):
                name, ext = splitext(fname)
                if ext in extensions:
                    name = prefix + name
                    result['module'].append(parent_package + '.' + name)
                    result['source'].append(join(parent_folder, fname))
            else:
                result = list_sources_and_modules(path, parent_package + '.' + fname,
                                                  extensions, prefix, exclude, result)
    return result

def get_ext_modules(name, source, args=[]):
    """Gets list of extension instances from module name and its corresponding Fortran source file"""
    v = [v for v in args if v.startswith('--fcompiler')]
    if v:
        compiler = v[0].split("=")[1].lower()
        gnu_compiler = ["g95", 'gnu95', "mingw32"]
        intel_compiler = ["intel", "intelm", "intelem", "intelv", "intelvem"]
        pg_compiler = ["pg", "pgfortran", "pgf90", "pgf95"]
        
        if compiler in gnu_compiler:
            extra_compile_args = ["-fopenmp", "-fPIC", "-O3", "-fbounds-check",
                                  "-mtune=native"]
            extra_link_args = ["-lgomp"]
        elif compiler in intel_compiler:
            extra_compile_args = ["-qopenmp", "-O3", "-funroll-loops"]
            extra_link_args = ["-liomp5"]
        elif compiler in pg_compiler:
            extra_compile_args = ["-mp"]
            extra_link_args = []
        else:
            raise ValueError("Support for this compiler is not included currently in setup file. Contact the developer.")
    else:
        extra_compile_args = ["-fopenmp", "-O3"]
        extra_link_args = ["-lgomp"]
    
    ext_modules = []
    for (module, src) in zip(name, source):
        fext = Extension(
            name=module,
            sources=[src],
            extra_compile_args=extra_compile_args,  # Fixed issue
            extra_link_args=extra_link_args,
            include_dirs=[np.get_include()]  # Ensuring NumPy headers are included
        )
        ext_modules.append(fext)
    return ext_modules

def run_setup(args):
    """Runs setup to install Yantra"""
    # Write version
    major, minor, patch, release = 1, 0, 0, '-dev'
    version = f"{major}.{minor}.{patch}{release}"
    fname = os.path.join('yantra', 'version.py')
    
    with open(fname, 'w') as f:
        f.write(f"version = '{version}'")
    
    # Get list of Fortran and Python modules
    fort = list_sources_and_modules('yantra', 'yantra', ['.f90'], exclude=[])
    py = list_sources_and_modules('yantra', 'yantra', ['.py'], exclude=[])
    
    # Build extension instances for Fortran modules
    ext_modules = get_ext_modules(fort['module'], fort['source'], args)
    
    # Run setup
    setup(
        name='yantra',
        version=version,
        author='Ravi A. Patel',
        author_email='ravee.a.patel@gmail.com',
        py_modules=py['module'],
        ext_modules=ext_modules,
        license='GPL V3 and later',
    )
    
    print('+++ Setup complete.')

if __name__ == '__main__':
    # Remove existing build directory
    if os.path.isdir('build'):
        shutil.rmtree('build')
    
    # Run setup
    run_setup(sys.argv)
