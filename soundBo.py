import rumps, time, osascript
from pygame import mixer

APP_NAME = "soundBo"


# allow uploadable sounds


def playMusic(pathToMusic: str, name: str, timeDuration: float = None, fade: int = 0):

    code, pastvol, err = osascript.run("output volume of (get volume settings)")
    osascript.run("set volume output volume 100")

    mixer.init()
    mixer.music.load(pathToMusic)
    mixer.music.play(fade_ms = fade)

    if timeDuration:
        time.sleep(timeDuration)
        mixer.music.stop()
    
    rumps.alert(f"Playing {name}...", ok="Stop", icon_path="icon.png")

    # Run after the alert is closed:

    mixer.music.stop()
    print(pastvol)
    osascript.run(f"set volume output volume {pastvol}")


class soundBo(rumps.App):
    def __init__(self):
        super(soundBo, self).__init__(name=APP_NAME, icon='icon.png', quit_button=None)
        self.menu = ["Curb", "Sax", "Yeah"]

    @rumps.clicked("Curb")
    def curb(self, _):
        playMusic(pathToMusic = "curb.mp3", name = "Curb")

    @rumps.clicked("Sax")
    def sax(self, _):
        playMusic(pathToMusic = "sax.mp3", name = "Sax")

    @rumps.clicked("Yeah")
    def yeah(self, _):
        playMusic(pathToMusic = "yeah.mp3", name = "Yeah")


if __name__ == "__main__":
    soundBo().run()