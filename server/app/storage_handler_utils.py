import grpc

from .config import settings
from protos.storage_pb2_grpc import ItemHandlerStub
from protos import storage_pb2 as storage_pb2

channel = grpc.insecure_channel(
    f"{settings.storage_handler_hostname}:{settings.storage_handler_port}"
)
stub = ItemHandlerStub(channel)


def upload_item(uuid: str, data: bytes):
    _request = storage_pb2.UploadItem_request(uuid=uuid, content=data)
    return stub.UploadItem(_request)


def download_item(uuid: str):
    _request = storage_pb2.DownloadItem_request(uuid=uuid)
    return stub.DownloadItem(_request)
