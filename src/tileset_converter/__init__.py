import os

import typed_argparse as tap
from argparse import ArgumentError
from typing import Optional
from PIL import Image as PILImage
import logging
from pydantic_core import from_json
from pathlib import Path

from .converters import wang_to_blob
from .manifest import Manifest, ConversionType, ConversionConfig
from .constants import DEFAULT_MANIFEST_FILENAME

logger = logging.getLogger()

class Args(tap.TypedArgs):
	input_filepath: Optional[str] = tap.arg("-i", help="Input file path", default=None)
	output_filepath: str = tap.arg("-o", default="./blob-tileset.png", help="Output file path")
	conversion: ConversionType = tap.arg("-c", default=ConversionType.WANG_TO_BLOB)

	manifest_path: Optional[str] = tap.arg("-m", help="Manifest file with conversion configuration", default=None)

def command(args: Args):
	conversion_configs: list[ConversionConfig] = []

	if args.manifest_path:
		try:
			with open(args.manifest_path) as manifest_file:
				manifest = Manifest.model_validate_json(manifest_file.read())
		except FileNotFoundError:
			logger.error(f"Manifest file `{args.manifest_path}` not found")
			return

		os.chdir(Path(args.manifest_path).parent)
		
		conversion_configs = manifest.conversion_configs
	else:
		if args.input_filepath:
			conversion_configs = [
				ConversionConfig(
					input_filepath=args.input_filepath,
					output_filepath=args.output_filepath,
					conversion=args.conversion
				)
			]
		else:
			if DEFAULT_MANIFEST_FILENAME in os.listdir("."):
				with open(DEFAULT_MANIFEST_FILENAME) as manifest_file:
					manifest = Manifest.model_validate_json(manifest_file.read())
				conversion_configs = manifest.conversion_configs
			else:
				logger.error(f"Must have either an input filepath, manifest path, or default `{DEFAULT_MANIFEST_FILENAME}` present")
				return
		
	for conversion_config in conversion_configs:
		try:
			image = PILImage.open(conversion_config.source_path)
		except FileNotFoundError as exception:
			logger.error(exception)
			continue

		blob_tileset = wang_to_blob(image)
		blob_tileset.save(conversion_config.destination_path)
		logger.info(f"Converted {conversion_config.source_path} to {conversion_config.destination_path} ({conversion_config.conversion})")

def convert_tileset():
	tap.Parser(Args).bind(command).run()

