from setuptools import setup

APP = ['soundBo.py']

DATA_FILES = [
    ('sounds', ['curb.mp3', 'sax.mp3', 'yeah.mp3']),
    ('', ['icon.png']),
    ]




OPTIONS = {
    'iconfile':'logo.icns',
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps', 'pygame', 'osascript', 'tkinter', 'shutil'],
    'includes': ['rumps', 'pygame', 'osascript', 'tkinter', 'shutil'],
    'resources': DATA_FILES, 
    'site_packages': True,
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    setuptools = "==70.3.0"
)

