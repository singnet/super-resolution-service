import logging
import grpc
import service.serviceUtils
import service.service_spec.super_resolution_pb2_grpc as grpc_bt_grpc
from service.service_spec.super_resolution_pb2 import Image
import subprocess
import concurrent.futures as futures
import sys
import os
from urllib.error import HTTPError

logging.basicConfig(
    level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s"
)
log = logging.getLogger("super_resolution_service")


class SuperResolutionServicer(grpc_bt_grpc.SuperResolutionServicer):
    """Super resolution servicer class to be added to the gRPC stub.
    Derived from protobuf (auto-generated) class."""

    def __init__(self):
        log.debug("SuperResolutionServicer created!")
        
        self.result = Image()

        self.root_path = os.getcwd()
        self.input_dir = self.root_path + "/service/temp/input"
        self.output_dir = self.root_path + "/service/temp/output"
        service.initialize_diretories([self.input_dir, self.output_dir])

        self.model_dir = self.root_path + "/service/models"
        self.prosr_model = "/proSR/proSR_x"
        self.prosrgan_model = "/proSRGAN/proSRGAN_x"
        self.scale_dict = {"proSR": [2, 4, 8],
                           "proSRGAN": [4, 8]}
        self.model_suffix = ".pth"
        if not os.path.exists(self.model_dir):
            log.error("Models folder ({}) not found. Please run download_models.sh.".format(self.model_dir))
            return

    def treat_inputs(self, base_command, request, arguments, created_images):
        """Treats gRPC inputs and assembles lua command. Specifically, checks if required field have been specified,
        if the values and types are correct and, for each input/input_type adds the argument to the lua command."""

        model_path = self.model_dir
        # Base command is the prefix of the command (e.g.: 'th test.lua ')
        file_index_str = ""
        command = base_command
        for field, values in arguments.items():
            # var_type = values[0]
            # required = values[1] Not being used now but required for future automation steps
            default = values[2]

            # Tries to retrieve argument from gRPC request
            try:
                arg_value = eval("request.{}".format(field))
            except Exception as e:  # AttributeError if trying to access a field that hasn't been specified.
                log.error(e)
                return False

            print("Received request.{} = ".format(field))
            print(arg_value)

            # Deals with each field (or field type) separately. This is very specific to the lua command required.
            if field == "input":
                assert(request.input != ""), "Input image field should not be empty."
                try:
                    image_path, file_index_str = \
                        service.serviceUtils.treat_image_input(arg_value, self.input_dir, "{}".format(field))
                    print("Image path: {}".format(image_path))
                    created_images.append(image_path)
                    command += "--{} {} ".format(field, image_path)
                except Exception as e:
                    log.error(e)
                    raise
            elif field == "model":
                if request.model == "proSR":
                    model_path += self.prosr_model
                elif request.model == "proSRGAN":
                    model_path += self.prosrgan_model
                else:
                    log.error("Input field model not recognized. Should be either \"proSR\" or \"proSRGAN\". Got: {}"
                              .format(request.model))
            elif field == "scale":
                # If empty, fill with default, else check if valid
                if request.scale == 0 or request.scale == "":
                    scale = default
                else:
                    try:
                        scale = int(request.scale)
                    except Exception as e:
                        log.error(e)
                        raise
                if scale not in self.scale_dict[request.model]:
                    log.error('Scale invalid. Should be one of {}.'.format(self.scale_dict[request.model]))
                str_scale = str(scale)
                model_path += str_scale + self.model_suffix
                command += "--checkpoint {} --{} {} ".format(model_path, field, str_scale)
            else:
                log.error("Command assembly error. Request field not found.")
                return False

        return command, file_index_str

    def increase_image_resolution(self, request, context):
        """Increases the resolution of a given image (request.image) """

        # Store the names of the images to delete them afterwards
        created_images = []

        # Python command call arguments. Key = argument name, value = tuple(type, required?, default_value)
        arguments = {"input": ("image", True, None),
                     "model": ("string", True, None),
                     "scale": ("int", False, 2)}

        # Treat inputs and assemble command
        base_command = "python3.6 ./service/increase_resolution.py "
        try:
            command, file_index_str = self.treat_inputs(base_command, request, arguments, created_images)
        except HTTPError as e:
            error_message = "Error downloading the input image \n" + e.read()
            log.error(error_message)
            self.result.data = error_message
            return self.result
        except Exception as e:
            log.error(e)
            self.result.data = e
            return self.result
        command += "--{} {}".format("output", self.output_dir)  # pre-defined for the service

        log.debug("Python command generated: {}".format(command))

        # Call super resolution. If it fails, log error, delete files and exit.
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = process.communicate()
        except Exception as e:
            self.result.data = e
            log.debug("Returning on exception!")
            log.error(e)
            for image in created_images:
                service.clear_file(image)
            return self.result

        # if stderr:
        #     log.debug("Returning on stderr!")
        #     log.error(stderr)
        #     self.result.data = stderr
        #     for image in created_images:
        #         service.clear_file(image)
        #     return self.result

        # Get output file path
        log.debug("Returning on service complete!")
        input_filename = os.path.split(created_images[0])[1]
        log.debug("Input file name: {}".format(input_filename))
        output_image_path = self.output_dir + '/' + input_filename
        log.debug("Output image path: {}".format(output_image_path))
        created_images.append(output_image_path)

        # Prepare gRPC output message
        self.result = Image()
        self.result.data = service.serviceUtils.jpg_to_base64(output_image_path, open_file=True).decode("utf-8")
        log.debug("Output image generated. Service successfully completed.")

        for image in created_images:
            service.serviceUtils.clear_file(image)

        return self.result


def serve(max_workers=5, port=7777):
    """The gRPC serve function.

    Params:
    max_workers: pool of threads to execute calls asynchronously
    port: gRPC server port

    Add all your classes to the server here.
    (from generated .py files by protobuf compiler)"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_SuperResolutionServicer_to_server(
        SuperResolutionServicer(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    return server


if __name__ == '__main__':
    """Runs the gRPC server to communicate with the Snet Daemon."""
    parser = service.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    service.serviceUtils.main_loop(serve, args)
