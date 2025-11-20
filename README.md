# Cross Platform Inventory
This is a cross platform inventory tool
README.md — Cross-Platform Host Inventory Tool

Overview

This project provides a lightweight, cross-platform host inventory script designed for security engineers, vulnerability management analysts, and IT operations teams.
It automatically detects the operating system (macOS, Linux, Windows), executes OS-specific enumeration commands, and exports the results to structured JSON.

The script is designed to reflect real-world asset inventory practices found in VM programs that use tools like ServiceNow CMDB, Tenable Service Hub, JAMF, Intune, or SCCM.

This tool is suitable for:
	•	Vulnerability management workflows
	•	Security baselining
	•	Host discovery
	•	Lab automation
	•	Portfolio demonstration projects
	•	Pre-CMDB inventory gathering in small organizations

⸻

Features
	•	Automatic OS detection (macOS, Linux, Windows)
	•	Structured host inventory collection, including:
	•	hostname
	•	OS version
	•	CPU information
	•	network settings
	•	firewall status
	•	disk encryption status
	•	security controls
	•	Separate exported list of installed applications/packages
	•	Robust logging (inventory.log)
	•	Error handling for all commands
	•	Command-line interface (CLI) for specifying output paths
	•	JSON output compatible with CMDB/SIEM/VM tools

⸻

Project Structure

```bash
cross_platform_inventory.py
inventory.log
host_inventory.json
installed_apps.json
README.md
```

Requirements

No third-party Python libraries are required.
The script works with Python 3.7+.

For full functionality on Linux, certain commands (like dpkg or ufw) may require elevated privileges or availability depending on distro.

⸻

Usage

Basic Usage (default output files):

```bash
python3 cross_platform_inventory.py
```

This generates:
	•	host_inventory.json → core system info
	•	installed_apps.json → installed applications/packages
	•	inventory.log → logfile

Custom Output Paths

You can specify custom output files:

```bash
python3 cross_platform_inventory.py \
    --output my_inventory.json \
    --apps my_apps.json
```

Example Output

host_inventory.json

```json
{
    "os_detected": "macOS",
    "timestamp": "2025-11-13T20:14:02.123Z",
    "inventory": {
        "hostname": "MacBook-Pro",
        "os_version": "ProductVersion: 14.1",
        "cpu": "Apple M2 Pro",
        "ip_address": "172.20.10.5",
        "firewall": "Firewall is disabled.",
        "file_sharing": "File Sharing: ON",
        "disk_encryption": "FileVault is On."
    }
}
```

installed_apps.json

```json
{
    "applications": [
        "Google Chrome.app",
        "Visual Studio Code.app",
        "Slack.app",
        "Safari.app"
    ]
}
```

Logging

The script generates a detailed inventory.log file which includes:
	•	executed commands
	•	errors
	•	OS detection
	•	file write confirmations

This is useful for debugging and demonstrates professional-grade operational awareness.

⸻

How It Works

1. Detect OS

Uses platform.system() to determine:
	•	Darwin → macOS
	•	Linux → Linux
	•	Windows → Windows

2. Execute OS-Specific Commands

Each OS has a dedicated collector function that uses lightweight, universally available system commands.

3. Parse and Export JSON

Two output files:
	•	system inventory
	•	installed applications

These reflect the structure of real CMDB/asset-management schemas.

4. Logging

Every action is logged to inventory.log.

⸻

Extending the Tool

You can easily extend functionality:
	•	add cloud metadata (AWS/GCP/Azure)
	•	send results to REST API endpoints
	•	integrate with Tenable or Qualys
	•	add cryptographic signing
	•	add scheduling (cron/Task Scheduler)
	•	add SSH-based remote inventory

⸻

Use Cases
	•	Security auditing
	•	Vulnerability management prep
	•	Host baseline configuration
	•	Security team lab environments
	•	Demonstrating VM lifecycle understanding in interviews
	•	Lightweight CMDB population

⸻

License

MIT License. Free for personal and professional use.

