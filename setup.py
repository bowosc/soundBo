from setuptools import setup

APP = ['soundBo.py']

DATA_FILES = []




OPTIONS = {
    'iconfile':'logo.icns',
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps', 'pygame', 'osascript'],
    'includes': ['rumps', 'pygame', 'osascript'],
    'resources': ['sounds/curb.mp3', 'sounds/sax.mp3', 'sounds/yeah.mp3', 'icon.png'], 
    'site_packages': True,
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    setuptools = "==70.3.0"
)

