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

"""
*******************************************************************************************
2022-04-21 Super Resolution Gui Class.
This class is written to handle all the gui things we need to present to the screen
it should also handle all the functions and actions then pressing buttons etc. 
********************************************************************************************
"""


class SuperResolutionGuiClass:
    def __init__(self, user_window):
        self.window = user_window
        self.window.title('Super Resolution Application')
        self.window.geometry('1764x968+71+7')
        self.window.resizable(False, False)

        # Add the functions here before the gui part starts.
        def convert_to_96x96_and_24x24():

            # crop the largest size square
            def crop(img):
                width, height = img.size
                return img.crop(((width - min(img.size)) // 2, (height - min(img.size)) // 2,
                                (width + min(img.size)) // 2, (height + min(img.size)) // 2))

            try:
                path_to = self.textbox1_var.get()
                save_path = self.textbox3_var.get()
                self.statusbar1['maximum'] = len(os.listdir(path_to))

                for images in os.listdir(path_to):
                    if images.endswith((".png", ".jpg", ".jpeg")):
                        image_hr = Image.open(os.path.join(path_to, images))

                        image_hr = crop(image_hr).resize((96, 96))
                        image_lr = image_hr.copy().resize((24, 24))

                        fn, fext = os.path.splitext(images)
                        image_hr.save(f'{save_path}/%s_96%s' % (fn, fext))
                        image_lr.save(f'{save_path}/%s_24%s' % (fn, fext))

                        self.statusbar1['value'] += 1
                        self.statusbar1.update()
                        self.status_label1['text'] = "Status: {0:.0f}%".format(self.statusbar1['value']/len(os.listdir(path_to)) * 100)

                showinfo(message='Dataset completed!')

            except WindowsError:
                showinfo(message='Insert a valid folder')

        def training_the_model():
            print("Im the function that should train the model then the button is pressed. :)")

        def create_super_resolution_photo():
            print("Im the function that should take care of the Super Resolution Photo process. :)")


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
        self.main_frame.configure(background="white")

        # Next up is a frame on the main frame. but on the top.
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.place(relx=0.0, rely=0.0, relheight=0.154, relwidth=1.000)
        self.top_frame.configure(relief='groove')
        self.top_frame.configure(borderwidth="2")
        self.top_frame.configure(background="#697DE1")

        # Next thing I want to do is to place the logo, inside the frame.
        self.logo_label = tk.Label(self.main_frame)
        self.logo_label.place(relx=0.354, rely=0.033, height=60, width=650)
        self.logo_label.configure(background="#697DE1")
        self.logo_label.configure(foreground="white")
        self.logo_label.configure(anchor='w')
        self.logo_label.configure(compound='left')
        self.logo_label.configure(font="-family {Verdana} -size 36 -weight bold")
        self.logo_label.configure(text='Super resolution')

        # Now I have to place the first labelframe and place text boxes and buttons inside it.
        self.label_frame_create_own_dataset = tk.LabelFrame(self.main_frame)
        self.label_frame_create_own_dataset.place(relx=0.000, rely=0.17, relheight=0.192, relwidth=0.323)
        self.label_frame_create_own_dataset.configure(relief='groove')
        self.label_frame_create_own_dataset.configure(font="-family {Verdana} -size 14")
        self.label_frame_create_own_dataset.configure(foreground="white")
        self.label_frame_create_own_dataset.configure(highlightcolor="white")
        self.label_frame_create_own_dataset.configure(text='Create own dataset:')
        self.label_frame_create_own_dataset.configure(background="#697DE1")  # 6600CC

        # Place the button inside the label_frame_create_own_dataset
        self.btn_create_dataset = tk.Button(self.label_frame_create_own_dataset)
        self.btn_create_dataset.place(relx=0.018, rely=0.492, height=34, width=537, bordermode='ignore')
        self.btn_create_dataset.configure(compound='left')
        self.btn_create_dataset.configure(font="-family {Verdana} -size 10 -weight bold")
        self.btn_create_dataset.configure(background="white")  # d9d9d9
        self.btn_create_dataset.configure(text='Create dataset')
        self.btn_create_dataset.configure(command=lambda: convert_to_96x96_and_24x24())

        # place the textbox1 inside the label_frame_create_own_dataset and a label path to pictures.
        self.label_the_path_to_pictures = tk.Label(self.label_frame_create_own_dataset)
        self.label_the_path_to_pictures.place(relx=0.071, rely=0.1140, height=31, width=151, bordermode='ignore')
        self.label_the_path_to_pictures.configure(background="#697DE1")
        self.label_the_path_to_pictures.configure(anchor='w')
        self.label_the_path_to_pictures.configure(compound='left')
        self.label_the_path_to_pictures.configure(font="-family {Verdana} -size 10")
        self.label_the_path_to_pictures.configure(foreground="white")
        self.label_the_path_to_pictures.configure(text='Path to your pictures')

        self.textbox1_var = tk.StringVar()
        self.textbox1 = tk.Entry(self.label_frame_create_own_dataset, textvariable=self.textbox1_var)
        self.textbox1.place(relx=0.018, rely=0.271, height=20, relwidth=0.378, bordermode='ignore')

        # Next textbox called textbox3 I made an error then I was thinking what was needed on the gui...
        # and placing the label to the textbox3, save path
        self.label_save_path = tk.Label(self.main_frame)
        self.label_save_path.place(relx=0.222, rely=0.195, height=22, width=81)
        self.label_save_path.configure(anchor='w')
        self.label_save_path.configure(compound='left')
        self.label_save_path.configure(background="#697DE1")
        self.label_save_path.configure(font="-family {Verdana} -size 10")
        self.label_save_path.configure(foreground="white")
        self.label_save_path.configure(text='Save path')

        # This textbox should hold the path you want your transformed pictures to, with lower quality.
        self.textbox3_var = tk.StringVar()
        self.textbox3 = tk.Entry(self.label_frame_create_own_dataset, textvariable=self.textbox3_var)
        self.textbox3.place(relx=0.544, rely=0.271, height=20, relwidth=0.378, bordermode='ignore')

        # Place a progressbar so the user can se that stuff happens and doesn't worry about that the app hangs.
        self.statusbar1 = ttk.Progressbar(self.main_frame, value=0, orient='horizontal', mode='determinate')
        self.statusbar1.place(relx=0.008, rely=0.314, relwidth=0.307, relheight=0.0, height=22)

        # Starting with the second labelframe, who contains train the model.
        # ********************************************************************
        self.labelframe_train_model = tk.LabelFrame(self.main_frame)
        self.labelframe_train_model.place(relx=0.331, rely=0.17, relheight=0.192, relwidth=0.323)
        self.labelframe_train_model.configure(font="-family {Verdana} -size 14")
        self.labelframe_train_model.configure(foreground="white")
        self.labelframe_train_model.configure(text='Train model:')
        self.labelframe_train_model.configure(background="#697DE1")

        # Placing the label to the path to picture folder.
        self.label_path_to_picture_folder = tk.Label(self.labelframe_train_model)
        self.label_path_to_picture_folder.place(relx=0.265, rely=0.113, height=31, width=227, bordermode='ignore')
        self.label_path_to_picture_folder.configure(anchor='w')
        self.label_path_to_picture_folder.configure(compound='left')
        self.label_path_to_picture_folder.configure(background="#697DE1")
        self.label_path_to_picture_folder.configure(font="-family {Verdana} -size 10")
        self.label_path_to_picture_folder.configure(foreground="white")
        self.label_path_to_picture_folder.configure(text='Path to picture folder')

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

        # Placing a statusbar, so we can se the training progress.
        self.statusbar2 = ttk.Progressbar(self.main_frame)
        self.statusbar2.place(relx=0.365, rely=0.314, relwidth=0.223, relheight=0.0, height=22)
        self.statusbar2.configure(length="384")

        # Starts with creating the Super Resolution labelframe.
        # ********************************************************

        self.labelframe_create_super_resolution_photos = tk.LabelFrame(self.main_frame)
        self.labelframe_create_super_resolution_photos.place(relx=0.663, rely=0.171, relheight=0.192, relwidth=0.337)
        self.labelframe_create_super_resolution_photos.configure(font="-family {Verdana} -size 14")
        self.labelframe_create_super_resolution_photos.configure(foreground="white")
        self.labelframe_create_super_resolution_photos.configure(background="#697DE1")
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
        self.status_label1.place(relx=0.001, rely=0.368, height=48, width=439)
        self.status_label1.configure(anchor='w')
        self.status_label1.configure(compound='left')
        self.status_label1.configure(background="white")
        self.status_label1.configure(foreground="#697DE1")
        self.status_label1.configure(font="-family {Verdana} -size 12 -weight bold")
        self.status_label1.configure(text='Status:')

        # This one is with the train model.
        self.status_label2 = tk.Label(self.main_frame)
        self.status_label2.place(relx=0.332, rely=0.379, height=30, width=415)
        self.status_label2.configure(anchor='w')
        self.status_label2.configure(compound='left')
        self.status_label2.configure(background="white")
        self.status_label2.configure(foreground="#697DE1")
        self.status_label2.configure(font="-family {Verdana} -size 12 -weight bold")
        self.status_label2.configure(text='Status:')

        # This one is with create Super Resolution Photos.
        self.status_label3 = tk.Label(self.main_frame)
        self.status_label3.place(relx=0.662, rely=0.368, height=50, width=363)
        self.status_label3.configure(anchor='w')
        self.status_label3.configure(compound='left')
        self.status_label3.configure(background="white")
        self.status_label3.configure(foreground="#697DE1")
        self.status_label3.configure(font="-family {Verdana} -size 12 -weight bold")
        self.status_label3.configure(text='Status:')

        # Create a separator line.
        self.separator1 = ttk.Separator(self.main_frame)
        self.separator1.place(relx=0.00, rely=0.458, relwidth=0.999)

        # Creating the label frames for the photos we want to display.
        # ************************************************************

        self.labelframe_original_photo = tk.LabelFrame(self.main_frame)
        self.labelframe_original_photo.place(relx=0.000, rely=0.477, relheight=0.336, relwidth=0.322)
        self.labelframe_original_photo.configure(font="-family {Verdana} -size 14")
        self.labelframe_original_photo.configure(foreground="white")
        self.labelframe_original_photo.configure(text='Original Photo')
        self.labelframe_original_photo.configure(background="#697DE1")

        # Placing the container for the photo (Original Photo)
        # This label should hold no text later, it should only hold the image we want to display.
        self.original_container_label = tk.Label(self.main_frame)
        self.original_container_label.place(relx=0.020, rely=0.577, height=50, width=363)
        self.original_container_label.configure(foreground="white")
        self.original_container_label.configure(background="#697DE1")
        self.original_container_label.configure(font="-family {Verdana} -size 12 -weight bold")
        self.original_container_label.configure(text='Image Container')

        # label frame for the input picture.
        self.labelframe_input_picture = tk.LabelFrame(self.main_frame)
        self.labelframe_input_picture.place(relx=0.33, rely=0.477, relheight=0.337, relwidth=0.325)
        self.labelframe_input_picture.configure(font="-family {Verdana} -size 14")
        self.labelframe_input_picture.configure(text='Input Image')
        self.labelframe_input_picture.configure(foreground="white")
        self.labelframe_input_picture.configure(background="#697DE1")

        # Placing the container for the input picture.
        # This label should hold no text later, it should only hold the image we want to display.
        self.input_picture_container_label = tk.Label(self.main_frame)
        self.input_picture_container_label.place(relx=0.38, rely=0.577, height=50, width=363)
        self.input_picture_container_label.configure(foreground="white")
        self.input_picture_container_label.configure(background="#697DE1")
        self.input_picture_container_label.configure(font="-family {Verdana} -size 12 -weight bold")
        self.input_picture_container_label.configure(text='Image Container 2')

        # Label frame for the Super resolution Photo
        self.labelframe_output_image = tk.LabelFrame(self.main_frame)
        self.labelframe_output_image.place(relx=0.661, rely=0.477, relheight=0.337, relwidth=0.339)
        self.labelframe_output_image.configure(font="-family {Verdana} -size 14")
        self.labelframe_output_image.configure(foreground="white")
        self.labelframe_output_image.configure(background="#697DE1")
        self.labelframe_output_image.configure(text='Output Image')

        # Placing the Output Image Container.
        # This label should hold no text later, it should only hold the image we want to display.
        self.output_image_container_label = tk.Label(self.main_frame)
        self.output_image_container_label.place(relx=0.731, rely=0.577, height=50, width=363)
        self.output_image_container_label.configure(foreground="white")
        self.output_image_container_label.configure(background="#697DE1")
        self.output_image_container_label.configure(font="-family {Verdana} -size 12 -weight bold")
        self.output_image_container_label.configure(text='Image Container 3')
