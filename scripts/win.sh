pyinstaller gui.py --windowed --onefile --add-data 'data/captcha.wav;data/captcha.wav' --add-data 'data/logout.wav;data/logout.wav' --additional-hooks-dir './hooks' --hiddenimport 'cairosvg' --hiddenimport 'cairocffi' -y -n 'Book My Slot' --icon 'data/icons/vaccine.ico'
