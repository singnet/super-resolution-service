import grpc

# import the generated classes
import service.service_spec.super_resolution_pb2_grpc as grpc_bt_grpc
import service.service_spec.super_resolution_pb2 as grpc_bt_pb2

from service import registry, base64_to_jpg, clear_file

if __name__ == "__main__":

    try:
        # open a gRPC channel
        endpoint = "localhost:{}".format(registry["super_resolution_service"]["grpc"])
        channel = grpc.insecure_channel("{}".format(endpoint))
        print("Opened channel")

        # setting parameters
        grpc_method = "increase_image_resolution"
        input_image = \
            "http://d3sdoylwcs36el.cloudfront.net/VEN-virtual-enterprise-network-business-opportunities-small-fish_id799929_size485.jpg"
        model = "proSR"
        scale = 2

        # create a stub (client)
        stub = grpc_bt_grpc.SuperResolutionStub(channel)
        print("Stub created.")

        # create a valid request message
        request = grpc_bt_pb2.SuperResolutionRequest(input=input_image,
                                                     model=model,
                                                     scale=scale)
        # make the call
        response = stub.increase_image_resolution(request)
        print("Response received: {}".format(response))

        # et voilà
        output_file_path = "./super_resolution_test_output.jpg"
        if response.data:
            base64_to_jpg(response.data, output_file_path)
            clear_file(output_file_path)
            print("Service completed!")
        else:
            print("Service failed! No data received.")

    except Exception as e:
        print(e)
        exit(1)
