from setuptools import setup

setup(
    name = 'laxpy',
    version = '0.2.3',
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
