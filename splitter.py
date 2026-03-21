import flet as ft
import os
from glob import glob
import sys

def resource_path(relative_path):
    """Get absolute path to resource for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

CONFIG_FILE = "splitter_config.txt"

def save_folder(path):
    with open(CONFIG_FILE, "w") as f:
        f.write(path)

def load_folder():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    return os.path.expanduser("~\\Documents\\Codes")

def split_code(code):
    """Split a code into two halves with line break"""
    length = len(code)
    half = length // 2
    first_half = code[:half]
    second_half = code[half:]
    return f"{first_half}\n{second_half}"

def main(page: ft.Page):
    page.title = "Voddic Code Splitter Software"
    page.window_width = 950
    page.window_height = 720
    page.bgcolor = "#f4f7fb"
    page.scroll = ft.ScrollMode.AUTO
    
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    result = ft.Text(size=16)
    folder_status = ft.Text(weight="bold")
    
    progress = ft.ProgressBar(
        width=650,
        value=0,
        color="green",
        bgcolor="#d9d9d9",
        visible=False
    )

    folder_input = ft.TextField(
        label="Select Folder with TXT Files",
        width=550,
        value=load_folder(),
        read_only=False,
    )

    output_filename = ft.TextField(
        label="Output File Name",
        width=400,
        value="split_codes.txt",
        hint_text="split_codes.txt"
    )

    # Preview area
    preview_container = ft.Container(
        bgcolor=ft.Colors.GREY_100,
        border_radius=10,
        padding=15,
        width=700,
        visible=False,
        content=ft.Column([
            ft.Text("Preview (first 1 codes):", weight="bold", size=14),
            ft.Divider(height=5),
            ft.Text("", size=12, font_family="monospace"),
        ])
    )

    # ---------------- File Detection ----------------
    def get_txt_files(folder):
        files = glob(os.path.join(folder, "*.txt"))
        # Exclude the output file if it exists
        out_name = output_filename.value.strip() or "split_codes.txt"
        if not out_name.endswith('.txt'):
            out_name += '.txt'
        files = [f for f in files if os.path.basename(f) != out_name]
        return files

    def update_folder_status(e=None):
        folder = folder_input.value.strip()
        if not os.path.isdir(folder):
            folder_status.value = "❌ Invalid Folder"
        else:
            files = get_txt_files(folder)
            if files:
                file_count = len(files)
                total_size = sum(os.path.getsize(f) for f in files) / 1024
                folder_status.value = f"🟢 Found {file_count} TXT files ({total_size:.1f} KB total)"
                
                # Show preview from first file
                if files:
                    with open(files[0], 'r', encoding='utf-8') as f:
                        preview_lines = []
                        for i, line in enumerate(f):
                            if i >= 1:
                                break
                            code = line.strip()
                            if code:
                                split = split_code(code)
                                preview_lines.append(f"Original: {code}")
                                preview_lines.append(f"Split:    {split.replace(chr(10), ' ⬇ ')}")
                        
                        preview_container.visible = True
                        preview_container.content.controls[2].value = "\n".join(preview_lines)
            else:
                folder_status.value = "⚠ No TXT files found in folder"
                preview_container.visible = False
        page.update()

    # ---------------- Processing ----------------
    def split_files(e):
        folder = folder_input.value.strip()
        
        if not os.path.isdir(folder):
            result.value = "❌ Invalid folder"
            page.update()
            return
        
        files = get_txt_files(folder)
        if not files:
            result.value = "❌ No TXT files found in folder"
            page.update()
            return
        
        # Get output filename
        out_name = output_filename.value.strip()
        if not out_name:
            out_name = "split_codes.txt"
        if not out_name.endswith('.txt'):
            out_name += '.txt'
        
        output_path = os.path.join(folder, out_name)
        
        # Show progress
        progress.visible = True
        progress.value = 0
        result.value = f"⏳ Splitting codes in {len(files)} files..."
        page.update()
        
        try:
            total_codes = 0
            file_count = len(files)
            
            with open(output_path, 'w', encoding='utf-8') as outfile:
                
                for idx, file_path in enumerate(sorted(files)):
                    file_codes = 0
                    
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        for line in infile:
                            code = line.strip()
                            if code:
                                # Split the code and write with line break
                                split_result = split_code(code)
                                outfile.write(split_result + '\n')
                                file_codes += 1
                                total_codes += 1
                    
                    progress.value = (idx + 1) / file_count
                    page.update()
            
            progress.visible = False
            result.value = (
                f"✅ Split Complete!\n\n"
                f"📁 Files processed: {file_count}\n"
                f"📝 Original codes: {total_codes}\n"
                f"✂️ Each code split into 2 lines\n"
                f"💾 Saved to:\n{output_path}\n\n"
                f"Example:\n"
                f"Original: 7Y355Y2TEU → Split:\n"
                f"7Y355\nY2TEU"
            )
            
        except Exception as e:
            progress.visible = False
            result.value = f"❌ Error: {str(e)}"
        
        page.update()

    # Initial status update
    update_folder_status()

    # ---------------- HEADER ----------------
    header = ft.Container(
        bgcolor="#0F0F0F",
        padding=15,
        width=900,
        border_radius=10,
        content=ft.Row(
            [
                ft.Image(
                    src=resource_path("voddic_logo.png"),
                    width=80
                ),
                ft.Column(
                    [
                        ft.Text(
                            "Voddic Code Splitter",
                            color="white",
                            size=24,
                            weight="bold"
                        ),
                        ft.Text(
                            "Split Each Code Into Two Lines",
                            color="white"
                        )
                    ],
                    spacing=2
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # ---------------- MAIN CARD ----------------
    main_card = ft.Container(
        bgcolor="white",
        border_radius=10,
        padding=30,
        width=700,
        content=ft.Column(
            [
                ft.Text("Split Codes in Half", weight="bold", size=20),
                ft.Container(height=10),
                
                ft.Row(
                    [
                        ft.Text("📁", size=30),
                        ft.Text("Step 1: Select your folder", size=16, weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                folder_input,
                
                ft.Container(height=15),
                
                ft.Row(
                    [
                        ft.Text("✂️", size=30),
                        ft.Text("Step 2: Name output file", size=16, weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                output_filename,
                
                ft.Container(height=20),
                
                ft.ElevatedButton(
                    "✂️ SPLIT ALL CODES",
                    on_click=split_files,
                    style=ft.ButtonStyle(
                        color="white",
                        bgcolor="#003366",
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    width=400,
                    height=50,
                ),
                
                ft.Container(height=10),
                ft.Text(
                    "⚠️ Each code is split in half: 'ABCDEF' → 'ABC\\nDEF'",
                    size=12,
                    color=ft.Colors.GREY_700,
                    italic=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    result_box = ft.Container(
        bgcolor="white",
        padding=20,
        border_radius=10,
        width=720,
        content=result
    )

    # ---------------- FOOTER ----------------
    footer = ft.Container(
        bgcolor="#003366",
        padding=20,
        width=900,
        border_radius=10,
        margin=ft.margin.only(top=15, bottom=10),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=5,
            color=ft.Colors.BLUE_GREY_300,
            offset=ft.Offset(0, 2),
        ),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Image(
                                    src=resource_path("voddic_logo.png"),
                                    width=45,
                                    height=45,
                                ),
                                ft.Container(width=10),
                                ft.Text(
                                    "INTERNAL USE ONLY",
                                    color="white",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    italic=True,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Container(
                            bgcolor="white",
                            border_radius=20,
                            padding=ft.padding.only(left=12, right=12, top=5, bottom=5),
                            content=ft.Text(
                                "CODE SPLITTER",
                                color="#003366",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(color="white", height=15, thickness=1),
                
                ft.Container(
                    bgcolor="white",
                    border_radius=10,
                    padding=15,
                    content=ft.Column(
                        [
                            ft.Text(
                                "CREDITS & SUPERVISION",
                                color="#003366",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Divider(color="#003366", height=10, thickness=1),
                            
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text(
                                                "👑 Voddic LTD",
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                "https://voddic.com.ng",
                                                size=14,
                                                weight=ft.FontWeight.W_500,
                                            ),
                                            ft.Text(
                                                "voddic28@gmail.com",
                                                size=13,
                                                color=ft.Colors.GREY_700,
                                            ),
                                        ],
                                        spacing=5,
                                        horizontal_alignment=ft.CrossAxisAlignment.START,
                                    ),
                                    ft.VerticalDivider(color="#003366", width=20),
                                    ft.Column(
                                        [
                                            ft.Text(
                                                "🔧 WhatsApp Us",
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                 "+234 (812) 763 3556",
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                                color="#003366",
                                            ),
                                            ft.Text(
                                                "call us: +234 (812) 763 3556.",
                                                size=13,
                                                color=ft.Colors.GREY_700,
                                            ),
                                        ],
                                        spacing=5,
                                        horizontal_alignment=ft.CrossAxisAlignment.START,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            ),
                        ],
                        spacing=10,
                    ),
                ),
                
                ft.Container(height=5),
                
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    "Software Version: 1.0",
                                    color="white",
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    "Build Date: March 2026",
                                    color="white",
                                    size=13,
                                ),
                            ],
                            spacing=2,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "All Rights Reserved",
                                    color="white",
                                    size=12,
                                    opacity=0.9,
                                ),
                                ft.Text(
                                    "© Voddic LTD",
                                    color="white",
                                    size=12,
                                    opacity=0.9,
                                ),
                            ],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=8,
        ),
    )

    # Add all components to page
    page.add(
        header,
        ft.Container(height=10),
        folder_status,
        preview_container,
        ft.Container(height=10),
        main_card,
        ft.Container(height=10),
        progress,
        result_box,
        ft.Row(
            [
                ft.ElevatedButton(
                    "💾 Save Folder",
                    on_click=lambda e: save_folder(folder_input.value)
                ),
                ft.OutlinedButton(
                    "🔄 Refresh",
                    on_click=update_folder_status
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        footer,
    )

ft.app(target=main)