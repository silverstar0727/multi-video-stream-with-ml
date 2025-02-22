import grpc 
import yolox_pb2, yolox_pb2_grpc

import cv2
import base64

def grpc_call(img_arr, grpc_server_url="localhost:50051"):
    options = [
        ('grpc.max_send_message_length', 1024 * 1024 * 1024), 
        # ('grpc.max_receive_message_length', 1024 * 1024 * 1024 )
    ]
    channel = grpc.insecure_channel(grpc_server_url, options)
    stub = yolox_pb2_grpc.YoloxStub(channel)

    data = base64.b64encode(img_arr)

    request_data = yolox_pb2.B64Image(
        b64image=data, 
        width=img_arr.shape[0], 
        height=img_arr.shape[1]
    )
    response = stub.Inference(request_data)

    return response.bbox_arr


if __name__ == "__main__":
    img_arr = cv2.imread("/", cv2.IMREAD_COLOR)
    grpc_call(img_arr)
