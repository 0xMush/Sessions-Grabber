# Sessions-Grabber

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Windows RDP & Session Grabber Tool</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem 1rem 3rem;
      line-height: 1.6;
      background-color: #0f172a;
      color: #e5e7eb;
    }
    h1, h2, h3, h4 {
      color: #fbbf24;
    }
    code, pre {
      font-family: "Fira Code", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      background: #020617;
      color: #e5e7eb;
      border-radius: 4px;
    }
    pre {
      padding: 0.75rem 1rem;
      overflow-x: auto;
    }
    code {
      padding: 0.15rem 0.35rem;
    }
    a {
      color: #38bdf8;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    .badge {
      display: inline-block;
      padding: 0.25rem 0.6rem;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 600;
      margin-right: 0.25rem;
      background: #1f2937;
      color: #e5e7eb;
    }
    .warning {
      border-left: 4px solid #f97316;
      background: #111827;
      padding: 0.75rem 1rem;
      margin: 1rem 0;
      font-size: 0.95rem;
    }
    .section {
      margin: 2rem 0;
    }
    ul {
      padding-left: 1.2rem;
    }
    li {
      margin-bottom: 0.25rem;
    }
    hr {
      border: none;
      border-top: 1px solid #1f2937;
      margin: 2rem 0;
    }
  </style>
</head>
<body>
  <h1>Windows RDP &amp; Session Audit Tool</h1>
  <p>
    <span class="badge">Windows</span>
    <span class="badge">Python</span>
    <span class="badge">RDP Audit</span>
    <span class="badge">Telegram Bot Report</span>
  </p>

  <div class="warning">
    <strong>⚠️ Legal &amp; Ethical Notice</strong><br />
    This tool is intended <strong>only</strong> for security auditing, system administration,
    and recovery on machines that <strong>you own or have explicit permission to test</strong>.
    Any unauthorized access, password changes, or session data collection on systems you do not control
    may be illegal. The author is not responsible for misuse.
  </div>

  <div class="section">
    <h2>📌 Overview</h2>
    <p>
      This project is a Windows security auditing and diagnostic script. It helps administrators
      and power users inspect a local machine, check its RDP exposure, back up local Telegram Desktop
      and Discord session data, and send a detailed report to a Telegram bot.
    </p>
    <p>
      The script runs on Windows, requires Administrator privileges, and communicates with a Telegram
      bot using your bot token and chat ID.
    </p>
  </div>

  <div class="section">
    <h2>✨ Key Features</h2>

    <h3>🔐 RDP Security &amp; Password Audit</h3>
    <ul>
      <li>Detects if Remote Desktop Services (<code>TermService</code>) are running.</li>
      <li>Checks if RDP port <code>3389</code> is open on the local machine.</li>
      <li>
        Can attempt to change the current Windows user password to a predefined value
        (for recovery or authorized testing only).
      </li>
    </ul>

    <h3>💬 Telegram Desktop Session Backup</h3>
    <ul>
      <li>Looks for Telegram Desktop <code>tdata</code> in the user profile.</li>
      <li>Copies it to a temporary directory.</li>
      <li>Stores the backup in a ZIP archive that can be sent to your Telegram bot.</li>
    </ul>

    <h3>🎮 Discord Local Session Backup</h3>
    <ul>
      <li>Searches common Discord and browser paths for locally stored Discord tokens.</li>
      <li>Supports multiple platforms (Discord, Discord Canary/PTB, Chrome, Edge, Opera, Brave, etc.).</li>
      <li>Writes discovered tokens to a temporary file and includes them in the ZIP archive.</li>
    </ul>

    <h3>🖥 System &amp; Network Information</h3>
    <ul>
      <li>Collects IP address, OS version, and current username.</li>
      <li>Retrieves MAC address of available network interfaces.</li>
      <li>Scans typical ports: <code>3389</code>, <code>80</code>, <code>443</code>, <code>445</code>, <code>135</code>, <code>139</code>.</li>
      <li>Builds a structured Markdown report with all findings.</li>
    </ul>

    <h3>📲 Telegram Bot Reporting</h3>
    <ul>
      <li>Uses your Telegram bot token and chat ID.</li>
      <li>Sends a formatted Markdown report to your Telegram chat.</li>
      <li>Optionally attaches the ZIP archive that contains Telegram data and Discord token backup.</li>
      <li>Includes basic error handling and a fallback minimal message if the main send fails.</li>
    </ul>
  </div>

  <div class="section">
    <h2>📦 Requirements</h2>
    <ul>
      <li>Windows operating system</li>
      <li>Python 3.x</li>
      <li>Administrator privileges</li>
      <li>Python packages:
        <ul>
          <li><code>requests</code></li>
          <li><code>psutil</code></li>
        </ul>
      </li>
    </ul>

    <pre><code>pip install requests psutil</code></pre>
  </div>

  <div class="section">
    <h2>⚙️ Configuration</h2>
    <ol>
      <li>
        Create a Telegram bot using <strong>@BotFather</strong> and obtain your
        <strong>bot token</strong>.
      </li>
      <li>
        Get your <strong>chat ID</strong> (for example, by messaging your bot and using a helper tool or small script).
      </li>
      <li>
        In the script, set:
        <pre><code>TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"</code></pre>
        If you leave the default placeholders, the script will ask you for these values on first run and update itself.
      </li>
    </ol>
  </div>

  <div class="section">
    <h2>🚀 Usage</h2>
    <ol>
      <li>Clone or download this repository.</li>
      <li>Install dependencies:
        <pre><code>pip install requests psutil</code></pre>
      </li>
      <li>Open a terminal / PowerShell as <strong>Administrator</strong>.</li>
      <li>Run the script:
        <pre><code>python main.py</code></pre>
      </li>
    </ol>
    <p>
      After execution, a full report and (optionally) a ZIP archive with session backups will
      be sent to your configured Telegram bot.
    </p>
  </div>

  <div class="section">
    <h2>🔍 Intended Use Cases</h2>
    <ul>
      <li>Auditing RDP configuration on your own servers or lab machines.</li>
      <li>Testing how local apps store sessions on Windows.</li>
      <li>Backup or migration of Telegram Desktop sessions.</li>
      <li>Incident response and forensic analysis on authorized environments.</li>
    </ul>
    <p>
      It must <strong>not</strong> be used to access or take over accounts that do not belong to you,
      or systems you do not control.
    </p>
  </div>

  <div class="section">
    <h2>🧑‍💻 Author</h2>
    <p>
      <strong>Mushaib</strong> (aka <strong>Mrexe</strong>)<br />
      GitHub: <a href="https://github.com/0xMush" target="_blank" rel="noopener noreferrer">@0xMush</a>
    </p>
  </div>

  <hr />

  <div class="section">
    <h2>⚠️ Final Disclaimer</h2>
    <p>
      This project is provided for educational, research, and defensive purposes only.
      You are fully responsible for complying with all applicable laws and regulations.
    </p>
  </div>
</body>
</html>
