# -*- mode: python ; coding: utf-8 -*-
"""Build the Windows .exe folder:  py -m PyInstaller build_exe.spec --noconfirm"""
import shutil
from pathlib import Path
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files

ROOT = Path(SPECPATH)
datas = []

# All pipeline scripts (app.exe runs them from the bundle when given a .py argument).
for p in sorted(ROOT.glob("*.py")):
    datas.append((str(p), "."))

# Files the app and scripts read at runtime.
for name in ("app.html", "channels.txt", "manifest.json", "version.json", "brand.example.json",
             "clip_rules.json", "learn_fixture.json", "streamers.json", "themes.json",
             "SKILL.md", "SKILL-REFERENCE.md", "README.md", "CHANGELOG.md", "NOTICE.md", "LICENSE"):
    p = ROOT / name
    if p.is_file():
        datas.append((str(p), "."))
for folder in ("fonts", "models", "sounds"):
    for p in sorted((ROOT / folder).rglob("*")) if (ROOT / folder).exists() else []:
        if p.is_file():
            datas.append((str(p), str(p.parent.relative_to(ROOT))))

# ffmpeg/ffprobe must be on PATH for every renderer and QC step.
binaries = []
for tool in ("ffmpeg", "ffprobe", "deno"):
    found = shutil.which(tool)
    if found:
        binaries.append((found, "bin"))
# CUDA runtime DLLs used by faster-whisper / ctranslate2 on NVIDIA cards.
for pkg in ("nvidia.cublas", "nvidia.cudnn"):
    try:
        binaries += collect_dynamic_libs(pkg)
    except Exception:
        pass

hiddenimports = [
    "cv2", "numpy", "PIL", "fontTools", "yt_dlp", "yt_dlp.extractor", "yt_dlp.postprocessor",
    "faster_whisper", "ctranslate2", "av", "mediapipe", "streamlink", "onnxruntime",
    "ctranslate2", "rapidocr_onnxruntime", "argostranslate", "websockets", "requests", "tqdm",
    "certifi", "charset_normalizer", "idna", "urllib3", "tkinter",
    "sentencepiece", "pyclipper", "shapely", "six",
]
datas += collect_data_files("rapidocr_onnxruntime")  # ONNX OCR models for vision.py

a = Analysis(
    ["app.py"],
    pathex=[str(ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["torch", "tensorflow", "scipy"],  # matplotlib is a mediapipe dependency
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="gta6-clipper",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="gta6-clipper")
