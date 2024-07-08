# Tileset Converter

CLI tool to convert tilesets (aka. from Wang to Blob etc.).

## Install it from PyPI (TODO)

```bash
$ pip install tileset_converter
```

## Usage

```py
from PIL import Image
from tileset_converter import wang_to_blob

wang_tileset = Image.open("some-wang-tileset.png")
blob_tileset = wang_to_blob(wang_tileset)
blob_tileset.save("some-blob-tileset.png")
```

```bash
$ convert-tileset -i "some-wang-tileset.png" --o "some-blob-tileset.png"
```

## Development

```bash
$ pip install -r requirements.txt
```

Then

```
$ pytest
```
