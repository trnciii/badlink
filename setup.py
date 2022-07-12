from setuptools import setup, find_packages

setup(
	name='lnman',
	version='1.0.2',
	url='https://github.com/trnciii/lnman',
	license='MIT',
	packages=find_packages(),
	entry_points={
		'console_scripts': ['lnman = lnman.__main__:main']
	}
)
