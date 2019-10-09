from setuptools import setup
from laxpy import __version__

setup(
    name = 'laxpy',
    version = __version__,
    description = 'A Python API for .lax files',
    license = 'MIT',
    author = 'Bryce Frank',
    author_email = 'bfrank70@gmail.com',
    url = 'https://github.com/brycefrank/laxpy',
    packages = ['laxpy', 'laxpytest'],
    install_requires = [
            'laspy',
            'shapely',
            'numpy',
            'numba'
        ],
    data = [('laxpytest/data'), ['test.las', 'test.lax']],
)
