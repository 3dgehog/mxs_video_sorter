from setuptools import setup, find_packages


def readme():
	with open('README.md') as f:
		return f.read()


setup(
	name='mxs_video_sorter',
	version='1.0b1',
	python_requires='>=3.4',
	description="Mx's video sorter for series and movies",
	long_description=readme(),
	url='http://github.com/Scheercuzy/mxs_video_sorter',
	author='Scheercuzy',
	author_email='maxi730@gmail.com',
	license='MIT',
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'mxs_video_sorter = mxs_video_sorter.__main__:main'
		]
	},
	package_data={
		'mxs_video_sorter': [
			'conf_template/config.yaml',
			'conf_template/rule_book.conf',
			'logging.yaml'
		]
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
		'guess-language-spirit==0.5.3'
	]
)
