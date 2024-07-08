from pathlib import Path

import PIL.Image as PILImage
from PIL.Image import Image
import numpy as np

from .util import image_chunks

def wang_to_blob(image: Image) -> Image:
	WANG_HORIZONTAL_TILES = 10
	WANG_VERTICAL_TILES = 6

	image_width, image_height = image.size
	tile_width = image_width // WANG_HORIZONTAL_TILES
	tile_height = image_height // WANG_VERTICAL_TILES

	tiles = image_chunks(image, WANG_HORIZONTAL_TILES, WANG_VERTICAL_TILES)

	mask = PILImage.open(Path(__file__).parent / "masks" / "wang-to-blob-mask.png")
	blob_horizontal_tiles, blob_vertical_tiles = mask.size

	mask2 = mask.copy()
	for x in range(blob_horizontal_tiles):
		for y in range(blob_vertical_tiles):
			r, g, b, a = mask2.getpixel((x, y)) # type: ignore
			mask2.putpixel((x, y), (r // 3, g // 3, b // 3, a))
	mask2.save("tempmask2.png")

	blob_image = PILImage.new(
		mode="RGBA",
		size=(
			tile_width*blob_horizontal_tiles,
			tile_height*blob_vertical_tiles
		)
	)

	for x in range(blob_horizontal_tiles):
		for y in range(blob_vertical_tiles):
			pixel: tuple[int, int, int, int] = mask.getpixel((x, y)) # type: ignore
			r, g, b, a = pixel
			if a > 0:
				try:
					source_index = r
					blob_image.paste(tiles[source_index], box=(x * tile_width, y * tile_height))
				except Exception as e:
					pass

	return blob_image