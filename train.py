import sys

import torch
import config
from torch import nn
from torch import optim
import os
import shutil

from utils import load_checkpoint, save_checkpoint, plot_examples, plot_examples_flask
from loss import VGGLoss
from torch.utils.data import DataLoader
from model import Generator, Discriminator
from tqdm import tqdm
from dataset import MyImageFolder

torch.backends.cudnn.benchmark = True


def config_updater_function():
    source_path = (sys.path[0])
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


def config_updater_function_flask():
    the_num_epochs = 1
    the_batch_size = 1
    the_num_workers = 1
    the_high_res = 48
    the_training_choice = 1
    the_model_choice = 0

    return the_num_epochs, the_batch_size, the_num_workers, the_high_res, the_training_choice, the_model_choice


def check_path():
    from gui_class import SuperResolutionGuiClass
    uw = SuperResolutionGuiClass.uw
    global home_project_dir
    home_project_dir = os.getcwd()

    picture_path = check_pathways()

    if os.path.isdir(f"{os.curdir}/test_images/") is False:
        shutil.copytree(f"{uw.user_path_to_training_picture_folder}", f"{os.curdir}/test_images")

    if os.path.isdir(f"{os.curdir}/saved/") is False:
        path = os.path.join(os.curdir, "saved/")
        os.mkdir(path)

    os.chdir(home_project_dir)


def check_pathways():
    from gui_class import SuperResolutionGuiClass
    uw = SuperResolutionGuiClass.uw
    copy_of_path = uw.user_path_to_training_picture_folder
    os.chdir(copy_of_path)
    os.chdir("..")
    global picture_path
    picture_path = os.getcwd()
    return picture_path


def train_fn(loader, disc, gen, opt_gen, opt_disc, bce, vgg_loss):
    loop = tqdm(loader, leave=True)

    for idx, (low_res, high_res) in enumerate(loop):
        high_res = high_res.to(config.DEVICE)
        low_res = low_res.to(config.DEVICE)

        ### Train Discriminator: max log(D(x)) + log(1 - D(G(z)))
        fake = gen(low_res)
        disc_real = disc(high_res)
        disc_fake = disc(fake.detach())
        disc_loss_real = bce(
            disc_real, torch.ones_like(disc_real) - 0.1 * torch.rand_like(disc_real)
        )
        disc_loss_fake = bce(disc_fake, torch.zeros_like(disc_fake))
        loss_disc = disc_loss_fake + disc_loss_real

        opt_disc.zero_grad()
        loss_disc.backward()
        opt_disc.step()

        # Train Generator: min log(1 - D(G(z))) <-> max log(D(G(z))
        disc_fake = disc(fake)

        adversarial_loss = 1e-3 * bce(disc_fake, torch.ones_like(disc_fake))
        loss_for_vgg = 0.006 * vgg_loss(fake, high_res)
        gen_loss = loss_for_vgg + adversarial_loss

        opt_gen.zero_grad()
        gen_loss.backward()
        opt_gen.step()

        if idx % 200 == 0:
            plot_examples("test_images/", gen)


def train_fn2(loader, gen, opt_gen, mse):
    loop = tqdm(loader, leave=True)

    for idx, (low_res, high_res) in enumerate(loop):
        high_res = high_res.to(config.DEVICE)
        low_res = low_res.to(config.DEVICE)

        fake = gen(low_res)

        l2_loss = mse(fake, high_res)

        gen_loss = l2_loss

        opt_gen.zero_grad()
        gen_loss.backward()
        opt_gen.step()

        if idx % 200 == 0:
            from gui_class import SuperResolutionGuiClass
            uw = SuperResolutionGuiClass.uw

            plot_examples(picture_path + "/test_images/", gen)


def train_fn_flask(loader, gen, opt_gen, mse):
    loop = tqdm(loader, leave=True)

    for idx, (low_res, high_res) in enumerate(loop):
        high_res = high_res.to(config.DEVICE)
        low_res = low_res.to(config.DEVICE)

        fake = gen(low_res)

        l2_loss = mse(fake, high_res)

        gen_loss = l2_loss

        opt_gen.zero_grad()
        gen_loss.backward()
        opt_gen.step()

        if idx % 200 == 0:
            plot_examples_flask(f'{(sys.path[1])}/app/static/test_images/', gen)


def main():
    the_num_epochs, the_batch_size, the_num_workers, the_high_res, the_training_choice, \
    the_model_choice = config_updater_function()

    from gui_class import SuperResolutionGuiClass
    uw = SuperResolutionGuiClass.uw
    uw.statusbar2['value'] = 0
    uw.status_label2['text'] = "Status: "
    uw.statusbar2.update()
    uw.status_label2['text'] = "Status: {0:.0f}% Complete".format(
        uw.statusbar2['value'] / the_num_epochs * 100)

    print(f'Number of epochs selected: {the_num_epochs}')
    print(f'Selected Batch Size: {the_batch_size}')
    print(f'Number of Workers selected: {the_num_workers}')
    print(f'Selected Highres: {the_high_res}')
    print(f'Selected Training: {the_training_choice}')
    check_path()
    dataset = MyImageFolder(root_dir=uw.user_path_to_training_picture_folder)  # root_dir="images/")
    loader = DataLoader(
        dataset,
        batch_size=the_batch_size,
        shuffle=True,
        pin_memory=True,
        num_workers=the_num_workers,
    )
    gen = Generator(in_channels=3).to(config.DEVICE)
    disc = Discriminator(in_channels=3).to(config.DEVICE)
    opt_gen = optim.Adam(gen.parameters(), lr=config.LEARNING_RATE, betas=(0.9, 0.999))
    opt_disc = optim.Adam(disc.parameters(), lr=config.LEARNING_RATE, betas=(0.9, 0.999))
    mse = nn.MSELoss()
    bce = nn.BCEWithLogitsLoss()
    vgg_loss = VGGLoss()

    if the_model_choice == 0:
        load_checkpoint(
            config.CHECKPOINT_GEN,
            gen,
            opt_gen,
            config.LEARNING_RATE,
        )
        load_checkpoint(
            config.CHECKPOINT_DISC, disc, opt_disc, config.LEARNING_RATE,
        )

    for epoch in range(the_num_epochs):
        uw.statusbar2['maximum'] = the_num_epochs
        if config.DEVICE == "cuda":
            # Empty the cache memory in the cuda before we do next iteration.
            torch.cuda.empty_cache()
            torch.cuda.memory_summary(device=config.DEVICE, abbreviated=True)
            # print("Empty cache memory")

        print(f' Epoch number: {epoch} with Device: {config.DEVICE}')

        # Do a check what kind of training the user want to do,
        # 0 = loss for vgg + adversarial loss
        # 1 = L2 loss

        if the_training_choice == 0:

            print(f'Training with: Loss for vgg + adversarial loss:')
            print()
            train_fn(loader, disc, gen, opt_gen, opt_disc, mse, bce, vgg_loss)

        else:

            print(f'Training with L2 loss:')
            print()
            train_fn2(loader, disc, gen, opt_gen, opt_disc, mse, bce, vgg_loss)

        uw.statusbar2['value'] += 1
        uw.statusbar2.update()
        uw.status_label2['text'] = "Status: {0:.0f}% Complete".format(
            uw.statusbar2['value'] / the_num_epochs * 100)
        uw.status_label2.update()

        if the_model_choice == 1:
            save_checkpoint(gen, opt_gen, filename=config.CHECKPOINT_GEN)
            save_checkpoint(disc, opt_disc, filename=config.CHECKPOINT_DISC)


def main_flask():

    the_num_epochs, the_batch_size, the_num_workers, the_high_res, the_training_choice, \
    the_model_choice = config_updater_function_flask()

    dataset = MyImageFolder(root_dir=f'{(sys.path[1])}/app/static/files/images/')
    loader = DataLoader(
        dataset,
        batch_size=the_batch_size,
        shuffle=True,
        pin_memory=True,
        num_workers=the_num_workers,
    )
    gen = Generator(in_channels=3).to(config.DEVICE)
    disc = Discriminator(in_channels=3).to(config.DEVICE)
    opt_gen = optim.Adam(gen.parameters(), lr=config.LEARNING_RATE, betas=(0.9, 0.999))
    opt_disc = optim.Adam(disc.parameters(), lr=config.LEARNING_RATE, betas=(0.9, 0.999))
    mse = nn.MSELoss()
    bce = nn.BCEWithLogitsLoss()
    vgg_loss = VGGLoss()

    if the_model_choice == 0:
        load_checkpoint(
            config.CHECKPOINT_GEN,
            gen,
            opt_gen,
            config.LEARNING_RATE,
        )
        load_checkpoint(
            config.CHECKPOINT_DISC, disc, opt_disc, config.LEARNING_RATE,
        )

    for epoch in range(the_num_epochs):
        if config.DEVICE == "cuda":
            torch.cuda.empty_cache()
            torch.cuda.memory_summary(device=config.DEVICE, abbreviated=True)

        print(f' Epoch number: {epoch} with Device: {config.DEVICE}')

        if the_training_choice == 0:

            print(f'Training with: Loss for vgg + adversarial loss:')
            print()
            train_fn(loader, disc, gen, opt_gen, opt_disc, mse, bce, vgg_loss)

        else:

            print(f'Training with L2 loss:')
            print()
            train_fn_flask(loader, disc, gen, opt_gen, opt_disc, mse, bce, vgg_loss)

        if the_model_choice == 1:
            save_checkpoint(gen, opt_gen, filename=config.CHECKPOINT_GEN)
            save_checkpoint(disc, opt_disc, filename=config.CHECKPOINT_DISC)

    return print('Super Resolution picture done')


if __name__ == "__main__":
    main()
