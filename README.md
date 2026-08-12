# Advanced WhatsApp Sender And Lead Extractor

An GUI-based desktop utility built in Python (PyQt5) to extract business leads from Google Maps, analyze phone numbers for active WhatsApp accounts, and send bulk WhatsApp messages (text and images) securely.

[![Watch the tutorial on YouTube](https://github.com/user-attachments/assets/e6ddb267-c599-41ad-9761-ed4267b1cad9)](https://www.youtube.com/watch?v=vcJBbGqtvM8)

---

## 🚀 Key Features

### 1. Google Maps Lead Extractor (Passive Monitor Mode)
* **User-Driven Scrapes:** Rather than using aggressive crawlers that get blocked or freeze, this tool runs as a passive monitor. You search Maps, click on listings manually, and the tool captures details in real-time.
* **Smart Number Extraction Fallback:** Automatically scrapes the phone number from the opened profile pane. If the phone number is missing there, it falls back to parsing the preview card text on the left results sidebar.
* **Export to CSV:** Allows downloading the extracted leads (Name and Phone) directly into a `.csv` file.

### 2. WhatsApp Number Analyzer
* Automatically parses a bulk list of phone numbers (manually loaded or imported via Excel/CSV).
* Filters out invalid numbers and flags numbers that do not have active WhatsApp accounts.

### 3. Bulk WhatsApp Sender (Text & Images)
* **Text Messages:** Sends messages to thousands of numbers with custom delays to prevent spam bans.
* **Image Messages:** Sends images with custom captions.
* **Emoji Support:** Uses automatic system clipboard pasting (`pyperclip` + `Ctrl+V`) to bypass standard Selenium typing errors with emojis (like `😊` and `🚀`).
* **Multi-Account Sessions:** Save and switch between multiple WhatsApp accounts within the app.

---

## 🛠️ Developer Setup (Running from Source)

### 1. Install Python
Download and install Python (v3.10+) from the [official website](https://www.python.org/downloads/). 
Make sure to check the box **"Add python.exe to PATH"** during installation.

### 2. Install Dependencies
Open a command prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

### 3. Start the Application
Run the main script:
```bash
python main.py
```
*Note: Chrome Driver matching is handled automatically by the software. Keep Google Chrome updated.*

---

## 📦 Packaging for Non-Developers (Creating an `.exe`)

If you want to share this app with a friend who doesn't have Python or a code editor installed, you can bundle it into a standalone Windows executable.

### 1. Build the Binary
Run the following command in your virtual environment:
```bash
pyinstaller --noconfirm --onedir --windowed --add-data "fonts;fonts" --add-data "src;src" main.py
```
This will compile the application and output the results inside the `dist/` directory.

### 2. Create the Distribution Zip
1. Go to the `dist/` folder.
2. You will find a folder named **`main`** which contains `main.exe` and a folder named **`_internal`**.
3. **Right-click** on the `main` folder and select **Compress to ZIP file** (or send to a zipped folder).
4. Send that `.zip` file to your friend.

*Note: Your friend must **fully extract/unzip** the folder before double-clicking `main.exe`. If they attempt to run `main.exe` directly inside the `.zip` file without extracting it, the application will crash with a `Failed to load Python DLL` error because it cannot access the `_internal` directory.*

---

## 🔍 Troubleshooting & FAQs

#### Q1: "pip" or "python" is not recognized as an internal or external command
* **Cause:** Python wasn't added to the system PATH.
* **Fix:** Re-run the Python installer, select **Modify**, check **"Add Python to PATH"**, and complete installation. Then open a fresh Command Prompt window.

#### Q2: Google Chrome fails to open or crashes instantly
* **Cause:** Usually caused by restrictive antiviruses, system permission limits on temporary directories, or memory constraints on WebGL/GPU acceleration.
* **Fix:** The program is pre-configured with safety flags (`--disable-gpu`, `--disable-dev-shm-usage`, `--no-sandbox`) to prevent this. Ensure Google Chrome is installed in the default location.

#### Q3: Windows Defender / SmartScreen blocks the `.exe` file
* **Cause:** Standard Windows warning for unsigned, custom-made executable applications.
* **Fix:** Click **"More info"** on the blue warning pop-up, then click **"Run anyway"**.
