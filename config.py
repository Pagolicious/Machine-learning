import torch
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2

LOAD_MODEL = True
SAVE_MODEL = True
CHECKPOINT_GEN = "gen.pth.tar"
CHECKPOINT_DISC = "disc.pth.tar"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
LEARNING_RATE = 1e-4


# The load settings file function goes here:
def load_config_constant_values():
    with open("settings.txt", mode="r") as file:
        file_line = file.read()
        settings_item_list = file_line.split(",")

        # Unpack the setting items to the right owners:
        num_epochs, batch_size, num_workers, high_res = settings_item_list

        # convert the values to integers as we want them so.
        num_epochs = int(num_epochs)
        batch_size = int(batch_size)
        num_workers = int(num_workers)
        high_res = int(high_res)

    return num_epochs, batch_size, num_workers, high_res


# NUM_EPOCHS = 100
# BATCH_SIZE = 16
# NUM_WORKERS = 4
# HIGH_RES = 96
NUM_EPOCHS, BATCH_SIZE, NUM_WORKERS, HIGH_RES = load_config_constant_values()
LOW_RES = HIGH_RES // 4
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
        A.RandomCrop(width=HIGH_RES, height=HIGH_RES),
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
