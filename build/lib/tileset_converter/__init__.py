import typed_argparse as tap
from typing import Optional
from PIL import Image as PILImage

from .converters import wang_to_blob

class Args(tap.TypedArgs):
	input_filepath: str = tap.arg("-i", help="Input file path")
	output_filepath: str = tap.arg("-o", default="./blob-tileset.png", help="Output file path")

def run(args: Args):
	try:
		image = PILImage.open(args.input_filepath)
	except FileNotFoundError as exception:
		print(exception)
		quit()

	blob_tileset = wang_to_blob(image)
	blob_tileset.save(args.output_filepath)

def convert_tileset():
	tap.Parser(Args).bind(run).run()
