from itertools import product
from PIL.Image import Image

def image_chunks(image: Image, horizontal_chunks: int, vertical_chunks: int) -> list[Image]:
	"""
	Creates new images by splitting a source image into `horizontal_chunks` * `vertical_chunks` in a grid like fasion.
	"""
	image_width, image_height = image.size
	chunk_width = image_width // horizontal_chunks
	chunk_height = image_height // vertical_chunks

	return [
		image.crop((
			x_chunk * chunk_width,
			y_chunk * chunk_height,
			(x_chunk + 1) * chunk_width,
			(y_chunk + 1) * chunk_height
		))
		for y_chunk, x_chunk in product(range(0, vertical_chunks), range(0, horizontal_chunks))
	]
