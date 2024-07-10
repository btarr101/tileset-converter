from enum import Enum

from pydantic import BaseModel
from pathlib import Path


class ConversionType(Enum):
	WANG_TO_BLOB = "WANG_TO_BLOB"


class ConversionConfig(BaseModel):
	source_path: Path
	destination_path: Path
	conversion: ConversionType


class Manifest(BaseModel):
	conversion_configs: list[ConversionConfig]
