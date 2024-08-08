from PyInstaller.utils.hooks import copy_metadata, collect_all

# Collect all TTS files
datas, binaries, hiddenimports = collect_all('TTS')
