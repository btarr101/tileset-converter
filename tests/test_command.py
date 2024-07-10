from pathlib import Path
import pytest
from tileset_converter import command, Args
from tileset_converter.manifest import Manifest, ConversionConfig, ConversionType
from tileset_converter.constants import DEFAULT_MANIFEST_FILENAME
import os
import glob

from .test_converters import FIXTURE_DIR, TEST_OUTPUT_DIR


@pytest.fixture(autouse=True)
def cleanup():
	files = glob.glob(f"{TEST_OUTPUT_DIR}/*")
	for file in files:
		os.remove(file)

	yield


def test_default_manifest(tmp_path_factory: pytest.TempPathFactory):
	tmpdir = tmp_path_factory.mktemp("test")
	manifest = Manifest(
		conversion_configs=[
			ConversionConfig(
				source_path=FIXTURE_DIR / "wang-template.png",
				destination_path=tmpdir / "blob-test.png",
				conversion=ConversionType.WANG_TO_BLOB
			)
		]
	)
	with open(tmpdir / DEFAULT_MANIFEST_FILENAME, "w+") as manifest_file:
		manifest_file.write(manifest.model_dump_json())

	previous_dir = os.getcwd()
	os.chdir(tmpdir)

	command(Args())

	os.chdir(previous_dir)
	assert manifest.conversion_configs[0].destination_path.exists()


def test_attempt_default_manifest(caplog: pytest.LogCaptureFixture):
	command(Args())

	assert caplog.records[0].message == f"Must have either an input filepath, manifest path, or default `{DEFAULT_MANIFEST_FILENAME}` present"


def test_specified_manifest(caplog: pytest.LogCaptureFixture):
	caplog.set_level("INFO")
	args = Args(
		manifest_path=FIXTURE_DIR / "manifest-template.json"
	)

	command(args)

	assert (TEST_OUTPUT_DIR / "blob-template.png").exists()
	assert "Converted" in caplog.records[0].message


def test_attempt_specified_manifest(caplog: pytest.LogCaptureFixture):
	args = Args(
		manifest_path="i do not exist"
	)

	command(args)

	assert caplog.records[0].message == "Manifest file `i do not exist` not found"