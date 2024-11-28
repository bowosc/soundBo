import rumps, time, osascript, shutil, os
from tkinter import filedialog, Tk
from os.path import isfile, join
from pygame import mixer

APP_NAME = "soundBo"
DEFAULT_VOL = 100

# List of basic clickable functions in the menu
CLICKFUNCTS = ["+ Add Sound", "Remove App"]


# TODO
# move pys to .src


# Sound option class
class SoundOption:
    def __init__(self, name: str, path: str, menu: rumps.MenuItem = None):
        self.name = name
        self.path = path
        self.menu = menu
        self.fileType = ".mp3"

    def play(self, volume: int = DEFAULT_VOL, time_duration: int = None, fade: int = 0):
        play_sound(self.path, self.name, volume, time_duration, fade)

    def delete_self(self):
        remove_file(self.name)
        SoundBo.refresh_menu()

# Utility functions
def play_sound(path_to_sound: str, name: str, volume: int = DEFAULT_VOL, time_duration: float = None, fade: int = 0):
    '''
    Play sound until stopped. Current system volume will be restored after sound is stopped.

    Parameters :

    pathToSound: In-app path to the sound, should always be within the /sounds folder.

    name: Name of sound within the rumps app GUI.

    volume: 0-100 volume to play sound at. Defaults to 100.

    timeDuration: Time to wait before automatically stopping sound. If not set, sound will stop playing when window is closed.

    fade: pygame.mixer fade effect.
    '''
    code, past_vol, err = osascript.run("output volume of (get volume settings)")
    osascript.run(f"set volume output volume {volume}")

    mixer.init()
    mixer.music.load(path_to_sound)
    mixer.music.play(fade_ms=fade)

    if time_duration:
        time.sleep(time_duration)
        mixer.music.stop()
    else:
        rumps.alert(f"Playing {name}...", ok="Stop")  # pauses program until alert is closed

    # After the alert is closed
    mixer.music.stop()
    osascript.run(f"set volume output volume {past_vol}")

def upload_mp3_file() -> str:
    '''
    Prompts user to select an mp3 file from the device, through the Finder window. 
    Returns the path to the file selected.
    '''
    root = Tk()
    root.withdraw()
    root.lift()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title="Select a .mp3 file",
        filetypes=[("MP3 Files", "*.mp3")]
    )
    root.destroy()
    return file_path

def remove_file(sound_name: str):
    '''
    Remove a sound file from the sounds directory. 

    sound_name should be the word just after the final "/" but preceding ".mp3" on the file :)
    '''
    file_path = f"sounds/{sound_name}.mp3"
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"ERROR - UNHANDLED DELETION: {file_path} does not exist.")

def add_sound(sound_name: str, initing: bool = False):
    '''
    Prompts user to select an mp3 file to add to the menu.

    Parameters:
    sound_name (str) is the name of the sound file, and its name in the menu. 

    initing (bool) should only be True if used while initiating the app (processing existing sound files).
    '''


    if not initing:
        source_path = upload_mp3_file()

        if sound_name:
            new_path = f"sounds/{sound_name}.mp3"
        else:
            new_path = source_path.split("/")

        shutil.copyfile(source_path, f"sounds/{new_path[len(new_path)-1]}")
        print(new_path)

    new_sound = SoundOption(sound_name, new_path)
    sound_menu = rumps.MenuItem(title=new_sound.name)

    play_button = rumps.MenuItem(title="Play", callback=lambda _: new_sound.play())
    delete_button = rumps.MenuItem(title="Delete", callback=lambda _: new_sound.delete_self())

    sound_menu.add(play_button)
    sound_menu.add(delete_button)

    new_sound.menu = sound_menu
    return sound_menu

def init_sound_menu(app_instance):
    '''
    Essentially refreshes the menu bar list, adding a little entry for each sound that soundBo has an mp3 file for.
    '''
    for item in list(app_instance.menu.keys()):
        if item not in CLICKFUNCTS:
            del app_instance.menu[item]

    # Add existing sounds to the menu
    starter_sounds = [f for f in os.listdir("sounds") if isfile(join("sounds", f))]
    for sound in starter_sounds:
        name = sound.split(".")[0]
        app_instance.menu.add(add_sound(name, initing=True))


class SoundBo(rumps.App):
    '''
    Main app class, manages menu bar options.
    '''
    instance = None  # Class-level reference to the singleton instance

    def __init__(self):
        super(SoundBo, self).__init__(name=APP_NAME, icon='icon.png', quit_button=None)
        SoundBo.instance = self
        self.refresh_menu()

    @staticmethod
    def refresh_menu():
        if SoundBo.instance:
            init_sound_menu(SoundBo.instance)

    @rumps.clicked("+ Add Sound")
    def click_add_sound(self, _):
        add_sound()
        self.refresh_menu()

    @rumps.clicked("Remove App")
    def removeApp(self, _):

        kill = rumps.alert(title="Remove App?", message="Are you sure you want to remove this app?", ok="Keep", cancel="Remove", icon_path="logo.icns")

        if kill == 0:
            kill = rumps.alert(title="Remove App?", message="Are you extra-super-sure?", ok="no...", cancel="YES!", icon_path="logo.icns")

            if kill == 0:
                rumps.quit_application()

        


if __name__ == "__main__":

    # TESTING CODE
    file_path = filedialog.askopenfilename(
        title="CLICK CANCEL!! CLOSE THIS WINDOW!!",
        filetypes=[("Bingus Files", "*.bingus")]
    )
    # REMOVE BEFORE PRODUCTION


    SoundBo().run()