import time
from tkinter import *
import pygame
import os
from os.path import join
from tkinter import filedialog
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

# color_red =
# directory/folder path
dir_path = r'audio'

music_list = []


# Iterate directory
def show_list():
    for file_path in os.listdir(dir_path):
        # check if current file_path is a file
            if os.path.isfile(os.path.join(dir_path, file_path)):
                # add filename to list
                music_list.append(file_path)


root = Tk()

root.title('MP3.Player')
root.iconbitmap('image/sound.ico')
root.geometry("550x600")
pygame.mixer.init()


# Grab song length info
def song_len_info():
    # Grab current song elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000

    # convert to time format
    conv_curr_time = time.strftime('%H:%M:%S', time.gmtime(current_time))

    # throw up temp label to get data
    # slider_label.config(text=f'Slider: {int(trek_slider.get())} and Song Position: {int(current_time)} ')

    # Get the current song tuple number
    current_song = display.curselection()
    # Add one to the current song number
    # Grab song title from playlist
    song = display.get(current_song)
    # Add directory structure and mp3 to song title
    song = f'C:/Users/leroy/PycharmProjects/pythonProject11/audio/{song}.mp3'
    # Get song length with Mutagen
    song_mut = MP3(song)
    # Get song length
    global song_length
    song_length = song_mut.info.length
    # Convert to time format
    conv_all_time = time.strftime('%H:%M:%S', time.gmtime(song_length))

    current_time += 1

    if int(trek_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {conv_curr_time} of {conv_all_time}  ')

    elif paused:
        pass

    elif int(trek_slider.get()) == int(current_time):
        # slider hasn't been moved

        # update slider to position
        slider_position = int(song_length)
        trek_slider.config(to=slider_position, value=int(current_time))
    else:
        slider_position = int(song_length)
        trek_slider.config(to=slider_position, value=int(trek_slider.get()))

        # convert to time format
        conv_curr_time = time.strftime('%H:%M:%S', time.gmtime(int(trek_slider.get())))

        # output time to status bar
        status_bar.config(text=f'Time Elapsed: {conv_curr_time} of {conv_all_time}  ')

        # Move thing along by one second
        next_time = int(trek_slider.get()) + 1
        trek_slider.config(value=next_time)


    # # output time to status bar
    # status_bar.config(text=f'Time Elapsed: {conv_curr_time} of {conv_all_time}  ')

    # trek_slider.config(value=current_time)

    # update time
    status_bar.after(1000, song_len_info)


def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose song", filetypes=(("mp3 File", "*.mp3"), ))

    # strip out the directory info and .mp3 extension
    song = song.replace("C:/Users/leroy/PycharmProjects/pythonProject11/audio/", "")
    song = song.replace(".mp3", "")

    # Add song to list box
    display.insert(END, song)


def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose song", filetypes=(("mp3 File", "*.mp3"),))

    for song in songs:
        song = song.replace("C:/Users/leroy/PycharmProjects/pythonProject11/audio/", "")
        song = song.replace(".mp3", "")

        display.insert(END, song)


def delete_one():
    stop()
    display.delete(ANCHOR)
    pygame.mixer.music.stop()


def delete_all():
    stop()
    display.delete(0, END)
    pygame.mixer.music.stop()


def play():
    global stopped
    stopped = False

    song = display.get(ACTIVE)
    song = f'C:/Users/leroy/PycharmProjects/pythonProject11/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Call the info function
    song_len_info()


    # slider_position = int(song_length)
    # trek_slider.config(to=slider_position, value=0)


# Stop playing current song
global stopped
stopped = False
def stop():
    # Reset slider and status bar
    status_bar.config(text='')
    trek_slider.config(value=0)
    # Stop playing
    pygame.mixer.music.stop()
    display.selection_clear(ACTIVE)

    # Clear the status bar
    status_bar.config(text='')

    # Set stop variable to true
    global stopped
    stopped = True


def next_song():
    # Reset slider and status bar
    status_bar.config(text='')
    trek_slider.config(value=0)
    # Get the current song tuple number
    next_one = display.curselection()
    # Add one to the current song number
    next_one = next_one[0]+1
    # Grab song title from playlist
    song = display.get(next_one)
    # Add directory structure and mp3 to song title
    song = f'C:/Users/leroy/PycharmProjects/pythonProject11/audio/{song}.mp3'
    # Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Clear active bar in playlist listbox
    display.selection_clear(0, END)
    # Active new song bar
    display.activate(next_one)
    display.selection_set(next_one, last=None)


def previous_song():
    # Reset slider and status bar
    status_bar.config(text='')
    trek_slider.config(value=0)
    pre_one = display.curselection()
    pre_one = pre_one[0] - 1
    song = display.get(pre_one)
    song = f'C:/Users/leroy/PycharmProjects/pythonProject11/audio/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    display.selection_clear(0, END)
    display.activate(pre_one)
    display.selection_set(pre_one, last=None)


global paused
paused = False


def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True


def slide(x):

    # slider_label.config(text=f'{int(trek_slider.get())} of {int(song_length)}')

    song = display.get(ACTIVE)
    song = f'C:/Users/leroy/PycharmProjects/pythonProject11/audio/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(trek_slider.get()))


# Create volume func
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

pygame.mixer.init()

# Songs display
display = Listbox(root, bg="black", fg="green", selectbackground="green", selectforeground="black", width=90, height=20)
display.pack(pady=10)
# Define picture
back_bttn_img = PhotoImage(file="image/back-arrow.png")
stop_bttn_img = PhotoImage(file="image/stop-button.png")
play_bttn_img = PhotoImage(file="image/play-button.png")
pause_bttn_img = PhotoImage(file="image/pause.png")
forward_bttn_img = PhotoImage(file="image/forward-arrow.png")

master_frame = Frame(root)
master_frame.pack(pady=5)

# Frame for button
controls_frame = Frame(master_frame)
controls_frame.grid(pady=5, row=1, column=0, columnspan=4)

# Create volume frame
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=1, column=4)

# Buttons
back_button = Button(controls_frame, image=back_bttn_img, borderwidth=0, command=previous_song)
back_button.grid(row=0, column=0, pady=10, padx=5)
stop_button = Button(controls_frame, image=stop_bttn_img, borderwidth=0, command=stop)
stop_button.grid(row=0, column=1, pady=10, padx=5)
play_button = Button(controls_frame, image=play_bttn_img, borderwidth=0, command=play)
play_button.grid(row=0, column=2, pady=10, padx=5)
pause_button = Button(controls_frame, image=pause_bttn_img, borderwidth=0, command=lambda: pause(paused))
pause_button.grid(row=0, column=3, pady=10, padx=5)
forward_button = Button(controls_frame, image=forward_bttn_img, borderwidth=0, command=next_song)
forward_button.grid(row=0, column=4, pady=10, padx=5)

# Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add songs
add_songs_menu = Menu(my_menu)
my_menu.add_cascade(label="Add New Songs", menu=add_songs_menu)
add_songs_menu.add_command(label="Add Song", command=add_song)
# Add many songs
add_songs_menu.add_command(label="Add Many Songs", command=add_many_song)

# Delete song
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_one)
remove_song_menu.add_command(label="Delete all songs from playlist", command=delete_all)

status_bar = Label(root, text='', relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create trek slider
trek_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=460)
trek_slider.grid(pady=10, row=2, column=1, columnspan=4)

# Create volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=80)
volume_slider.pack(pady=10)

# Player control frame
# slider_label = Label(root, text="0")
# slider_label.pack(pady=10)


root.mainloop()