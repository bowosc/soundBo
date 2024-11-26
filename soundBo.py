import rumps, time, osascript, shutil
import tkinter as tk
from tkinter import filedialog
from pygame import mixer

APP_NAME = "soundBo"


def playSound(pathToSound: str, name: str, timeDuration: float = None, fade: int = 0):

    code, pastvol, err = osascript.run("output volume of (get volume settings)")
    osascript.run("set volume output volume 100")

    mixer.init()
    mixer.music.load(pathToSound)
    mixer.music.play(fade_ms = fade)

    if timeDuration:
        time.sleep(timeDuration)
        mixer.music.stop()
    
    rumps.alert(f"Playing {name}...", ok="Stop", icon_path="icon.png") # pauses program until alert is closed

    # after the alert is closed:

    mixer.music.stop()
    print(pastvol)
    osascript.run(f"set volume output volume {pastvol}")

    


def uploadMP3File() -> str:
    '''
    Opens finder window for file selection, only allowing
    the selection of .mp3 files. 
    
    Returns filepath.
    '''
    root=tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename(
        title = "Select a .mp3 file, or drag-and-drop one into this window!",
        filetypes = [("MP3 Files", "*.mp3")]
        )

    print('File path: ',filePath)
    return filePath





class soundOption():
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.fileType = ".mp3"

    def play(self):
        playSound(self.path, self.name)
    
    

class soundBo(rumps.App):
    def __init__(self):
        super(soundBo, self).__init__(name=APP_NAME, icon='icon.png', quit_button=None)
        self.menu = ["+ Add Sound", "Curb", "Sax", "Yeah"]

    @rumps.clicked("Curb")
    def curb(self, _):
        playSound(pathToSound = "sounds/curb.mp3", name = "Curb")

    @rumps.clicked("Sax")
    def sax(self, _):
        playSound(pathToSound = "sounds/sax.mp3", name = "Sax")

    @rumps.clicked("Yeah")
    def yeah(self, _):
        playSound(pathToSound = "sounds/yeah.mp3", name = "Yeah")

    @rumps.clicked("+ Add Sound")
    def clickAddSound(self, _):


        ###TEST CODE REMOVE WHEN DONE###
        soundName = "bingus"
        ###TEST CODE REMOVE WHEN DONE###




        path = uploadMP3File()
        newpath = f"sounds/{soundName}.mp3"

        shutil.copyfile(path, newpath)
        
        newSound = soundOption(soundName, newpath)

        fileButton = rumps.MenuItem(title = newSound.name, callback=lambda _: newSound.play())
        
        print("new sound: " + fileButton.title)
        self.menu.add(fileButton)

        # make copy of file, put it in here
        return

    



if __name__ == "__main__":
    uploadMP3File()
    soundBo().run()