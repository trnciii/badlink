from setuptools import setup, find_packages

setup(
	name='lnman',
	version='1.0.1',
	url='https://github.com/trnciii/lnman',
	license='MIT',
	packages=find_packages(),
	entry_points={
		'console_scripts': ['lnman = lnman.main:main']
	}
)
