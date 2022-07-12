from setuptools import setup, find_packages
from lnman.version.version import version_string

setup(
	name='lnman',
	version=version_string,
	url='https://github.com/trnciii/lnman',
	license='MIT',
	packages=find_packages(),
	entry_points={
		'console_scripts': ['lnman = lnman.__main__:main']
	}
)
