from tkinter import *
from tkinter import filedialog
import pygame.mixer as mixer
import os
from tkinter import ttk

# Initializing the mixer
mixer.init()


def play_song(song_name: StringVar, songs_list: Listbox, status: StringVar, progress: ttk.Progressbar):
    songPlayingList = songs_list.get(ACTIVE).split("-")
    songName = songPlayingList[0]
    songArtistList = songPlayingList[1].split(".")
    songArtist = songArtistList[0]
    song_name.set(songName)

    mixer.music.load(songs_list.get(ACTIVE))
    mixer.music.play()

    status.set(f"PLAYING:    {songName.upper()} by {songArtist.upper()}")

    # Resetting the progress bar
    progress_bar['value'] = 0
    progress_bar['maximum'] = mixer.Sound(songs_list.get(ACTIVE)).get_length()
    progress.start(1000)
    update_progress()


def stop_song(status: StringVar, progress: ttk.Progressbar):
    mixer.music.stop()
    status.set("Song STOPPED")
    progress.stop()


def load(listbox):
    os.chdir(filedialog.askdirectory(title='Select your playlist'))

    tracks = os.listdir()

    for track in tracks:
        listbox.insert(END, track)


def pause_song(status: StringVar, progress: ttk.Progressbar):
    mixer.music.pause()
    status.set("Song PAUSED")
    progress.stop()


def resume_song(status: StringVar, songs_list: Listbox, progress: ttk.Progressbar):
    songPlayingList = songs_list.get(ACTIVE).split("-")
    songName = songPlayingList[0]
    songArtistList = songPlayingList[1].split(".")
    songArtist = songArtistList[0]
    mixer.music.unpause()
    status.set(f"RESUMING... {songName.upper()} by {songArtist.upper()}")
    progress.start(1000)


# Creating the master GUI
root = Tk()
root.geometry('660x300')
root.title("Pulkit's Music Player")
root.resizable(False, False)

# All the frames
song_frame = LabelFrame(root, text='Song playing', bg='LightBlue', width=400, height=80)
song_frame.place(x=0, y=0)

button_frame = LabelFrame(root, text='Control Buttons', bg='Turquoise', width=380, height=200)
button_frame.place(y=80)

listbox_frame = LabelFrame(root, text="Pulkit's Playlists", bg='RoyalBlue')
listbox_frame.place(x=385, y=0, height=280, width=280)

progress_bar = ttk.Progressbar(button_frame, orient='horizontal', mode='determinate', length=250)
progress_bar.place(x=65, y=90)

# All StringVar variables
current_song = StringVar(root, value='')

song_status = StringVar(root, value='No song playing at the moment')


def update_progress():
    current_time = mixer.music.get_pos() // 1000
    progress_bar['value'] = current_time
    root.after(1000, update_progress)


# Playlist ListBox
playlist = Listbox(listbox_frame, font=('comic sans ms', 10), selectbackground='LightPink')

scroll_bar = Scrollbar(listbox_frame, orient=VERTICAL)
scroll_bar.pack(side=RIGHT, fill=BOTH)
scroll_bar_horizontal = Scrollbar(listbox_frame, orient=HORIZONTAL)
scroll_bar_horizontal.pack(side=BOTTOM, fill=BOTH)

playlist.config(yscrollcommand=scroll_bar.set)
playlist.config(xscrollcommand=scroll_bar_horizontal.set)

scroll_bar.config(command=playlist.yview)
scroll_bar_horizontal.config(command=playlist.xview)

playlist.pack(fill=BOTH, padx=5, pady=5)

# SongFrame Labels
Label(song_frame, text='CURRENTLY PLAYING:', bg='LightBlue', font=('Times', 7, 'bold')).place(x=-1, y=20)

song_lbl = Label(song_frame, textvariable=current_song, font=("Times", 12), width=28)
song_lbl.place(x=113, y=15)

# Buttons in the main screen
pause_btn = Button(button_frame, text='Pause', bg='Aqua', font=("Georgia", 13), width=6,
                   command=lambda: pause_song(song_status, progress_bar))
pause_btn.place(x=15, y=40)

stop_btn = Button(button_frame, text='Stop', bg='Aqua', font=("Georgia", 13), width=6,
                  command=lambda: stop_song(song_status, progress_bar))
stop_btn.place(x=105, y=40)

play_btn = Button(button_frame, text='Play', bg='Aqua', font=("Georgia", 13), width=6,
                  command=lambda: play_song(current_song, playlist, song_status, progress_bar))
play_btn.place(x=195, y=40)

resume_btn = Button(button_frame, text='Resume', bg='Aqua', font=("Georgia", 13), width=6,
                    command=lambda: resume_song(song_status, playlist, progress_bar))
resume_btn.place(x=285, y=40)

load_btn = Button(button_frame, text='Add Your Playlist', bg='Aqua', font=("Georgia", 13), width=35,
                  command=lambda: load(playlist))
load_btn.place(x=10, y=125)

# Label at the bottom that displays the state of the music
Label(root, textvariable=song_status, bg='cyan', font=('Times', 9), justify=LEFT).pack(side=BOTTOM, fill=X)

# Finalizing the GUI
root.update()
root.mainloop()
