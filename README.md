# 🎧 Minimalyst

**Minimalyst** is a simple **music player** built with **Python** and **Kivy**, focused on delivering a **minimalistic and retro-inspired experience**. Designed with clean visuals and essential features, it's perfect for those who want to enjoy music distraction-free.

---

## ✨ Features

- 🎶 Plays `.mp3`, `.ogg`, `.wav`
- 🎚️ Volume control
- 🔁 Repeat mode toggle
- 📁 File chooser with path saving (JSON-based)
- 📀 Album cover display
- 🖼️ Progress slider with music sync
- 🎨 **Theme customization:** All visual assets are in the `img/` folder. Replace them to create your own look.
- 💻 Windows executable included (see Releases)

---

## 📸 Screenshot

<img width="957" height="535" alt="Image" src="https://github.com/user-attachments/assets/693677d9-0ad2-47a0-a86e-765afa1fd849" />

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`

### 🧪 Run from source

```bash
git clone https://github.com/your-username/minimalyst.git
cd minimalyst
pip install -r requirements.txt
python main.py
```

---

## 📁 Folder Structure (simplified)

```
minimalyst/
├── gui/
│   ├── minimalyst.kv
│   ├── widgets_config.py
│   └── default_path.json
├── resource/
│   ├── covers/
│   ├── img/
├── default_library/
├── main.py
├── requirements.txt
└── ...
```

---

## 📀 How to Add Album Covers

All album covers are stored in the `resource/covers/` folder. To add a custom cover for an album, follow these steps:

1. Get an image to use as the album cover.
2. Place the image inside the `resource/covers/` folder.
3. Make sure the **image filename matches the album name** exactly as it appears in the music file's metadata.

**Example:**

- Music file: `music.mp3`  
- Its metadata → Album: `Some_Jazz`  
- Then the cover image should be: `Some_Jazz.png` placed in `resource/covers/`

---

## 📦 Packaging

Built using:

```bash
pyinstaller --add-data "default_library;default_library"             --add-data "resource/covers;resource/covers"             --add-data "resource/img;resource/img"             --add-data "gui/minimalyst.kv;gui"             --add-data "gui/default_path.json;gui"             --hidden-import pywintypes             --hidden-import pythoncom             --hidden-import win32timezone             -w --icon mlyst.ico --name Minimalyst main.py
```

---

## 🧠 Inspiration

Inspired by:
- Vintage Walkmans
- Minimal and distraction-free software

---

## 🪪 License

MIT License.

---

## 🙌 Author

**Pedro Gabriel Ferraz Santos Silva**  
https://github.com/PGFerraz
