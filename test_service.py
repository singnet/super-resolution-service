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
            "https://www.gettyimages.ie/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg"
        model = "ESRGAN"
        scale = 4

        # create a stub (client)
        stub = grpc_bt_grpc.SuperResolutionStub(channel)
        print("Stub created.")

        # create a valid request message
        request = grpc_bt_pb2.SuperResolutionRequest(input=input_image,
                                                     model=model,
                                                     scale=scale)
        # make the call
        response = stub.increase_image_resolution(request)
        print("First 100 characters of response: {}".format(response[:100]))

        # et voilà
        output_file_path = "./super_resolution_test_output.jpg"
        if response.data:
            base64_to_jpg(response.data, output_file_path)
            clear_file(output_file_path)
            print("Service completed!")
        else:
            print("Service failed! No data received.")
            exit(1)

    except Exception as e:
        print(e)
        exit(1)
