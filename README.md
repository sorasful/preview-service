# preview-service

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Travis](https://img.shields.io/travis/FPurchess/preview-service/master.svg?logo=travis)](https://travis-ci.org/FPurchess/preview-service)

Super slim webservice to generate thumbnail images for document files (pdf, odt, doc, docx), video files (mp4, flv, webm, ogv, wmv), 3D Files (ply, obj, stl) and many more using a simple HTTP API.

This is a simple wrapper around [algoo/preview-generator](https://github.com/algoo/preview-generator).

See the [full list of supported file formats](https://github.com/algoo/preview-generator#supported-file-formats).

## Usage

Boot up the service:

```bash
docker build -t preview-service .
```


```bash
docker run -p 8000:8000 -v /tmp/cache/:/tmp/cache/ -v /tmp/files/:/tmp/files/ preview-service
```

**INFO** : You may need to update /tmp/cachec and /tmp/files permissions.


Use it to create a thumbnail:

```bash
curl -o thumbnail.jpeg -F 'file=file_to_preview.pdf' http://localhost:8000/preview/100x100
```

## Optional Volumes

- `/tmp/cache/` - mount it to persist thumbnail cache
- `/tmp/files/` - stores all uploaded files

Here's a full example:


## API

### GET `/`

Returns 200 OK when the service is up and running.

### POST `/preview/{width}x{height}`

Awaits a the file to be converted in a `multipart/form-data` with form name `file`.
Returns the converted file as a file response if the conversion is successful.

```bash
curl -o thumbnail.jpeg -F 'file=file_to_preview.pdf' http://localhost:8000/preview/100x100
```

Creates a 100x100 JPEG thumbnail image of `file_to_preview.pdf` and stores it in `thumbnail.jpeg`.

### GET `/cache/<cached-file>`

Returns a cached converted file if present.

## Thanks

Thanks [algoo](https://github.com/algoo/) and all contributors of [algoo/preview-generator](https://github.com/algoo/preview-generator).

## LICENSE

see LICENSE file
