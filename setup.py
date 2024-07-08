from setuptools import setup, find_packages

setup(
	name="tileset_converter",
	version="0.0.1",
	entry_points={
		"console_scripts": [
			"convert-tileset = tileset_converter:convert_tileset"
		]
	},
	packages=find_packages(where="src"),
	package_dir={"": "src"},
	package_data={"": ["*.png"]},
	install_requires=[
		"numpy==2.0.0",
		"pillow==10.4.0",
		"typed-argparse==0.3.1"
	]
)