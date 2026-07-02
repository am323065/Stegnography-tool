# 🕵️ Steganography Tool

> **UpToSkills Intern Project**
> README Author: Srajit

---

## 📖 What is Steganography?

Steganography is the art of **hiding secret information inside ordinary files** — like images — so that no one even knows a message is there. Unlike encryption (which scrambles the message), steganography hides the very *existence* of the message.

This project implements **LSB (Least Significant Bit)** Steganography. Every pixel in an image has Red, Green, and Blue values (0–255). The last bit of each value is so tiny that changing it makes **zero visible difference** to the image — but we can use those bits to secretly store a message!

---

## 👥 Team Credits

| Module | Work Done | Contributors |
|---|---|---|
| 🔐 **Module 1 — Encode** | LSB Encoding logic to hide message in image pixels | **Gauri, Aman & Team** |
| 🔓 **Module 2 — Decode** | LSB Decoding logic to extract message from image pixels | **Veera, Shreyaj, Vatsal & Team** |
| 🔒 **Module 3 — Encryption** | Password-based encryption & decryption of messages | **Arpita & Rakshita** |
| 🔒 **Encryption Research** | Independent encryption module research & implementation | **Aftab** |
| 🎨 **UI Design** | Streamlit web interface, styling, and layout | **Khushi & Madhuri** |
| 🖼️ **Sample Images** | Test PNG images of various resolutions | **Archana** |
| 📋 **Requirements** | Python dependency management | **Muskan** |
| 📝 **Documentation** | README and project documentation | **Srajit** |

---

## 🚀 How to Run the App

### Step 1: Clone the Repository
```bash
git clone https://github.com/YourUsername/Stegnography-tool.git
cd Stegnography-tool
```

### Step 2: Create a Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### Step 3: Install Required Libraries
```bash
pip install -r requirements.txt
```

### Step 4: Run the App
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 🔄 How the App Works

### 🔐 Encode Mode (Hide a message)
1. Upload a **PNG or BMP** carrier image
2. Type your **secret message**
3. Optionally enter a **password** to encrypt the message (Arpita & Rakshita's module)
4. Click **Encode** — the message gets hidden inside the image pixels (Gauri & Aman's module)
5. **Download** the stego-image (looks identical to the original!)

### 🔓 Decode Mode (Reveal a message)
1. Upload the **stego-image** (the one downloaded after encoding)
2. Enter the **password** if encryption was used
3. Click **Decode** — the hidden message is extracted (Veera, Shreyaj & Vatsal's module)
4. The original secret message is displayed!

---

## 📁 Project Structure

```
Stegnography-tool/
│
├── app.py                          ← Main integrated Streamlit app
├── encode.py                       ← Module 1: LSB Encoding (Gauri, Aman & Team)
├── decode.py                       ← Module 2: LSB Decoding (Veera, Shreyaj, Vatsal & Team)
├── encryption.py                   ← Module 3: Encryption (Arpita & Rakshita)
├── requirements.txt                ← Dependencies (Muskan)
├── README.md                       ← This file (Srajit)
│
└── sample_images- Archana/         ← Test images (Archana)
    ├── sample_01_sunset_800x600.png
    ├── sample_02_ocean_1024x768.png
    └── ...
```

---

## ⚠️ Important Notes

- ✅ Use **PNG or BMP** images only
- ❌ **JPEG is NOT supported** — JPEG compression destroys the hidden bits
- 📏 Larger images can store longer messages
- 🔒 If you encode with a password, you **must** use the same password to decode

---

*Built with ❤️ by UpToSkills Interns*