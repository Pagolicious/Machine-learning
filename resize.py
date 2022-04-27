from PIL import Image
import os


def resize_decrease(in_folder, out_folder):
    for images in os.listdir(in_folder):

        if (images.endswith(".png") or images.endswith(".jpg")
                or images.endswith(".jpeg")):
            image_file = Image.open(os.path.join(in_folder, images))
            width = float(image_file.size[0])
            height = float(image_file.size[1])
            print(width, height)

            if width > height:
                new_width = 96
                new_height = new_width * height / width
                new_width_small = 24
                new_height_small = new_width_small * height / width

                image_file_lower = image_file.resize((new_width, int(new_height)))
                image_file_lower.save(f'{out_folder}/96x96-{images}')
                image_file_lowest = image_file.resize((new_width_small, int(new_height_small)))
                image_file_lowest.save(f'{out_folder}/24x24-{images}')


            else:
                new_height = 96
                new_width = new_height * width / height
                new_height_small = 24
                new_width_small = new_height_small * width / height

                image_file_lower = image_file.resize((int(new_width), new_height))
                image_file_lower.save(f'{out_folder}/96x96-{images}')
                image_file_lowest = image_file.resize((int(new_width_small), new_height_small))
                image_file_lowest.save(f'{out_folder}/24x24-{images}')
