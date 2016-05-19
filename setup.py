try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from distutils.extension import Extension


libname="PyHtmlReport"
setup(
name = libname,
version= "0.1",
packages=         ['PyHtmlReport'],
)

