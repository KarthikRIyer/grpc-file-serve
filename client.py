from __future__ import print_function
import logging

import grpc

import file_serve_pb2
import file_serve_pb2_grpc


def list_files():
    with grpc.insecure_channel('localhost:8001') as channel:
        stub = file_serve_pb2_grpc.FileServiceStub(channel)
        file_list_stream = stub.GetFileList(file_serve_pb2.FileListRequest())
        for response in file_list_stream:
            print(response.name)


def download_file(name):
    with grpc.insecure_channel('localhost:8001') as channel:
        stub = file_serve_pb2_grpc.FileServiceStub(channel)
        response_stream = stub.GetFile(file_serve_pb2.FileRequest(name=name))
        try:
            with open(name, "wb") as fh:
                for response in response_stream:
                    fh.write(response.data)
        except grpc.RpcError as e:
            logging.error(str(e.details))


if __name__ == '__main__':
    logging.basicConfig()
    list_files()
    download_file(name='file3.jpg')
