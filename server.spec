# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['build_pyd\\server.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['warnings', 'random', 'os', 'datetime', 'time', 're', 'threading', 'ctypes', 'ctypes.wintypes', 'comtypes', 'comtypes.client', 'PIL', 'typing', 'win32clipboard', 'win32gui', 'win32api', 'win32con', 'pyperclip', 'psutil', 'shutil', 'winreg', 'logging', 'PIL.ImageGrab', 'win32process', 'comtypes.stream'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='server',
)
