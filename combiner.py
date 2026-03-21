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

CONFIG_FILE = "combiner_config.txt"

def save_folder(path):
    with open(CONFIG_FILE, "w") as f:
        f.write(path)

def load_folder():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    return os.path.expanduser("~\\Documents\\Codes")

def main(page: ft.Page):
    page.title = "Frigoglass Code Combiner"
    page.window_width = 950
    page.window_height = 700
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
        label="Output File Name (optional)",
        width=400,
        value="combined_codes.txt",
        hint_text="combined_codes.txt"
    )

    # ---------------- File Detection ----------------
    def get_txt_files(folder):
        files = glob(os.path.join(folder, "*.txt"))
        return files

    def update_folder_status(e=None):
        folder = folder_input.value.strip()
        if not os.path.isdir(folder):
            folder_status.value = "❌ Invalid Folder"
        else:
            files = get_txt_files(folder)
            if files:
                file_count = len(files)
                total_size = sum(os.path.getsize(f) for f in files) / 1024  # KB
                folder_status.value = f"🟢 Found {file_count} TXT files ({total_size:.1f} KB total)"
            else:
                folder_status.value = "⚠ No TXT files found in folder"
        page.update()

    # ---------------- Processing ----------------
    def combine_files(e):
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
            out_name = "combined_codes.txt"
        if not out_name.endswith('.txt'):
            out_name += '.txt'
        
        output_path = os.path.join(folder, out_name)
        
        # Show progress
        progress.visible = True
        progress.value = 0
        result.value = f"⏳ Combining {len(files)} files..."
        page.update()
        
        try:
            total_lines = 0
            file_count = len(files)
            combined_lines = set()  # Use set to remove duplicates
            duplicate_count = 0
            
            # Process each file
            for idx, file_path in enumerate(files):
                with open(file_path, 'r', encoding='utf-8') as infile:
                    lines = infile.readlines()
                    for line in lines:
                        code = line.strip()
                        if code:  # Skip empty lines
                            if code in combined_lines:
                                duplicate_count += 1
                            else:
                                combined_lines.add(code)
                                total_lines += 1
                
                # Update progress
                progress.value = (idx + 1) / file_count
                page.update()
            
            # Write combined file
            with open(output_path, 'w', encoding='utf-8') as outfile:
                for code in sorted(combined_lines):  # Sort for consistency
                    outfile.write(code + '\n')
            
            progress.visible = False
            result.value = (
                f"✅ Combination Complete!\n\n"
                f"📁 Files processed: {file_count}\n"
                f"📝 Total unique codes: {total_lines}\n"
                f"🔄 Duplicates removed: {duplicate_count}\n"
                f"💾 Saved to:\n{output_path}"
            )
            
        except Exception as e:
            progress.visible = False
            result.value = f"❌ Error: {str(e)}"
        
        page.update()

    # Initial status update
    update_folder_status()

    # ---------------- HEADER ----------------
    header = ft.Container(
        bgcolor="#003366",
        padding=15,
        width=900,
        border_radius=10,
        content=ft.Row(
            [
                ft.Image(
                    src=resource_path("frigoglass_logo.jpg"),
                    width=80
                ),
                ft.Column(
                    [
                        ft.Text(
                            "Frigoglass Code Combiner",
                            color="white",
                            size=24,
                            weight="bold"
                        ),
                        ft.Text(
                            "Combine Multiple TXT Files Into One",
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
                ft.Text("Combine All Codes", weight="bold", size=20),
                ft.Container(height=10),
                
                ft.Row(
                    [
                        ft.Icon(ft.icons.FOLDER_OPEN, color="#003366", size=30),
                        ft.Text("Step 1: Select your folder", size=16, weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                folder_input,
                
                ft.Container(height=15),
                
                ft.Row(
                    [
                        ft.Icon(ft.icons.DRIVE_FILE_MOVE, color="#003366", size=30),
                        ft.Text("Step 2: Name your combined file", size=16, weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                output_filename,
                ft.Text("(Leave as default for 'combined_codes.txt')", size=12, color=ft.Colors.GREY_700),
                
                ft.Container(height=20),
                
                ft.ElevatedButton(
                    "🔗 COMBINE ALL FILES",
                    on_click=combine_files,
                    style=ft.ButtonStyle(
                        color="white",
                        bgcolor="#003366",
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    width=400,
                    height=50,
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
                                    src=resource_path("frigoglass_logo.jpg"),
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
                                "FILE COMBINER",
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
                                                "👑 Crown Product Ijebu Ode",
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                "Electrical Department",
                                                size=14,
                                                weight=ft.FontWeight.W_500,
                                            ),
                                            ft.Text(
                                                "Development Team",
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
                                                "🔧 Technical Supervision",
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                "Engr. Ewan Ogbeide",
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                                color="#003366",
                                            ),
                                            ft.Text(
                                                "Project Lead & Supervisor",
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
                                    "© Frigoglass Industries Nigeria Ltd",
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