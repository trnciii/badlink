from setuptools import setup, find_packages
from lnman.core import version_string

setup(
	name='lnman',
	version=version_string,
	url='https://github.com/trnciii/lnman',
	license='MIT',
	packages=find_packages(),
	package_data={'lnman':['data/*']},
	entry_points={
		'console_scripts': ['lnman = lnman.__main__:main']
	}
)
