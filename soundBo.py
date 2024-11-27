import rumps, time, osascript, shutil, os
from tkinter import filedialog, Tk
from os.path import isfile, join
from pygame import mixer

APP_NAME = "soundBo"
DEFAULT_VOL = 30

# List of special clickable functions in the menu
CLICKFUNCTS = ["+ Add Sound"]



# add the ability to quit app
# test .app - ability, probably the files are gonna be screwed up



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
    file_path = f"sounds/{sound_name}.mp3"
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"ERROR - UNHANDLED DELETION: {file_path} does not exist.")

def add_sound(sound_name: str, initing: bool = False):
    new_path = f"sounds/{sound_name}.mp3"

    if not initing:
        source_path = upload_mp3_file()
        shutil.copyfile(source_path, new_path)

    new_sound = SoundOption(sound_name, new_path)
    sound_menu = rumps.MenuItem(title=new_sound.name)

    play_button = rumps.MenuItem(title="Play", callback=lambda _: new_sound.play())
    delete_button = rumps.MenuItem(title="Delete", callback=lambda _: new_sound.delete_self())

    sound_menu.add(play_button)
    sound_menu.add(delete_button)

    new_sound.menu = sound_menu
    return sound_menu

def init_sound_menu(app_instance):
    for item in list(app_instance.menu.keys()):
        if item not in CLICKFUNCTS:
            del app_instance.menu[item]

    # Add existing sounds to the menu
    starter_sounds = [f for f in os.listdir("sounds") if isfile(join("sounds", f))]
    for sound in starter_sounds:
        name = sound.split(".")[0]
        app_instance.menu.add(add_sound(name, initing=True))



# Main app class
class SoundBo(rumps.App):
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
        sound_name = "bingus"  # Replace with input logic if needed
        add_sound(sound_name)
        self.refresh_menu()

    @rumps.clicked("Remove App")
    def removeApp(self, _):

        kill = rumps.alert(title="Remove App?", message="Are you sure you want to remove this app?", ok="Keep", cancel="Remove", icon_path="logo.icns")

        if kill == 0:
            kill = rumps.alert(title="Remove App?", message="Are you extra-super-sure?", ok="no...", cancel="YES!", icon_path="logo.icns")

            if kill == 0:
                rumps.quit_application()

        


if __name__ == "__main__":
    file_path = filedialog.askopenfilename(
        title="CLICK CANCEL!! CLOSE THIS WINDOW!!",
        filetypes=[("Bingus Files", "*.bingus")]
    )
    SoundBo().run()