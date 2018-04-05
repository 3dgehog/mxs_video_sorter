from setuptools import setup


def readme():
	with open('README.md') as f:
		return f.read()


setup(
	name='7m_video_sorter',
	version='1.0a1',
	python_requires='>=3.5',
	description='A video sorter for series and movies',
	long_description=readme(),
	url='http://github.com/Scheercuzy/7m_video_sorter',
	author='Scheercuzy',
	author_email='maxi730@gmail.com',
	license='MIT',
	packages=['7m_video_sorter'],
	package_data={
		'7m_video_sorter': ['*.yaml', '*.conf']
	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"Development Status :: Beta",
		"License :: OSI Approved :: MIT License"
	],
	install_requires=[
		'colorlog==3.1.2',
		'guessit==2.1.4',
		'progressbar2==3.36.0',
		'PyYAML==3.12',
	],
	zip_safe=False
)
