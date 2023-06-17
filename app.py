import threading
import tkinter as tk
from tkinter.font import Font
import customtkinter as ctk
from script import mico_videos, mico_sync
from pytube import YouTube
from werkzeug.utils import secure_filename
import os
from PIL import Image

def select_frame_by_name(name):
    # set button color for selected button
    app.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
    app.sync_button.configure(fg_color=("gray75", "gray25") if name == "sync" else "transparent")

    # show selected frame
    if name == "home":
        app.home_frame.grid(row=0, column=1, sticky="nsew")
    else:
        app.home_frame.grid_forget()
    if name == "sync":
        app.sync_frame.grid(row=0, column=1, sticky="nsew")
    else:
        app.sync_frame.grid_forget()
        
def home_button_event():
    select_frame_by_name("home")

def sync_button_event():
    select_frame_by_name("sync")

def change_appearance_mode_event(new_appearance_mode):
    ctk.set_appearance_mode(new_appearance_mode)
    
def uploadBot():
    try:
        file = tk.filedialog.askopenfile(mode="r", filetypes=[('Video Files', ['*.mp4', "*.mov"])])
        bot_name = file.name
        bot_title.configure(text=bot_name)
        if file:
            startDownload(bot_name)
            
    except Exception as e:
        print(e)

def preview():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink)
        title.configure(text=ytObject.title, text_color="black")
        
        bot_title.grid(row=3,column=0,columnspan=2, padx=20, pady=10)
        upload.grid(row=4,column=0,columnspan=2, padx=20, pady=10)

    except Exception as e:
        title.configure(text="Enter a link !", text_color="black")
        progressLabel.configure(text="Download error - Invalid Link", text_color = "red")
        
def startDownload(bot_name):
    try:
        ytLink = link.get()
        progressLabel.grid(row=5,column=0,columnspan=2, padx=20, pady=10)
        pPercentage.grid(row=6,column=0,columnspan=2, padx=20, pady=10)
        progressBar.grid(row=7,column=0,columnspan=2, padx=20, pady=10)
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()
        progressLabel.configure(text="")
        
        video.download(filename="top_for_mico.mp4")
        progressLabel.destroy()
        progressBar.destroy()
        pPercentage.configure(text="Syncing videos based on audio...(This may take some time)", text_color = "black")
        infiniteBar.grid(row=7,column=0,columnspan=2, padx=20, pady=10)
        mico_videos(bot_name, "top_for_mico.mp4", mirror_bot = True, mirror_top= var1 )
        os.remove("top_for_mico.mp4")
        infiniteBar.destroy()
        os.startfile("mico_video.mp4")
        app.destroy()
        
        
    except Exception as e:
        print(e)
        progressLabel.configure(text="Download error - Invalid Link", text_color = "red")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize * 2
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    
    progressLabel.configure(text="Downloading youtube file (Don't worry, it will be removed after)", text_color="black")
    pPercentage.configure(text=per+"%")
    pPercentage.update()

    # Update progress bar
    
    progressBar.set(float(percentage_of_completion)/100)
    
def sync_uploadBot():
    try:
        file = tk.filedialog.askopenfile(mode="r", filetypes=[('Video Files', ['*.mp4', "*.mov"])])
        sync_bot_name = file.name
        sync_bot_title.configure(text=sync_bot_name)
        if file:
            sync_startDownload(sync_bot_name)
            
    except Exception as e:
        print(e)

def sync_preview():
    try:
        ytLink = sync_link.get()
        ytObject = YouTube(ytLink)
        sync_title.configure(text=ytObject.title, text_color="black")
        
        sync_bot_title.grid(row=3,column=0,columnspan=2, padx=20, pady=10)
        sync_upload.grid(row=4,column=0,columnspan=2, padx=20, pady=10)

    except Exception as e:
        sync_title.configure(text="Enter a link !", text_color="black")
        sync_progressLabel.configure(text="Download error - Invalid Link", text_color = "red")
        
def sync_startDownload(bot_name):
    try:
        ytLink = sync_link.get()
        sync_progressLabel.grid(row=5,column=0,columnspan=2, padx=20, pady=10)
        sync_pPercentage.grid(row=6,column=0,columnspan=2, padx=20, pady=10)
        sync_progressBar.grid(row=7,column=0,columnspan=2, padx=20, pady=10)
        ytObject = YouTube(ytLink, on_progress_callback=sync_on_progress)
        video = ytObject.streams.get_highest_resolution()
        sync_progressLabel.configure(text="")
        
        video.download(filename="top_for_mico.mp4")
        sync_progressLabel.destroy()
        sync_progressBar.destroy()
        sync_pPercentage.configure(text="Applying audio...(This may take some time)", text_color = "black")
        sync_infiniteBar.grid(row=7,column=0,columnspan=2, padx=20, pady=10)
        mico_sync(bot_name, "top_for_mico.mp4")
        os.remove("top_for_mico.mp4")
        sync_infiniteBar.destroy()
        os.startfile("mico_video.mp4")
        app.destroy()
        
        
    except Exception as e:
        print(e)
        sync_progressLabel.configure(text="Download error - Invalid Link", text_color = "red")

def sync_on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize * 2
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    
    sync_progressLabel.configure(text="Downloading youtube file (Don't worry, it will be removed after)", text_color="black")
    sync_pPercentage.configure(text=per+"%")
    sync_pPercentage.update()

    # Update progress bar
    
    sync_progressBar.set(float(percentage_of_completion)/100)   
    
# System settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Our app frame

app = ctk.CTk()
app.geometry("800x450")
app.title("Mico")
app.resizable(0,0)

# set grid layout 1x2
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# load images with light and dark mode image
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
app.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(26, 26))
app.mirror_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "edit_dark.png")),
                                            dark_image=Image.open(os.path.join(image_path, "edit_light.png")), size=(20, 20))
app.wave_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "wave_dark.png")),
                                            dark_image=Image.open(os.path.join(image_path, "wave_light.png")), size=(20, 20))

# create navigation frame
app.navigation_frame = ctk.CTkFrame(app, corner_radius=0)
app.navigation_frame.grid(row=0, column=0, sticky="nsew")
app.navigation_frame.grid_rowconfigure(3, weight=1)

app.navigation_frame_label = ctk.CTkLabel(app.navigation_frame, text="  Mico - Mirror and Compare", image=app.logo_image,
                                                        compound="left", font=ctk.CTkFont(size=15, weight="bold"))
app.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

app.home_button = ctk.CTkButton(app.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Superpose and sync",
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            image=app.mirror_image, anchor="w", command=home_button_event)
app.home_button.grid(row=1, column=0, sticky="ew")

app.sync_button = ctk.CTkButton(app.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Only sync",
                                                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                image=app.wave_image, anchor="w", command=sync_button_event)
app.sync_button.grid(row=2, column=0, sticky="ew")

app.appearance_mode_menu = ctk.CTkOptionMenu(app.navigation_frame, values=["Light", "Dark", "System"],
                                                        command=change_appearance_mode_event)
app.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=20, sticky="s")

# create home frame
app.home_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")
app.home_frame.grid_columnconfigure(1, weight=1)

# Adding UI elements
title = ctk.CTkLabel(app.home_frame, text="Insert a youtube link for a video to be on top")
title.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

# Link input
url_var = tk.StringVar()
link = ctk.CTkEntry(app.home_frame, width=350, height=40, textvariable=url_var)
link.grid(row=1, column=0, padx=20, pady=10)

# Mirror button

var1 = tk.IntVar()
c1 = ctk.CTkCheckBox(app.home_frame, text='Mirror it ?',variable=var1, onvalue=True, offvalue=False)
c1.grid(row=1, column=1)

# Submit link button

submit_btn = ctk.CTkButton(app.home_frame, text="Submit Link", command=preview)
submit_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=10)


# Upload Button

bot_title = ctk.CTkLabel(app.home_frame, text="")

upload = ctk.CTkButton(app.home_frame, text="Upload your video (Mico will mirror it)", command=threading.Thread(target=uploadBot).start)

# Downloading progress

progressLabel = ctk.CTkLabel(app.home_frame, text="")


# Progress percentage
pPercentage = ctk.CTkLabel(app.home_frame, text="0%")

progressBar = ctk.CTkProgressBar(app.home_frame, width=300)
progressBar.set(0)

# 2nd progress bar
infiniteBar = ctk.CTkProgressBar(app.home_frame, width=300)
infiniteBar.configure(mode="indeterminate")
infiniteBar.start()

# Finish label

finishLabel = ctk.CTkLabel(app.home_frame, text="")
finishLabel.grid(row=8,column=0,columnspan=2, padx=20, pady=10)

# **********************************************************************
# create sync frame
app.sync_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")
app.sync_frame.grid_columnconfigure(0, weight=1)

# Adding UI elements
sync_title = ctk.CTkLabel(app.sync_frame, text="Insert a youtube link of the audio you need")
sync_title.grid(row=0, column=0, padx=20, pady=10)

# Link input
sync_url_var = tk.StringVar()
sync_link = ctk.CTkEntry(app.sync_frame, width=350, height=40, textvariable=sync_url_var)
sync_link.grid(row=1, column=0, padx=20, pady=10)

# Submit link button

sync_submit_btn = ctk.CTkButton(app.sync_frame, text="Submit Link", command=sync_preview)
sync_submit_btn.grid(row=2, column=0, padx=20, pady=10)


# Upload Button

sync_bot_title = ctk.CTkLabel(app.sync_frame, text="")

sync_upload = ctk.CTkButton(app.sync_frame, text="Upload your video (Mico will NOT mirror it)", command=threading.Thread(target=sync_uploadBot).start)

# Downloading progress

sync_progressLabel = ctk.CTkLabel(app.sync_frame, text="")

# Progress percentage
sync_pPercentage = ctk.CTkLabel(app.sync_frame, text="0%")

sync_progressBar = ctk.CTkProgressBar(app.sync_frame, width=300)
sync_progressBar.set(0)

# 2nd progress bar
sync_infiniteBar = ctk.CTkProgressBar(app.sync_frame, width=300)
sync_infiniteBar.configure(mode="indeterminate")
sync_infiniteBar.start()

# Finish label

sync_finishLabel = ctk.CTkLabel(app.sync_frame, text="")
sync_finishLabel.grid(row=8,column=0,columnspan=2, padx=20, pady=10)

# select default frame
select_frame_by_name("home")

# Run app

app.mainloop()