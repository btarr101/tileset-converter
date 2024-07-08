from pathlib import Path
import pytest
from PIL import Image, ImageChops
from tileset_converter.converters import wang_to_blob

FIXTURE_DIR = Path(__file__).parent / "fixtures"
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output"

@pytest.mark.parametrize(
	["wang_path", "blob_path"],
	[
		(FIXTURE_DIR / "wang-template.png", FIXTURE_DIR / "blob-template.png"),
		(FIXTURE_DIR / "tile-caverns-wang.png", FIXTURE_DIR / "tile-caverns-blob.png")
	]
)
def test_wang_to_blob(wang_path, blob_path):
	wang_image = Image.open(wang_path)
	expected_blob_image = Image.open(blob_path)

	blob_image = wang_to_blob(wang_image)
	
	diff = ImageChops.difference(blob_image, expected_blob_image)
	bbox = diff.getbbox()
	if bbox:
		blob_image.save(TEST_OUTPUT_DIR / "wang-to-blob-diff.png")
		pytest.fail(reason=f"Difference found: {str(bbox)}")
