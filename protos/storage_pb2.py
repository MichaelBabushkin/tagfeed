# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/storage.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14protos/storage.proto\"3\n\x12UploadItem_request\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"%\n\x13UploadItem_response\x12\x0e\n\x06status\x18\x01 \x01(\t\"$\n\x14\x44ownloadItem_request\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"Z\n\x15\x44ownloadItem_response\x12\x11\n\x07\x63ontent\x18\x01 \x01(\x0cH\x00\x12\x0f\n\x05\x65rror\x18\x02 \x01(\tH\x00\x42\x1d\n\x1b\x44ownloadItem_response_oneof2\x85\x01\n\x0bItemHandler\x12\x37\n\nUploadItem\x12\x13.UploadItem_request\x1a\x14.UploadItem_response\x12=\n\x0c\x44ownloadItem\x12\x15.DownloadItem_request\x1a\x16.DownloadItem_responseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.storage_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_UPLOADITEM_REQUEST']._serialized_start=24
  _globals['_UPLOADITEM_REQUEST']._serialized_end=75
  _globals['_UPLOADITEM_RESPONSE']._serialized_start=77
  _globals['_UPLOADITEM_RESPONSE']._serialized_end=114
  _globals['_DOWNLOADITEM_REQUEST']._serialized_start=116
  _globals['_DOWNLOADITEM_REQUEST']._serialized_end=152
  _globals['_DOWNLOADITEM_RESPONSE']._serialized_start=154
  _globals['_DOWNLOADITEM_RESPONSE']._serialized_end=244
  _globals['_ITEMHANDLER']._serialized_start=247
  _globals['_ITEMHANDLER']._serialized_end=380
# @@protoc_insertion_point(module_scope)
