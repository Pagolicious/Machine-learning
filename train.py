import torch
import config
from torch import nn
from torch import optim

# import gui_class

from utils import load_checkpoint, save_checkpoint, plot_examples
from loss import VGGLoss
from torch.utils.data import DataLoader
from model import Generator, Discriminator
from tqdm import tqdm
from dataset import MyImageFolder
# from uw_module import *

torch.backends.cudnn.benchmark = True
config.load_config_constant_values()


# gui_class.SuperResolutionGuiClass.statusbar2['maximum'] = config.NUM_EPOCHS

def train_fn(loader, disc, gen, opt_gen, opt_disc, mse, bce, vgg_loss):
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
        # l2_loss = mse(fake, high_res)
        adversarial_loss = 1e-3 * bce(disc_fake, torch.ones_like(disc_fake))
        loss_for_vgg = 0.006 * vgg_loss(fake, high_res)
        gen_loss = loss_for_vgg + adversarial_loss

        opt_gen.zero_grad()
        gen_loss.backward()
        opt_gen.step()

        if idx % 200 == 0:
            plot_examples("test_images/", gen)


def main():
    dataset = MyImageFolder(root_dir="images/")
    loader = DataLoader(
        dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        pin_memory=True,
        num_workers=config.NUM_WORKERS,
    )
    gen = Generator(in_channels=3).to(config.DEVICE)
    disc = Discriminator(in_channels=3).to(config.DEVICE)
    opt_gen = optim.Adam(gen.parameters(), lr=config.LEARNING_RATE, betas=(0.9, 0.999))
    opt_disc = optim.Adam(disc.parameters(), lr=config.LEARNING_RATE, betas=(0.9, 0.999))
    mse = nn.MSELoss()
    bce = nn.BCEWithLogitsLoss()
    vgg_loss = VGGLoss()

    if config.LOAD_MODEL:
        load_checkpoint(
            config.CHECKPOINT_GEN,
            gen,
            opt_gen,
            config.LEARNING_RATE,
        )
        load_checkpoint(
            config.CHECKPOINT_DISC, disc, opt_disc, config.LEARNING_RATE,
        )

        # Making a local import to avoid circular import error.
    from gui_class import SuperResolutionGuiClass
    uw = SuperResolutionGuiClass.uw

    for epoch in range(config.NUM_EPOCHS):
        uw.statusbar2['maximum'] = config.NUM_EPOCHS
        if config.DEVICE == "cuda":

            # Empty the cache memory in the cuda before we do next iteration.
            torch.cuda.empty_cache()
            torch.cuda.memory_summary(device=config.DEVICE, abbreviated=True)
            print("Empty cache memory")

        # Tell the user what epoch we are on.
        print(f' Epoch number: {epoch} with Device: {config.DEVICE}')

        train_fn(loader, disc, gen, opt_gen, opt_disc, mse, bce, vgg_loss)

        uw.statusbar2['value'] += 1
        uw.statusbar2.update()
        uw.status_label2['text'] = "Status: {0:.0f}% Complete".format(
            uw.statusbar2['value'] / config.NUM_EPOCHS * 100)

        if config.SAVE_MODEL:
            save_checkpoint(gen, opt_gen, filename=config.CHECKPOINT_GEN)
            save_checkpoint(disc, opt_disc, filename=config.CHECKPOINT_DISC)


if __name__ == "__main__":
    main()
