import sys
import os
import time
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import filedialog as fd, filedialog
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
import config
import train
from resize import resize_decrease

"""
*******************************************************************************************
2022-04-21 Super Resolution Gui Class.
This class is written to handle all the gui things we need to present to the screen
it should also handle all the functions and actions then pressing buttons etc. 
********************************************************************************************
"""


class SuperResolutionGuiClass:
    uw = None

    def __init__(self, user_window):
        self.window = user_window
        self.window.title('Super Resolution Application Dark Mode')
        self.window.geometry('1764x968+71+7')
        self.window.resizable(False, False)
        self.choice = tk.IntVar()
        self.choice2 = tk.IntVar()
        SuperResolutionGuiClass.uw = self

        # Add the functions here before the gui part starts.

        def with_crop():
            # crop the largest size square
            def crop(img):
                width, height = img.size
                return img.crop(((width - min(img.size)) // 2, (height - min(img.size)) // 2,
                                 (width + min(img.size)) // 2, (height + min(img.size)) // 2))

            try:
                path_to = self.textbox1_var.get()
                save_path = self.textbox3_var.get()
                height_option = self.textbox4_var.get()
                width_option = self.textbox5_var.get()
                self.statusbar1['maximum'] = len(os.listdir(path_to))

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

                        self.statusbar1['value'] += 1
                        self.statusbar1.update()
                        self.status_label1['text'] = "Status: {0:.0f}% Complete".format(
                            self.statusbar1['value'] / len(os.listdir(path_to)) * 100)
                    else:
                        showinfo(message='Select a folder with images')
                        break

                if self.statusbar1['value'] == len(os.listdir(path_to)):
                    showinfo(message='Dataset completed!')
                self.statusbar1['value'] = 0
                self.status_label1['text'] = "Status: "

            except WindowsError:
                showinfo(message='Insert a valid folder')

        def without_crop():

            try:
                in_folder = self.textbox1.get()
                out_folder = self.textbox3.get()
                height_option = self.textbox4_var.get()
                width_option = self.textbox5_var.get()
                # resize_decrease(in_folder, out_folder)
                self.statusbar1['maximum'] = len(os.listdir(in_folder))

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

                        self.statusbar1['value'] += 1
                        self.statusbar1.update()
                        self.status_label1['text'] = "Status: {0:.0f}% Complete".format(
                            self.statusbar1['value'] / len(os.listdir(in_folder)) * 100)

                showinfo(message='Dataset completed!')
                self.statusbar1['value'] = 0
                self.status_label1['text'] = "Status: "

            except WindowsError:
                showinfo(message='Insert a valid folder')

        def training_the_model():

            # Call the training function, from the train.py file.
            train.main()

        def create_super_resolution_photo():
            print("Im the function that should take care of the Super Resolution Photo process. :)")

        def selected_option():
            print(f'You selected option: {str(self.choice.get())}')

            option = self.choice.get()

            if option == 0:
                with_crop()
            elif option == 1:
                without_crop()
            else:
                showinfo(message='Select a dataset option')

        def get_user_path_to_picture_folder():
            self.textbox1.delete(0, 'end')
            user_path_picture_folder = fd.askdirectory(parent=self.window, initialdir='/',
                                                       title='Please select a directory')
            self.textbox1.insert(0, user_path_picture_folder)

        def store_user_path_to_save_picture_folder():
            self.textbox3.delete(0, 'end')
            user_path_to_save_picture_folder = fd.askdirectory(parent=self.window, initialdir='/',
                                                               title='Please select where to save your pictures')
            self.textbox3.insert(0, user_path_to_save_picture_folder)

        def config_settings_window():
            self.settings_window = tk.Toplevel(self.window)
            self.settings_window_height = 600
            self.settings_window_width = 600

            # Try to center the new window.
            screen_width = self.settings_window.winfo_screenwidth()
            screen_height = self.settings_window.winfo_screenheight()
            self.settings_window_x_cord = int((screen_width / 2) - (self.settings_window_width / 2))
            self.settings_window_y_cord = int((screen_height / 2) - (self.settings_window_height / 2))
            self.settings_window.geometry("{}x{}+{}+{}".format(self.settings_window_width, self.settings_window_height,
                                                               self.settings_window_x_cord,
                                                               self.settings_window_y_cord))
            self.settings_window.title('Train Config Window')
            self.settings_window.resizable(False, False)

            # Add the controls to the new window.

            # 1) adding a frame to the settings_window
            self.settings_window_frame = tk.Frame(self.settings_window)
            self.settings_window_frame.place(relx=0.01, rely=0.02, relheight=0.950, relwidth=0.980)
            self.settings_window_frame.configure(relief='ridge')
            self.settings_window_frame.configure(borderwidth="2")
            self.settings_window_frame.configure(background="black")

            # 2) Now place the inside frame with the nice purple look.
            self.inside_frame = tk.Frame(self.settings_window)
            self.inside_frame.place(relx=0.02, rely=0.04, relheight=0.918, relwidth=0.960)
            self.inside_frame.configure(relief='ridge')
            self.inside_frame.configure(borderwidth="2")
            self.inside_frame.configure(background="#330066")

            # 3) Add the labels we,are going to need.
            self.number_of_epoch_label = tk.Label(self.settings_window)
            self.number_of_epoch_label.place(relx=0.24, rely=0.20, height=31, width=290, bordermode='ignore')
            self.number_of_epoch_label.configure(background="#330066")
            self.number_of_epoch_label.configure(anchor='w')
            self.number_of_epoch_label.configure(compound='left')
            self.number_of_epoch_label.configure(font="-family {Verdana} -size 12")
            self.number_of_epoch_label.configure(foreground="white")
            self.number_of_epoch_label.configure(text='Set the number of training epochs:')

            # 4) Add the textbox to hold the number of epochs the user enter.
            self.number_of_epoch_textbox_var = tk.StringVar()
            self.number_of_epoch_textbox = tk.Entry(self.settings_window, textvariable=self.number_of_epoch_textbox_var)
            self.number_of_epoch_textbox.place(relx=0.25, rely=0.25, height=20, relwidth=0.470, bordermode='ignore')

            # 5) Add the Batch size label:
            self.batch_size_label = tk.Label(self.settings_window)
            self.batch_size_label.place(relx=0.25, rely=0.30, height=31, width=290, bordermode='ignore')
            self.batch_size_label.configure(background="#330066")
            self.batch_size_label.configure(anchor='w')
            self.batch_size_label.configure(compound='left')
            self.batch_size_label.configure(font="-family {Verdana} -size 12")
            self.batch_size_label.configure(foreground="white")
            self.batch_size_label.configure(text='Set Batch Size:')

            # 6) Add Batch Size textbox:
            self.batch_size_textbox_var = tk.StringVar()
            self.batch_size_textbox = tk.Entry(self.settings_window, textvariable=self.batch_size_textbox_var)
            self.batch_size_textbox.place(relx=0.25, rely=0.35, height=20, relwidth=0.470, bordermode='ignore')

            # 7) Add the Number of workers label:
            self.number_of_workers_label = tk.Label(self.settings_window)
            self.number_of_workers_label.place(relx=0.25, rely=0.40, height=31, width=290, bordermode='ignore')
            self.number_of_workers_label.configure(background="#330066")
            self.number_of_workers_label.configure(anchor='w')
            self.number_of_workers_label.configure(compound='left')
            self.number_of_workers_label.configure(font="-family {Verdana} -size 12")
            self.number_of_workers_label.configure(foreground="white")
            self.number_of_workers_label.configure(text='Set Number Of Workers:')

            # 8) Add the number of workers textbox:
            self.number_of_workers_textbox_var = tk.StringVar()
            self.number_of_workers_textbox = tk.Entry(self.settings_window,
                                                      textvariable=self.number_of_workers_textbox_var)
            self.number_of_workers_textbox.place(relx=0.25, rely=0.45, height=20, relwidth=0.470, bordermode='ignore')

            # 9) Add the set high_res label:
            self.set_high_res_label = tk.Label(self.settings_window)
            self.set_high_res_label.place(relx=0.25, rely=0.50, height=31, width=290, bordermode='ignore')
            self.set_high_res_label.configure(background="#330066")
            self.set_high_res_label.configure(anchor='w')
            self.set_high_res_label.configure(compound='left')
            self.set_high_res_label.configure(font="-family {Verdana} -size 12")
            self.set_high_res_label.configure(foreground="white")
            self.set_high_res_label.configure(text='Set High Res:')

            # 10) Add the set Highres textbox.
            self.set_high_res_textbox_var = tk.StringVar()
            self.set_high_res_textbox = tk.Entry(self.settings_window,
                                                 textvariable=self.set_high_res_textbox_var)
            self.set_high_res_textbox.place(relx=0.25, rely=0.55, height=20, relwidth=0.470, bordermode='ignore')

            # 11) Add the Save And Exit Button.
            self.btn_save_and_exit_config = tk.Button(self.settings_window)
            self.btn_save_and_exit_config.place(relx=0.25, rely=0.82, height=34, width=283, bordermode='ignore')
            self.btn_save_and_exit_config.configure(compound='left')
            self.btn_save_and_exit_config.configure(font="-family {Verdana} -size 10 -weight bold")
            self.btn_save_and_exit_config.configure(background="white")  # d9d9d9
            self.btn_save_and_exit_config.configure(text='Save And Exit Config Settings:')

            # Adding 2 option buttons to make the training choice how you want to train
            # Either with l2 loss, or VGGLoss + adversarial_loss

            self.style = ttk.Style()
            self.style.map('TRadiobutton', background=[('selected', '#330066'), ('active', '#330066')])
            self.style.configure('.', background='#330066')
            self.style.configure('.', foreground='white')
            self.style.configure('.', font="-family {Verdana} -size 10 -weight bold")

            # Loss for vgg + adversarial_loss
            self.radiobutton3 = ttk.Radiobutton(self.settings_window, text="Option 3",
                                                variable=self.choice2,
                                                value=0)
            self.radiobutton3.place(relx=0.25, rely=0.62, relwidth=0.450, relheight=0.040, height=21)
            self.radiobutton3.configure(compound='left')
            self.radiobutton3.configure(text='Loss for vgg + adversarial_loss')

            # L2 Loss option goes here:
            self.radiobutton4 = ttk.Radiobutton(self.settings_window, text="Option 4",
                                                variable=self.choice2,
                                                value=1)
            self.radiobutton4.place(relx=0.25, rely=0.67, relwidth=0.450, relheight=0.049, height=21)
            self.radiobutton4.configure(compound='left')
            self.radiobutton4.configure(text='L2 Loss')


            # Collect the settings the user entered.
            # sv = save variable
            sv1 = self.number_of_epoch_textbox_var
            sv2 = self.batch_size_textbox_var
            sv3 = self.number_of_workers_textbox_var
            sv4 = self.set_high_res_textbox_var
            sv5 = self.choice2

            self.btn_save_and_exit_config.configure(
                command=lambda: save_settings(self.settings_window, sv1, sv2, sv3, sv4, sv5))

        def save_settings(x, sv1, sv2, sv3, sv4, sv5):
            self.settings_window = x

            # Do some validation and error handling.
            # Make sure the user enters only numbers and not any empty boxes.
            try:

                self.sv1_num_epoch = int(sv1.get())
                self.sv2_batch_size = int(sv2.get())
                self.sv3_num_workers = int(sv3.get())
                self.sv4_set_high_res = int(sv4.get())
                self.sv5 = int(sv5.get())

            except ValueError:
                tkinter.messagebox.showerror("Error:", "Most only have numbers:")

            # Do a check so the boxes is not contains the value 0
            # if there is 0 il reset it to the standard paper value.
            # unsure about the workers tho , maybe you want train with 0 workers in som rare occasions ?
            # But if that´s the case we just erase the num worker check in a later issue card.

            if self.sv1_num_epoch == 0:
                self.sv1_num_epoch = 100
            if self.sv2_batch_size == 0:
                self.sv2_batch_size = 16
            if self.sv3_num_workers == 0:
                self.sv3_num_workers = 4
            if self.sv4_set_high_res == 0:
                self.sv4_set_high_res = 96

            # Save routine goes here:

            with open("settings.txt", mode="w") as file:
                try:
                    file.write(
                        f'{self.sv1_num_epoch},{self.sv2_batch_size},{self.sv3_num_workers},{self.sv4_set_high_res},'
                        f'{self.sv5}')

                    # Extra protection is good :) even it´s a context manager.
                    file.close()

                except IOError:
                    tkinter.messagebox.showerror("Error:", "Something went wrong with saving file:")

            tkinter.messagebox.showinfo("Information:", "Saved the settings.")

            # this should come last, because this removes the window.
            self.settings_window.destroy()

        """ 
        *   Some notes and explanation of the commands of a frame object.
        *************************************************************************************************************
        *   relx is the variable to adjust the frame left to right.                                                 *
        *   rely is the variable to adjust the frame up and down.                                                   *
        *   relheight is the variable to adjust the height of the frame                                             *
        *   relwidth is the variable to adjust the width of the frame                                               *
        *   The relief style of a widget refers to certain simulated 3-D effects around the outside of the widget   *
        *   borderwidth: It will represent the size of the border around the label                                  *
        *   background: tells what background color the frame should have.                                          *
        *************************************************************************************************************
        """

        # Placing the main frame on the window.
        self.main_frame = tk.Frame(self.window)

        self.main_frame.place(relx=0.01, rely=0.02, relheight=0.954, relwidth=0.980)
        self.main_frame.configure(relief='ridge')
        self.main_frame.configure(borderwidth="2")
        self.main_frame.configure(background="black")

        # Next up is a frame on the main frame. but on the top.
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.place(relx=0.0, rely=0.0, relheight=0.154, relwidth=1.000)
        self.top_frame.configure(relief='groove')
        self.top_frame.configure(borderwidth="2")
        self.top_frame.configure(background="#330066")

        # Next thing I want to do is to place the logo, inside the frame.
        self.logo_label = tk.Label(self.main_frame)
        self.logo_label.place(relx=0.354, rely=0.033, height=60, width=650)
        self.logo_label.configure(background="#330066")
        self.logo_label.configure(foreground="white")
        self.logo_label.configure(anchor='w')
        self.logo_label.configure(compound='left')
        self.logo_label.configure(font="-family {Verdana} -size 36 -weight bold")
        self.logo_label.configure(text='Super Resolution')

        # Now I have to place the first labelframe and place text boxes and buttons inside it.
        self.label_frame_create_own_dataset = tk.LabelFrame(self.main_frame)
        self.label_frame_create_own_dataset.place(relx=0.000, rely=0.17, relheight=0.392, relwidth=0.323)
        self.label_frame_create_own_dataset.configure(relief='groove')
        self.label_frame_create_own_dataset.configure(font="-family {Verdana} -size 14")
        self.label_frame_create_own_dataset.configure(foreground="white")
        self.label_frame_create_own_dataset.configure(highlightcolor="white")
        self.label_frame_create_own_dataset.configure(text='Create own dataset:')
        self.label_frame_create_own_dataset.configure(background="#330066")  # 6600CC

        # Place the button inside the label_frame_create_own_dataset
        self.btn_create_dataset = tk.Button(self.label_frame_create_own_dataset)
        self.btn_create_dataset.place(relx=0.018, rely=0.752, height=34, width=537, bordermode='ignore')
        self.btn_create_dataset.configure(compound='left')
        self.btn_create_dataset.configure(font="-family {Verdana} -size 10 -weight bold")
        self.btn_create_dataset.configure(background="white")  # d9d9d9
        self.btn_create_dataset.configure(text='Create dataset')
        self.btn_create_dataset.configure(command=lambda: selected_option())

        # Placing a filedialog button to the path of your pictures.
        self.btn_file_dialog_path_to_your_pictures = tk.Button(self.label_frame_create_own_dataset)
        self.btn_file_dialog_path_to_your_pictures.place(relx=0.018, rely=0.260, height=24, relwidth=0.378,
                                                         bordermode='ignore')
        self.btn_file_dialog_path_to_your_pictures.configure(compound='left')
        self.btn_file_dialog_path_to_your_pictures.configure(font="-family {Verdana} -size 10 -weight bold")
        self.btn_file_dialog_path_to_your_pictures.configure(background="white")
        self.btn_file_dialog_path_to_your_pictures.configure(text='Select your folder:')
        self.btn_file_dialog_path_to_your_pictures.configure(command=lambda: get_user_path_to_picture_folder())

        # Placing a filedialog button to handle the save path of the pictures.
        self.btn_file_dialog_save_path_dataset = tk.Button(self.label_frame_create_own_dataset)
        self.btn_file_dialog_save_path_dataset.place(relx=0.018, rely=0.490, height=24, relwidth=0.378,
                                                     bordermode='ignore')
        self.btn_file_dialog_save_path_dataset.configure(compound='left')
        self.btn_file_dialog_save_path_dataset.configure(font="-family {Verdana} -size 10 -weight bold")
        self.btn_file_dialog_save_path_dataset.configure(background="white")
        self.btn_file_dialog_save_path_dataset.configure(text='Select your folder:')
        self.btn_file_dialog_save_path_dataset.configure(command=lambda: store_user_path_to_save_picture_folder())

        # Placing the first option button aka radiobutton.
        self.style = ttk.Style()
        self.style.map('TRadiobutton', background=[('selected', '#330066'), ('active', '#330066')])
        self.style.configure('.', background='#330066')
        self.style.configure('.', foreground='white')
        self.style.configure('.', font="-family {Verdana} -size 10 -weight bold")

        self.radiobutton1 = ttk.Radiobutton(self.label_frame_create_own_dataset, text="Option 1", variable=self.choice,
                                            value=0)
        self.radiobutton1.place(relx=0.550, rely=0.120, relwidth=0.215, relheight=0.049, height=21)
        self.radiobutton1.configure(compound='left')
        self.radiobutton1.configure(text='Crop pictures')

        # Place the second option button aka radiobutton 2 (Resize the pictures)
        self.radiobutton2 = ttk.Radiobutton(self.label_frame_create_own_dataset, text="Option 2", variable=self.choice,
                                            value=1)
        self.radiobutton2.place(relx=0.550, rely=0.250, relwidth=0.250, relheight=0.049, height=21)
        self.radiobutton2.configure(compound='left')
        self.radiobutton2.configure(text='Resize pictures')

        # place the textbox1 inside the label_frame_create_own_dataset and a label path to pictures.
        self.label_the_path_to_pictures = tk.Label(self.label_frame_create_own_dataset)
        self.label_the_path_to_pictures.place(relx=0.021, rely=0.1140, height=31, width=220, bordermode='ignore')
        self.label_the_path_to_pictures.configure(background="#330066")
        self.label_the_path_to_pictures.configure(anchor='w')
        self.label_the_path_to_pictures.configure(compound='left')
        self.label_the_path_to_pictures.configure(font="-family {Verdana} -size 12")
        self.label_the_path_to_pictures.configure(foreground="white")
        self.label_the_path_to_pictures.configure(text='Path to your picture folder')

        self.textbox1_var = tk.StringVar()
        self.textbox1 = tk.Entry(self.label_frame_create_own_dataset, textvariable=self.textbox1_var)
        self.textbox1.place(relx=0.018, rely=0.200, height=20, relwidth=0.378, bordermode='ignore')

        # Adding labels to the image size boxes.
        self.user_setting_image_size_label = tk.Label(self.label_frame_create_own_dataset)
        self.user_setting_image_size_label.place(relx=0.545, rely=0.4000, height=31, width=220, bordermode='ignore')
        self.user_setting_image_size_label.configure(background="#330066")
        self.user_setting_image_size_label.configure(anchor='w')
        self.user_setting_image_size_label.configure(compound='left')
        self.user_setting_image_size_label.configure(font="-family {Verdana} -size 12")
        self.user_setting_image_size_label.configure(foreground="white")
        self.user_setting_image_size_label.configure(text='Height and Width')

        # Adding 2 moore textboxes so the user can decide the image size , if he want to.

        self.textbox4_var = tk.StringVar()
        self.textbox4 = tk.Entry(self.label_frame_create_own_dataset, textvariable=self.textbox4_var)
        self.textbox4.place(relx=0.550, rely=0.500, height=20, relwidth=0.100, bordermode='ignore')

        self.textbox5_var = tk.StringVar()
        self.textbox5 = tk.Entry(self.label_frame_create_own_dataset, textvariable=self.textbox5_var)
        self.textbox5.place(relx=0.720, rely=0.500, height=20, relwidth=0.100, bordermode='ignore')

        # Next textbox called textbox3 I made an error then I was thinking what was needed on the gui...
        # and placing the label to the textbox3, save path
        self.label_save_path = tk.Label(self.main_frame)
        self.label_save_path.place(relx=0.008, rely=0.310, height=22, width=200)
        self.label_save_path.configure(anchor='w')
        self.label_save_path.configure(compound='left')
        self.label_save_path.configure(background="#330066")
        self.label_save_path.configure(font="-family {Verdana} -size 12")
        self.label_save_path.configure(foreground="white")
        self.label_save_path.configure(text='Save picture path folder')

        # This textbox should hold the path you want your transformed pictures to, with lower quality.

        self.textbox3_var = tk.StringVar()
        self.textbox3 = tk.Entry(self.label_frame_create_own_dataset, textvariable=self.textbox3_var)
        self.textbox3.place(relx=0.018, rely=0.430, height=20, relwidth=0.378, bordermode='ignore')

        # Place a progressbar so the user can se that stuff happens and doesn't worry about that the app hangs.
        self.statusbar1 = ttk.Progressbar(self.main_frame)
        self.statusbar1.place(relx=0.008, rely=0.514, relwidth=0.307, relheight=0.0, height=22)
        self.statusbar1.configure(length="527")

        # Starting with the second labelframe, who contains train the model.
        # ********************************************************************
        self.labelframe_train_model = tk.LabelFrame(self.main_frame)
        self.labelframe_train_model.place(relx=0.331, rely=0.17, relheight=0.392, relwidth=0.323)
        self.labelframe_train_model.configure(font="-family {Verdana} -size 14")
        self.labelframe_train_model.configure(foreground="white")
        self.labelframe_train_model.configure(text='Train model:')
        self.labelframe_train_model.configure(background="#330066")

        # Placing the label to the path to picture folder.
        self.label_path_to_picture_folder = tk.Label(self.labelframe_train_model)
        self.label_path_to_picture_folder.place(relx=0.220, rely=0.113, height=31, width=320, bordermode='ignore')
        self.label_path_to_picture_folder.configure(anchor='w')
        self.label_path_to_picture_folder.configure(compound='left')
        self.label_path_to_picture_folder.configure(background="#330066")
        self.label_path_to_picture_folder.configure(font="-family {Verdana} -size 12")
        self.label_path_to_picture_folder.configure(foreground="white")
        self.label_path_to_picture_folder.configure(text='Path to your training pictures folder')

        # Placing the textbox2 that should contain the path to the pictures the model needs to train.
        self.textbox2 = tk.Entry(self.labelframe_train_model)
        self.textbox2.place(relx=0.106, rely=0.271, height=20, relwidth=0.687, bordermode='ignore')

        # Placing the button that should start the training
        self.btn_train_model = tk.Button(self.main_frame)
        self.btn_train_model.place(relx=0.365, rely=0.263, height=34, width=387)
        self.btn_train_model.configure(background="white")
        self.btn_train_model.configure(compound='left')
        self.btn_train_model.configure(font="-family {Verdana} -size 10 -weight bold")
        self.btn_train_model.configure(foreground="#000000")
        self.btn_train_model.configure(text='Train model')
        self.btn_train_model.configure(command=lambda: training_the_model())

        # Placing the config button
        self.btn_train_config = tk.Button(self.main_frame)
        self.btn_train_config.place(relx=0.365, rely=0.330, height=34, width=387)
        self.btn_train_config.configure(background="white")
        self.btn_train_config.configure(compound='left')
        self.btn_train_config.configure(font="-family {Verdana} -size 10 -weight bold")
        self.btn_train_config.configure(foreground="#000000")
        self.btn_train_config.configure(text='Enter Config Settings')
        self.btn_train_config.configure(command=lambda: config_settings_window())

        # Placing a statusbar, so we can se the training progress.
        self.statusbar2 = ttk.Progressbar(self.main_frame)
        self.statusbar2.place(relx=0.365, rely=0.514, relwidth=0.223, relheight=0.0, height=22)
        self.statusbar2.configure(length="384")

        # Starts with creating the Super Resolution labelframe.
        # ********************************************************

        self.labelframe_create_super_resolution_photos = tk.LabelFrame(self.main_frame)
        self.labelframe_create_super_resolution_photos.place(relx=0.663, rely=0.171, relheight=0.392, relwidth=0.337)
        self.labelframe_create_super_resolution_photos.configure(font="-family {Verdana} -size 14")
        self.labelframe_create_super_resolution_photos.configure(foreground="white")
        self.labelframe_create_super_resolution_photos.configure(background="#330066")
        self.labelframe_create_super_resolution_photos.configure(text='Create Super resolution photo:')

        # Placing a button down in the labelframe_create_super_resolution_photos.
        # This button should later hold the code to make super resolution photos.
        self.btn_create_super_resolution_photo = tk.Button(self.main_frame)
        self.btn_create_super_resolution_photo.place(relx=0.735, rely=0.260, height=34, width=327)
        self.btn_create_super_resolution_photo.configure(background="white")
        self.btn_create_super_resolution_photo.configure(compound='left')
        self.btn_create_super_resolution_photo.configure(font="-family {Verdana} -size 10 -weight bold")
        self.btn_create_super_resolution_photo.configure(foreground="#000000")
        self.btn_create_super_resolution_photo.configure(text='Create super resolution photo')
        self.btn_create_super_resolution_photo.configure(command=lambda: create_super_resolution_photo())

        # Adding a progressbar, so we can track progress then creating super photos.
        self.statusbar3 = ttk.Progressbar(self.main_frame)
        self.statusbar3.place(relx=0.735, rely=0.314, relwidth=0.188, relheight=0.0, height=22)
        self.statusbar3.configure(length="329")

        # Adding the status labels, so we can write text, of the status of each process.
        # ******************************************************************************

        # This one is with the create your own dataset
        # self.status_label1_var = tk.StringVar()
        self.status_label1 = tk.Label(self.main_frame)
        self.status_label1.place(relx=0.001, rely=0.568, height=48, width=439)
        self.status_label1.configure(anchor='w')
        self.status_label1.configure(compound='left')
        self.status_label1.configure(background="black")
        self.status_label1.configure(foreground="white")
        self.status_label1.configure(font="-family {Verdana} -size 12 -weight bold")
        self.status_label1.configure(text='Status:')

        # This one is with the train model.
        self.status_label2 = tk.Label(self.main_frame)
        self.status_label2.place(relx=0.332, rely=0.568, height=48, width=439)
        self.status_label2.configure(anchor='w')
        self.status_label2.configure(compound='left')
        self.status_label2.configure(background="black")
        self.status_label2.configure(foreground="white")
        self.status_label2.configure(font="-family {Verdana} -size 12 -weight bold")
        self.status_label2.configure(text='Status:')

        # This one is with create Super Resolution Photos.
        self.status_label3 = tk.Label(self.main_frame)
        self.status_label3.place(relx=0.662, rely=0.568, height=50, width=439)
        self.status_label3.configure(anchor='w')
        self.status_label3.configure(compound='left')
        self.status_label3.configure(background="black")
        self.status_label3.configure(foreground="white")
        self.status_label3.configure(font="-family {Verdana} -size 12 -weight bold")
        self.status_label3.configure(text='Status:')

        # Create a separator line.
        self.separator1 = ttk.Separator(self.main_frame)
        self.separator1.place(relx=0.00, rely=0.638, relwidth=0.999)

        # Creating the label frames for the photos we want to display.
        # ************************************************************

        self.labelframe_original_photo = tk.LabelFrame(self.main_frame)
        self.labelframe_original_photo.place(relx=0.000, rely=0.657, relheight=0.336, relwidth=0.322)
        self.labelframe_original_photo.configure(font="-family {Verdana} -size 14")
        self.labelframe_original_photo.configure(foreground="white")
        self.labelframe_original_photo.configure(text='Original Photo')
        self.labelframe_original_photo.configure(background="#330066")

        # Placing the container for the photo (Original Photo)
        # This label should hold no text later, it should only hold the image we want to display.
        self.original_container_label = tk.Label(self.main_frame)
        self.original_container_label.place(relx=0.020, rely=0.737, height=50, width=363)
        self.original_container_label.configure(foreground="white")
        self.original_container_label.configure(background="#330066")
        self.original_container_label.configure(font="-family {Verdana} -size 12 -weight bold")
        self.original_container_label.configure(text='Image Container')

        # label frame for the input picture.
        self.labelframe_input_picture = tk.LabelFrame(self.main_frame)
        self.labelframe_input_picture.place(relx=0.33, rely=0.657, relheight=0.337, relwidth=0.325)
        self.labelframe_input_picture.configure(font="-family {Verdana} -size 14")
        self.labelframe_input_picture.configure(text='Input Image')
        self.labelframe_input_picture.configure(foreground="white")
        self.labelframe_input_picture.configure(background="#330066")

        # Placing the container for the input picture.
        # This label should hold no text later, it should only hold the image we want to display.
        self.input_picture_container_label = tk.Label(self.main_frame)
        self.input_picture_container_label.place(relx=0.38, rely=0.737, height=50, width=363)
        self.input_picture_container_label.configure(foreground="white")
        self.input_picture_container_label.configure(background="#330066")
        self.input_picture_container_label.configure(font="-family {Verdana} -size 12 -weight bold")
        self.input_picture_container_label.configure(text='Image Container 2')

        # Label frame for the Super resolution Photo
        self.labelframe_output_image = tk.LabelFrame(self.main_frame)
        self.labelframe_output_image.place(relx=0.661, rely=0.657, relheight=0.337, relwidth=0.339)
        self.labelframe_output_image.configure(font="-family {Verdana} -size 14")
        self.labelframe_output_image.configure(foreground="white")
        self.labelframe_output_image.configure(background="#330066")
        self.labelframe_output_image.configure(text='Output Image')

        # Placing the Output Image Container.
        # This label should hold no text later, it should only hold the image we want to display.
        self.output_image_container_label = tk.Label(self.main_frame)
        self.output_image_container_label.place(relx=0.731, rely=0.737, height=50, width=363)
        self.output_image_container_label.configure(foreground="white")
        self.output_image_container_label.configure(background="#330066")
        self.output_image_container_label.configure(font="-family {Verdana} -size 12 -weight bold")
        self.output_image_container_label.configure(text='Image Container 3')
