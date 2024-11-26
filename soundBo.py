import rumps, time, osascript, shutil, os
import tkinter as tk
from os.path import isfile, join
from tkinter import filedialog
from pygame import mixer

APP_NAME = "soundBo"
DEFAULT_VOL = 30

# add close app button
# allow user to remove sounds

class soundOption():
    def __init__(self, name: str, path: str, menu: rumps.MenuItem = None):
        self.name = name
        self.path = path
        self.menu = menu
        self.fileType = ".mp3"

    def getName(self):
        return self.name

    def play(self, volume: int = DEFAULT_VOL, timeduration: int = None, fade: int = 0):
        playSound(self.path, self.name, volume, timeduration, fade)

    def deleteSelf(self):
        
        print(self.menu)
        if self.name in self.menu:
            self.menu.pop(self.name)
        else:
            print(f"Menu item for {self.name} not found.")
        
        removeFile(self.name)
    

def playSound(pathToSound: str, name: str, volume: int = DEFAULT_VOL, timeDuration: float = None, fade: int = 0):
    '''
    Play sound until stopped. Current system volume will be restored after sound is stopped.

    Parameters :

    pathToSound: In-app path to the sound, should always be within the /sounds folder.

    name: Name of sound within the rumps app GUI.

    volume: 0-100 volume to play sound at. Defaults to 100.

    timeDuration: Time to wait before automatically stopping sound. If not set, sound will stop playing when window is closed.

    fade: pygame.mixer fade effect.
    '''

    code, pastvol, err = osascript.run("output volume of (get volume settings)")
    osascript.run(f"set volume output volume {volume}")

    mixer.init()
    mixer.music.load(pathToSound)
    mixer.music.play(fade_ms = fade)

    if timeDuration:
        time.sleep(timeDuration)
        mixer.music.stop()
    else:
        rumps.alert(f"Playing {name}...", ok="Stop", icon_path="icon.png") # pauses program until alert is closed


    # after the alert is closed
    mixer.music.stop()

    osascript.run(f"set volume output volume {pastvol}")


def uploadMP3File() -> str:
    '''
    Opens finder window for file selection, only allowing
    the selection of .mp3 files. 
    
    Returns filepath.
    '''

    root=tk.Tk()
    root.withdraw()

    root.lift()
    root.attributes("-topmost", True)

    filePath = filedialog.askopenfilename(
        title = "Select a .mp3 file, or drag-and-drop one into this window!",
        filetypes = [("MP3 Files", "*.mp3")]
        )
    
    root.destroy()
    # make sure the window is closed

    return filePath
    
def removeFile(soundName: str):
    filePath = f"sounds/{soundName}.mp3"

    if os.path.exists(filePath):
        os.remove(filePath)
        print(f"{filePath} has been deleted.")
    else:
        print(f"{filePath} does not exist.")

def addSound(soundName: str, initing: bool = False):

    newpath = f"sounds/{soundName}.mp3"

    if initing:
        print("initalizing file " + soundName)
    else:
        path = uploadMP3File()

        shutil.copyfile(path, newpath)

    newSound = soundOption(soundName, newpath)

    # Create a submenu for each sound
    soundMenu = rumps.MenuItem(title=newSound.name)

    # Add play and delete options to the submenu
    playButton = rumps.MenuItem(title="Play", callback=lambda _: newSound.play())
    deleteButton = rumps.MenuItem(title="Delete", callback=lambda _: newSound.deleteSelf())

    soundMenu.add(playButton)
    soundMenu.add(deleteButton)

    
    newSound.menu = soundMenu
    return soundMenu



def buttonClicked(sound: soundOption):
    sound.play()

class soundBo(rumps.App):
    def __init__(self):
        super(soundBo, self).__init__(name=APP_NAME, icon='icon.png', quit_button=None)


        # initate any sound effects that are already in the sounds file
        starterSounds = [f for f in os.listdir("sounds") if isfile(join("sounds", f))]  
        

        for sound in starterSounds:
            name = sound.split(".")[0]

            self.menu.add(addSound(soundName=name, initing=True))

            '''newsound = soundOption(
                    name = name,
                    path = f"sounds/{sound}"
                    )
            
            def create_button_callback(sound_instance):

                return lambda _: buttonClicked(sound_instance)
            
            fileButton = rumps.MenuItem(title = newsound.getName(), callback=create_button_callback(newsound))
            self.menu.add(fileButton)'''
            

    @rumps.clicked("+ Add Sound")
    def clickAddSound(self, _):

        ###TEST CODE EDIT WHEN DONE###
        soundName = "bingus"
        ###TEST CODE EDIT WHEN DONE###
        
        fileButton = addSound(soundName)
        self.menu.add(fileButton)

    



if __name__ == "__main__":

    filePath = filedialog.askopenfilename(
            title = "Select any file...",
            )
    

    soundBo().run()