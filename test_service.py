import grpc

# import the generated classes
import service.service_spec.super_resolution_pb2_grpc as grpc_bt_grpc
import service.service_spec.super_resolution_pb2 as grpc_bt_pb2

from service import registry, base64_to_jpg

if __name__ == "__main__":

    try:
        # open a gRPC channel
        endpoint = "localhost:701z6"
        channel = grpc.insecure_channel("{}".format(endpoint))
        print("opened channel")

        grpc_method = "increase_image_resolution"

        input_image = \
            "https://www.gettyimages.ie/gi-resources/images/Homepage/Hero/UK/CMS_Creative_164657191_Kingfisher.jpg"
        model = "proSR"
        scale = 2

        if grpc_method == "increase_image_resolution":
            # create a stub (client)
            stub = grpc_bt_grpc.SuperResolutionStub(channel)
            # create a valid request message
            request = grpc_bt_pb2.SuperResolutionRequest(input=input_image,
                                                         scale=scale)
            # make the call
            response = stub.increase_image_resolution(request)

            # et voilà
            base64_to_jpg(response.data, "/Shared/super_resolution_test_output.jpg")
            print("Service completed!")
        else:
            print("Invalid method!")

    except Exception as e:
        print(e)
