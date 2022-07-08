from os import listdir
from os.path import join

from protos import storage_pb2


def upload_item(uuid, content, path):
    uuid = uuid
    if uuid in listdir(path):
        return storage_pb2.UploadItem_response(status=f"uuid {uuid} already exists")
    _path = join(path, uuid)
    with open(_path, "wb") as binary_file:
        binary_file.write(content)
    return storage_pb2.UploadItem_response(status="ok")


def download_item(uuid, path):
    if not uuid in listdir(path):
        return storage_pb2.DownloadItem_response(error=f"No file with uuid {uuid}")
    _path = join(path, uuid)
    with open(_path, "rb") as f:
        content = f.read()
    return storage_pb2.DownloadItem_response(content=content)
