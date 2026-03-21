🔧 Code Splitter v1.0
Split Codes in Half for Excel Label Printing
📌 Overview
Code Splitter is a desktop application that automatically splits promotional codes into two equal halves, making them ready for Excel label printing. Instead of manually copying codes to Excel and dragging formulas, this tool does it instantly—even for millions of codes.

🎯 The Problem It Solves
Manual Process (Before):
Open original code file in Notepad

Copy all codes (thousands/millions of lines)

Open Microsoft Excel

Paste all codes into a column

Enter formula: =LEFT(A1,INT(LEN(A1)/2)) & CHAR(10) & RIGHT(A1,LEN(A1)-INT(LEN(A1)/2))

Drag formula down to apply to all rows

Copy the split results

Open new Notepad file

Paste split codes

Save with new filename

Time: 30-60 minutes for millions of codes
Risk: Formula errors, accidental deletions, formatting issues

With Code Splitter:
Place all code files in a folder

Copy folder path

Paste path into the app

Click "SPLIT ALL CODES"

Time: Less than 30 seconds
Risk: None—automated and accurate

✨ How It Works
The app applies the Excel formula logic directly to your codes:

Excel Formula Equivalent:
excel
=LEFT(A1,INT(LEN(A1)/2)) & CHAR(10) & RIGHT(A1,LEN(A1)-INT(LEN(A1)/2))
Example:
Original Code	Split Result
7Y355Y2TEU	7Y355
Y2TEU
3NFX5KX6EP	3NFX5
KX6EP
8YJJYC333W	8YJJY
C333W
Each code becomes two lines in the output file—perfect for Excel's "Wrap Text" feature when printing labels.

📦 Features
✅ Batch Processing – Process all .txt files in a folder at once

✅ Preserves Order – Codes remain in original sequence

✅ Custom Output Name – Choose your own filename

✅ Progress Tracking – Real-time progress bar for large files

✅ Folder Memory – Remembers your last used folder

✅ Professional UI – Clean, intuitive interface with company branding

✅ Scrollable Interface – Handles any screen size

✅ Standalone Executable – No Python installation required



🚀 Download & Installation
Windows Executable (Recommended)
Download Code_Splitter_v1.0.exe from the Releases section

Double-click to run (no installation required)

The app will create a splitter_config.txt file in the same folder to remember your settings

System Requirements
Windows 7, 8, 10, or 11

50 MB free disk space

No additional software or dependencies required

📖 How to Use
Step-by-Step Guide:
Prepare Your Files

Place all .txt files containing codes in one folder

Each file should have one code per line

Launch the App

Double-click Code_Splitter_v1.0.exe

Select Folder

Click "Browse" or paste your folder path

The app will show how many files and total size

Name Output File

Default: split_codes.txt

Change if you want a different filename

Split!

Click "SPLIT ALL CODES"

Watch the progress bar as files are processed

Output file is created in the same folder

Use in Excel

Open the output file in Notepad or Excel

Each code appears as two lines

Enable "Wrap Text" in Excel cells for proper display

🔧 Technical Details
Input Format
Files must be .txt with one code per line

Codes can be any length (odd/even both work)

Empty lines are automatically skipped

Output Format
Same folder as input files

Filename: split_codes.txt (or your custom name)

Each code split into two lines with \n line break

Performance
Tested with 5 million codes

Processing time: ~30 seconds per million codes

Memory efficient (streaming, not loading all at once)

❓ Frequently Asked Questions
Q: What if codes have odd length?
A: The split uses integer division: len(code) // 2. For example, 9-character code: first half = 4 chars, second half = 5 chars.

Q: Can I split files in subfolders?
A: Currently only processes files in the selected folder. Subfolders are not processed automatically.

Q: Does it modify original files?
A: No! Original files remain untouched. A new output file is created.

Q: Can I use it on macOS/Linux?
A: The executable is Windows-only, but the Python source code can run on any platform with Python installed.

Q: What happens if the output file already exists?
A: It will be overwritten. The app automatically skips the output file when processing.

🛠️ Development
Build from Source
bash
# Clone repository
git clone https://github.com/yAminco6/free-to-use-softwares

# Install dependencies
pip install flet

# Run
python splitter.py

# Build executable
pyinstaller --onefile --noconsole --icon=assets/icon.ico --add-data "assets/logo.jpg;assets" splitter.py
Technology Stack
Framework: Flet (Python UI framework)

Build Tool: PyInstaller

Target Platform: Windows (Android APK also available in separate release)

📝 Version History
v1.0 (March 2026)
Initial release

Batch file processing

Progress bar with real-time updates

Persistent folder settings

Professional UI with company branding

👥 Credits
Developed by: Voddic LTD - Software Department
Supervised by: Israel-Collins O.C
Contact: voddic28@gmail.com | https://voddic.com.ng

📄 License
Internal Use Only - Voddic Ltd

🤝 Contributing
This tool was built for internal use but open-sourced to help others facing similar challenges. For support or inquiries:

📧 Email: voddic28@gmail.com

📞 WhatsApp: +234 (812) 763 3556

🌐 Website: https://voddic.com.ng

Download the latest release below 👇
