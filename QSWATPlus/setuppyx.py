from distutils.core import setup
from distutils.extension import Extension
    
from Cython.Build import cythonize  # @UnresolvedImport
import os
import numpy
if 'QSWAT_PROJECT' in os.environ and 'Linux' in os.environ['QSWAT_PROJECT']:
    includePath = '/usr/include/python3.'
    numpyInclude = numpy.get_include()
    sep = ':'
    is32 = '_32' in os.environ['QSWAT_PROJECT']
elif 'QSWAT_PROJECT' in os.environ and 'Mac' in os.environ['QSWAT_PROJECT']:
    includePath = '/usr/local/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/include/python3.9'
    numpyInclude = numpy.get_include()
    sep = ':'
    is32 = '_32' in os.environ['QSWAT_PROJECT']
else:
    includePath = os.environ['OSGEO4W_ROOT'] + r'/apps/Python37/include'
    numpyInclude = numpy.get_include()
    sep = ';'
    is32 = False
if 'INCLUDE' in os.environ:
    os.environ['INCLUDE'] = os.environ['INCLUDE'] + sep + includePath + sep + numpyInclude 
else:
    os.environ['INCLUDE'] = includePath + sep + numpyInclude
    
print('include path is {0}'.format(os.environ['INCLUDE']))

# NB for Linux also had to 
#sudo ln -s  /usr/lib/python3/dist-packages/numpy/core/include/numpy /usr/include/numpy
# for it to find numpy/arrayobject.h

if is32:
    # only run cythonize to get .c files from .pyx
    cythonize('*.pyx', include_path = [os.environ['INCLUDE']])
else:
    # Create extensions with proper include directories
    extensions = [
        Extension('jenks', ['jenks.pyx'], include_dirs=[includePath, numpyInclude]),
        Extension('dataInC', ['dataInC.pyx'], include_dirs=[includePath, numpyInclude]),
        Extension('polygonizeInC', ['polygonizeInC.pyx'], include_dirs=[includePath, numpyInclude]),
        Extension('polygonizeInC2', ['polygonizeInC2.pyx'], include_dirs=[includePath, numpyInclude]),
    ]
    setup(
        name = "pyxes",
        package_dir = {'QSWATPlus': ''}, 
        ext_modules = cythonize(extensions),
    )
