from PIL import Image
import os


def resize_decrease():
    name = 1
    folder_dir = "C:/Users/Oscar/Desktop/PyCharm/super_resolution/images/original"
    for images in os.listdir(folder_dir):

        if (images.endswith(".png") or images.endswith(".jpg")
                or images.endswith(".jpeg")):

            image_file = Image.open(os.path.join(folder_dir, images))
            image_file = image_file.resize((96, 96))
            image_file.save('C:/Users/Oscar/Desktop/PyCharm/super_resolution/images/resized/original/original-96x96.jpg')

            image_file.save(f'C:/Users/Oscar/Desktop/PyCharm/super_resolution/images/resized/decreased/{name}-800-600-25%.jpg', quality=25)

            image_file.save(f'C:/Users/Oscar/Desktop/PyCharm/super_resolution/images/resized/decreased/{name}-800-600-1%.jpg', quality=1)

            name += 1


if __name__ == '__main__':
    resize_decrease()
