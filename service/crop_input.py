from PIL import Image

# INPUTS: Number of output images
input_image = "../data/dog_640_512.jpg"
output_path = "./cropped_data"

# Get input image info
image = Image.open(input_image)
width, height = image.size

# Define stride and window size
window_size = 200
stride = 20

# Steps list
width_list = range(0, width-window_size-stride, stride)
height_list = range(0, height-window_size-stride, stride)

index = 0

for h in height_list:
    for w in width_list:
        while True:
            save_path = output_path+'/'+str(index).zfill(3)+".jpg"
            box = (w, h, w + window_size, h + window_size)
            image.crop(box).save(save_path)
            index += 1
            try:
                Image.open(save_path)
            except Exception as e:
                print(e)
                continue
            break
