from tkinter.messagebox import showinfo

from PIL import Image
import os


def with_crop():
    from gui_class import SuperResolutionGuiClass
    uw = SuperResolutionGuiClass.uw

    # crop the largest size square
    def crop(img):
        width, height = img.size
        return img.crop(((width - min(img.size)) // 2, (height - min(img.size)) // 2,
                         (width + min(img.size)) // 2, (height + min(img.size)) // 2))

    try:
        path_to = uw.textbox1_var.get()
        save_path = uw.textbox3_var.get()
        height_option = uw.textbox4_var.get()
        width_option = uw.textbox5_var.get()
        uw.statusbar1['maximum'] = len(os.listdir(path_to))

        for images in os.listdir(path_to):
            if images.endswith((".png", ".jpg", ".jpeg")):
                image_hr = Image.open(os.path.join(path_to, images))

                if height_option and width_option:
                    image_hr = crop(image_hr).resize((int(width_option), int(height_option)))
                    image_lr = image_hr.copy().resize(
                        (round(int(width_option) / 4), round(int(height_option) / 4)))

                    if height_option == width_option:
                        fn, fext = os.path.splitext(images)
                        image_hr.save(f'{save_path}/%s_{width_option}%s' % (fn, fext))
                        image_lr.save(f'{save_path}/%s_{round(int(width_option) / 4)}%s' % (fn, fext))
                    else:
                        showinfo(message='Cropped images need to be same width and height')
                        break
                else:
                    image_hr = crop(image_hr).resize((96, 96))
                    image_lr = image_hr.copy().resize((24, 24))

                    fn, fext = os.path.splitext(images)
                    image_hr.save(f'{save_path}/%s_96%s' % (fn, fext))
                    image_lr.save(f'{save_path}/%s_24%s' % (fn, fext))

                uw.statusbar1['value'] += 1
                uw.statusbar1.update()
                uw.status_label1['text'] = "Status: {0:.0f}% Complete".format(
                    uw.statusbar1['value'] / len(os.listdir(path_to)) * 100)
            else:
                showinfo(message='Select a folder with images')
                break

        if uw.statusbar1['value'] == len(os.listdir(path_to)):
            showinfo(message='Dataset completed!')
        uw.statusbar1['value'] = 0
        uw.status_label1['text'] = "Status: "

    except WindowsError:
        showinfo(message='Insert a valid folder')


def without_crop():
    from gui_class import SuperResolutionGuiClass
    uw = SuperResolutionGuiClass.uw

    try:
        in_folder = uw.textbox1.get()
        out_folder = uw.textbox3.get()
        height_option = uw.textbox4_var.get()
        width_option = uw.textbox5_var.get()

        uw.statusbar1['maximum'] = len(os.listdir(in_folder))

        for images in os.listdir(in_folder):

            if (images.endswith(".png") or images.endswith(".jpg")
                    or images.endswith(".jpeg")):
                image_file = Image.open(os.path.join(in_folder, images))

                if height_option and width_option:

                    width = float(image_file.size[0])
                    height = float(image_file.size[1])

                    if width > height:
                        new_width = round(int(width_option))
                        new_height = new_width * height / width
                        new_width_small = round(int(width_option) / 4)
                        new_height_small = new_width_small * height / width

                        image_file_lower = image_file.resize((new_width, int(new_height)))
                        image_file_lower.save(f'{out_folder}/{new_width}x{round(new_height)}-{images}')
                        image_file_lowest = image_file.resize((new_width_small, int(new_height_small)))
                        image_file_lowest.save(
                            f'{out_folder}/{new_width_small}x{round(new_height_small)}-{images}')

                    else:
                        new_height = round(int(height_option))
                        new_width = new_height * width / height
                        new_height_small = round(int(height_option) / 4)
                        new_width_small = new_height_small * width / height

                        image_file_lower = image_file.resize((int(new_width), new_height))
                        image_file_lower.save(f'{out_folder}/{round(new_width)}x{new_height}-{images}')
                        image_file_lowest = image_file.resize((int(new_width_small), new_height_small))
                        image_file_lowest.save(
                            f'{out_folder}/{round(new_width_small)}x{new_height_small}-{images}')

                else:
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

                uw.statusbar1['value'] += 1
                uw.statusbar1.update()
                uw.status_label1['text'] = "Status: {0:.0f}% Complete".format(
                    uw.statusbar1['value'] / len(os.listdir(in_folder)) * 100)

        showinfo(message='Dataset completed!')
        uw.statusbar1['value'] = 0
        uw.status_label1['text'] = "Status: "

    except WindowsError:
        showinfo(message='Insert a valid folder')


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
