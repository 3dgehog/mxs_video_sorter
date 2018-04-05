from setuptools import setup


def readme():
	with open('README.md') as f:
		return f.read()


setup(
	name='mxs_video_sorter',
	version='1.0a1',
	python_requires='>=3.5',
	description="Mx's video sorter for series and movies",
	long_description=readme(),
	url='http://github.com/Scheercuzy/mxs_video_sorter',
	author='Scheercuzy',
	author_email='maxi730@gmail.com',
	license='MIT',
	packages=['mxs_video_sorter'],
	scripts=['mxs_video_sorter/main.py'],
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
	]
)
