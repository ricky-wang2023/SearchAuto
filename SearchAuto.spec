# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['searchAuto.py'],
    pathex=[],
    binaries=[],
    datas=[('README.md', '.'), ('requirements.txt', '.'), ('ai_search.py', '.'), ('ai_search_light.py', '.'), ('check_threads.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'sentence_transformers', 'transformers', 'chromadb', 'huggingface_hub'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SearchAuto',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
