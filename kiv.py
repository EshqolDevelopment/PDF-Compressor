import os


def file(path):
    app_data_path = os.getenv('APPDATA') + '\\' + "PDF Compressor Pro"
    return f"{app_data_path}\\{path}".replace("\\", "/")


kv = f"""

Screen:
    id: Home
    
    Text:
        id: title
        text: "Drag your pdf files here or choose them directly through the button below"
        x, y = 0.5, 0.8
        font_size: 22
        bold: True
        
    Img:
        source: "drag_and_drop.png"
        size_hint_x: 0.5
        x, y = 0.5, 0.48
        
    Button:
        x, y = 0.5, 0.48
        size_hint_x: 0.5
        size_hint_y: 0.45
        opacity: 0
        on_press: app.choose_file()
        
    Text:
        text: "\\n".join(app.file_names).replace('@', '   |   ')
        x, y = 0.5, 0.16
        
    BtnIcon:
        text: "Output folder"
        icon: "folder-outline"
        x, y = 0.12, 0.5
        on_press: app.select_output_dir()
    
    
    Text:
        halign: "left"
        id: output_dir
        text: app.output_dir
        # x, y = 0.12, 0.42
        pos_hint: {{'x': 0.015, "center_y": 0.42}}
        font_size: 13
               
        
    BtnIcon:
        text: "Compress"
        icon: "arrow-collapse-vertical"
        x, y = 0.88, 0.5
        md_bg_color: 0, 0.8, 1, 1
        on_release: app.compress_files()
        
        
    BtnIcon:
        id: open
        icon: "file-pdf-box"
        text: "open compressed files"
        x, y = 0.87, 0.13
        opacity: 0
        on_press: app.open_folder()
        
        
"""