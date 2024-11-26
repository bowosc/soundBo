import rumps, time, osascript, shutil, os
import tkinter as tk
from os.path import isfile, join
from tkinter import filedialog
from pygame import mixer

APP_NAME = "soundBo"
DEFAULT_VOL = 30

class soundOption():
    def __init__(self, name: str, path: str, main_menu: rumps.MenuItem):
        self.name = name
        self.path = path
        self.main_menu = main_menu  # Reference to the app's main menu
        self.menu_key = None        # Will store a reference to the sound's submenu
        self.fileType = ".mp3"

    def getName(self):
        return self.name

    def play(self, volume: int = DEFAULT_VOL, timeduration: int = None, fade: int = 0):
        playSound(self.path, self.name, volume, timeduration, fade)

    def deleteSelf(self):
        # Delete the sound file
        removeFile(self.name)
        
        # Remove the sound's submenu from the main menu if it exists
        if self.menu_key and self.menu_key in self.main_menu:
            self.main_menu.pop(self.menu_key)
            print(f"Menu item '{self.name}' removed from the menu.")
        else:
            print(f"Menu item for '{self.name}' not found.")
    

def playSound(pathToSound: str, name: str, volume: int = DEFAULT_VOL, timeDuration: float = None, fade: int = 0):
    code, pastvol, err = osascript.run("output volume of (get volume settings)")
    osascript.run(f"set volume output volume {volume}")

    mixer.init()
    mixer.music.load(pathToSound)
    mixer.music.play(fade_ms=fade)

    if timeDuration:
        time.sleep(timeDuration)
        mixer.music.stop()
    else:
        rumps.alert(f"Playing {name}...", ok="Stop", icon_path="icon.png")

    mixer.music.stop()
    osascript.run(f"set volume output volume {pastvol}")


def uploadMP3File() -> str:
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes("-topmost", True)

    filePath = filedialog.askopenfilename(
        title="Select a .mp3 file, or drag-and-drop one into this window!",
        filetypes=[("MP3 Files", "*.mp3")]
    )
    
    root.destroy()
    return filePath


def removeFile(soundName: str):
    filePath = f"sounds/{soundName}.mp3"

    if os.path.exists(filePath):
        os.remove(filePath)
        print(f"{filePath} has been deleted.")
    else:
        print(f"{filePath} does not exist.")


def addSound(soundName: str, main_menu: rumps.MenuItem, initing: bool = False):
    newpath = f"sounds/{soundName}.mp3"

    if initing:
        print("Initializing file " + soundName)
    else:
        path = uploadMP3File()
        shutil.copyfile(path, newpath)

    newSound = soundOption(soundName, newpath, main_menu)

    # Create a fresh submenu for each sound
    soundMenu = rumps.MenuItem(title=newSound.name)

    # Create new instances of Play and Delete buttons
    playButton = rumps.MenuItem(title="Play", callback=lambda _: newSound.play())
    deleteButton = rumps.MenuItem(
        title="Delete",
        callback=lambda _: newSound.deleteSelf()
    )

    # Add the Play and Delete buttons to the submenu
    soundMenu.add(playButton)
    soundMenu.add(deleteButton)

    # Store reference to the submenu key in the soundOption instance
    newSound.menu_key = newSound.name

    # Add the submenu to the main menu using a unique key (soundName)
    main_menu.add(soundMenu)
    
    return soundMenu


class soundBo(rumps.App):
    def __init__(self):
        super(soundBo, self).__init__(name=APP_NAME, icon='icon.png', quit_button=None)

        # Initiate any sound effects that are already in the sounds file
        starterSounds = [f for f in os.listdir("sounds") if isfile(join("sounds", f))]  
        
        for sound in starterSounds:
            name = sound.split(".")[0]
            self.menu.add(addSound(soundName=name, main_menu=self.menu, initing=True))

    @rumps.clicked("+ Add Sound")
    def clickAddSound(self, _):
        soundName = "bingus"
        fileButton = addSound(soundName, main_menu=self.menu)
        self.menu.add(fileButton)

if __name__ == "__main__":

    filePath = filedialog.askopenfilename(
            title = "Select any file...",
            )
    

    soundBo().run()