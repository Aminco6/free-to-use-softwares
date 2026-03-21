@echo off
echo Building Frigoglass Code Splitter...
echo.

pyinstaller --onefile --noconsole --icon=frigoglass.ico --add-data "frigoglass_logo.jpg;." --name "Frigoglass_Code_Splitter" --clean --noconfirm splitter.py

echo.
echo ✅ Build complete!
echo 📁 Executable is in the 'dist' folder
echo 📦 File: dist\Frigoglass_Code_Splitter.exe
pause