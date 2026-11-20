@echo off
REM Build the standalone Windows exe folder. Run from this repo folder.
python -m pip install -r requirements.txt -r requirements-gpu.txt || exit /b 1
python -m pip install --no-deps -r requirements-vision.txt -r requirements-translate.txt || exit /b 1
python -m pip install pyclipper shapely six || exit /b 1
python -m PyInstaller build_exe.spec --noconfirm || exit /b 1
echo.
echo Done: dist\gta6-clipper\gta6-clipper.exe
