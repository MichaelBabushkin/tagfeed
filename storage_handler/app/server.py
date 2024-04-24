from concurrent import futures
import threading
import time
import os
from os import listdir, mkdir
from os.path import join

import grpc

from .config import settings
from protos import storage_pb2_grpc
from .services import upload_item, download_item


class Listener(storage_pb2_grpc.ItemHandlerServicer):
    """The listener function implemests the rpc call as described in the .proto file"""

    def __init__(self, folder=settings.app_folder, subfolder=settings.app_data_folder):
        self.data_dir = subfolder
        self.cur_path = join(os.path.abspath(os.getcwd()), folder)
        self.full_path_data_dir = join(self.cur_path, self.data_dir)
        if not self.data_dir in listdir(self.cur_path):
            mkdir(self.full_path_data_dir)

    def UploadItem(self, request, context={}):
        return upload_item(request.uuid, request.content, self.full_path_data_dir)

    def DownloadItem(self, request, context={}):
        return download_item(request.uuid, self.full_path_data_dir)


def serve():
    """The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    storage_pb2_grpc.add_ItemHandlerServicer_to_server(Listener(), server)
    server.add_insecure_port(f"[::]:{settings.storage_handler_port}")
    server.start()
    try:
        while True:
            print("Server Running : threadcount %i" % (threading.active_count()))
            time.sleep(10)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        server.stop(0)


if __name__ == "__main__":
    serve()
