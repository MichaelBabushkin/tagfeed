import shutil

import unittest

from .config import settings
from storage_handler.app.server import Listener


class Req:
    def __init__(self, uuid, content=None):
        self.uuid = uuid
        if content:
            self.content = content


class GrpcTest(unittest.TestCase):
    def setUp(self):
        self.server = Listener(subfolder=settings.app_data_folder)

    def tearDown(self):
        shutil.rmtree(f"{settings.app_folder}/{settings.app_data_folder}")

    def test_upload_strings(self):
        for uuid in range(2):
            res = self.server.UploadItem(
                Req(str(uuid), bytes(f"{uuid}: Hello world", "utf-8"))
            )
            self.assertEqual(res.status, "ok")

    def test_download_strings(self):
        self.test_upload_strings()
        for uuid in range(2):
            res = self.server.DownloadItem(Req(str(uuid)))
            self.assertEqual(res.content, bytes(f"{uuid}: Hello world", "utf-8"))

    def test_upload_image(self):
        with open(f"{settings.app_folder}/tests/tagfeed.png", "rb") as f:
            content = f.read()
        res = self.server.UploadItem(Req(str(2), content))
        self.assertEqual(res.status, "ok")

    def test_download_image(self):
        self.test_upload_image()
        with open(f"{settings.app_folder}/tests/tagfeed.png", "rb") as f:
            content2 = f.read()
        res = self.server.DownloadItem(Req(str(2)))
        self.assertEqual(res.content, content2)
