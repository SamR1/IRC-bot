import sys
from cx_Freeze import setup, Executable

options = {
    'build_exe': {
        'include_files': [
            'config.yml.example'
        ],
        'includes': [
            'ircbot',
            'ircsocket',
            'appdirs',
            'packaging',
            'packaging.version',
            'packaging.specifiers',
            'packaging.requirements',
            'six'
        ],
        'path': sys.path + ['classes']
    }
}

executables = [
    Executable('app.py', targetName='IRCBot')
]

setup(
    name="IRCBot",
    version="0.1",
    description="A simple IRC Bot (alpha version)",
    executables=executables,
    options=options
)

