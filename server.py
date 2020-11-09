from concurrent import futures
import logging

import grpc

import file_serve_pb2
import file_serve_pb2_grpc
import os

from os import listdir
from os.path import isfile, join


class FileServer(file_serve_pb2_grpc.FileServiceServicer):
    _PIECE_SIZE_IN_BYTES = 1024 * 1024  # 1MB

    def GetFile(self, request, context):
        fileName = 'files/' + request.name
        if os.path.isfile("./" + fileName):
            with open(fileName, 'rb') as content_file:
                while True:
                    content = content_file.read(FileServer._PIECE_SIZE_IN_BYTES)
                    if len(content) == 0:
                        break
                    yield file_serve_pb2.FileResponse(data=content)
        else:
            print(fileName + " not found")
            yield file_serve_pb2.FileResponse()

    def GetFileList(self, request, context):
        onlyfiles = [file_serve_pb2.FileNameResponse(name=f) for f in listdir('files')
                     if isfile(join('files', f))]
        return iter(onlyfiles)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_serve_pb2_grpc.add_FileServiceServicer_to_server(FileServer(), server)
    server.add_insecure_port('[::]:8001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
