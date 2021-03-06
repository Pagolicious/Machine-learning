import torch
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
import sys

source_path = (sys.path[0])
LOAD_MODEL = True
SAVE_MODEL = True
CHECKPOINT_GEN = source_path + "/gen.pth.tar"
CHECKPOINT_DISC = source_path + "/disc.pth.tar"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
LEARNING_RATE = 1e-4


# The load settings file function goes here:
def load_config_constant_values():
    source_path = (sys.path[1])  # If using flask, set path to (sys.path[1]). If GUI use (sys.path[0])
    with open(source_path + "/settings.txt", mode="r") as file:
        settings_item_listsettings_item_list = ""
        file_line = file.read()
        settings_item_list = file_line.split(",")

        # Unpack the setting items to the right owners:
        the_num_epochs, the_batch_size, the_num_workers, the_high_res, the_training_choice, \
        the_model_choice = settings_item_list

        # convert the values to integers as we want them so.
        the_num_epochs = int(the_num_epochs)
        the_batch_size = int(the_batch_size)
        the_num_workers = int(the_num_workers)
        the_high_res = int(the_high_res)
        the_training_choice = int(the_training_choice)
        the_model_choice = int(the_model_choice)

    return the_num_epochs, the_batch_size, the_num_workers, the_high_res, the_training_choice, the_model_choice


num_epochs, batch_size, num_workers, high_res, training_choice, the_model_choice = load_config_constant_values()


LOW_RES = high_res // 4
IMG_CHANNELS = 3

highres_transform = A.Compose(
    [
        A.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
        ToTensorV2(),
    ]
)

lowres_transform = A.Compose(
    [
        A.Resize(width=LOW_RES, height=LOW_RES, interpolation=Image.BICUBIC),
        A.Normalize(mean=[0, 0, 0], std=[1, 1, 1]),
        ToTensorV2(),
    ]
)

both_transforms = A.Compose(
    [
        A.RandomCrop(width=high_res, height=high_res),
        A.HorizontalFlip(p=0.5),
        A.RandomRotate90(p=0.5),
    ]
)

test_transform = A.Compose(
    [
        A.Normalize(mean=[0, 0, 0], std=[1, 1, 1]),
        ToTensorV2(),
    ]
)
