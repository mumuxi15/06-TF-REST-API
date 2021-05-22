import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name="tfdata", 
	version="0.0.1",
	author="Penny.P",
	author_email="mumuxi15@gmail.com",
	description="A small demo",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/mumuxi15",
	project_urls={
		"Bug Tracker": "https://github.com/pypa/sampleproject/issues",
	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	package_dir={"": "tfdata"},
	packages=setuptools.find_packages(where="tfdata"),
	python_requires=">=3.6",
)