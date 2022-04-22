from PIL import Image
import os


def resize_decrease():
    folder_dir = "C:/Users/Oscar/Desktop/PyCharm/super_resolution/images/original"
    for images in os.listdir(folder_dir):

        if (images.endswith(".png") or images.endswith(".jpg")
                or images.endswith(".jpeg")):
            image_file = Image.open(os.path.join(folder_dir, images))
            width = float(image_file.size[0])
            height = float(image_file.size[1])
            print(width, height)

            if width > height:
                new_width = 96
                new_height = new_width * height / width

                image_file_lower = image_file.resize((new_width, new_height))
                image_file_lower.save(f'C:/Users/Oscar/Desktop/PyCharm/super_resolution/images/resized/original/original-96x96-{images}')
                image_file_lowest = image_file.resize((24, 24))
                image_file_lowest.save(f'C:/Users/Oscar/Desktop/PyCharm/super_resolution/images/resized/original/original-24x24-{images}')

                #image_file.save(f'C:/Users/Oscar/Desktop/PyCharm/super_resolution/images/resized/decreased/{name}-800-600-25%.jpg', quality=25)

                #image_file.save(f'C:/Users/Oscar/Desktop/PyCharm/super_resolution/images/resized/decreased/{name}-800-600-1%.jpg', quality=1)
            else:
                new_height = 96
                new_width = new_height * width / height

                image_file_lower = image_file.resize((new_width, new_height))
                image_file_lower.save(f'C:/Users/Oscar/Desktop/PyCharm/super_resolution/images/resized/original/original-96x96-{images}')
                image_file_lowest = image_file.resize((24, 24))
                image_file_lowest.save(f'C:/Users/Oscar/Desktop/PyCharm/super_resolution/images/resized/original/original-24x24-{images}')


if __name__ == '__main__':
    resize_decrease()
