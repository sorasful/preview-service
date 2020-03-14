import hashlib
import json
import os

import uvicorn
from preview_generator.manager import PreviewManager
from starlette import status
from starlette.applications import Starlette
from starlette.responses import (
    FileResponse,
    JSONResponse,
    PlainTextResponse,
)
from starlette.staticfiles import StaticFiles

UPLOAD_DIR = '/tmp/files/'
CACHE_PATH = '/tmp/cache/'

app = Starlette()
app.mount('/cache', StaticFiles(directory=CACHE_PATH), name='cache')

manager = PreviewManager(CACHE_PATH, create_folder=True)


def error_response(error_message, status=None):
    return JSONResponse({"error": error_message}, status_code=status)


async def _store_uploaded_file(file) -> str:
    contents = await file.read()
    h = hashlib.md5(contents).hexdigest()
    upload_dest = os.path.join(UPLOAD_DIR, '.'.join([h, file.filename]))

    with open(upload_dest, 'wb+') as f:
        f.write(contents)

    return upload_dest


@app.route('/')
async def health_endpoint(request):
    return PlainTextResponse('OK')


@app.route('/preview/{width:int}x{height:int}', methods=['POST'])
async def preview_endpoint(request):
    width = request.path_params['width']
    height = request.path_params['height']

    form = await request.form()
    file = form.get('file', None)
    return_as_image = form.get('return_as_image', None)

    if file is None:
        return error_response('"file" is missing', status.HTTP_400_BAD_REQUEST)
    file_path = await _store_uploaded_file(file)

    try:
        image = manager.get_jpeg_preview(file_path, width=width, height=height)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

    if return_as_image is None or str(return_as_image).lower() != "true":
        img_url = image.split("/tmp")[-1]

        return PlainTextResponse(json.dumps({'url': img_url}))

    return FileResponse(image)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
