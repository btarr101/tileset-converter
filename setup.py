from setuptools import setup, find_packages

setup(
	name="tileset_converter",
	version="0.0.1",
	entry_points={
		"console_scripts": [
			"tileset-converter = tileset_converter:convert_tileset"
		]
	},
	packages=find_packages(where="src"),
	package_dir={"": "src"},
	package_data={"": ["*.png"]},
	install_requires=[
		"numpy==2.0.0",
		"pillow==10.4.0",
		"typed-argparse==0.3.1",
		"pydantic==2.8.2",
		"pydantic_core==2.20.1",
		"annotated-types==0.7.0"
	]
)