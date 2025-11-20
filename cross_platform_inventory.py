import subprocess
import platform
import json
import argparse
import logging
import sys
import os
from datetime import datetime

# --------------------------------------------
# Utility Functions
# --------------------------------------------

def setup_logging(log_file="inventory.log"):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.info("Logging initialized.")


def run(cmd):
    """Run a shell command safely"""
    try:
        output = subprocess.check_output(
            cmd, shell=True, text=True, stderr=subprocess.STDOUT
        ).strip()
        logging.info(f"Executed: {cmd}")
        return output
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {cmd} - Error: {e.output}")
        return "N/A"
    except Exception as e:
        logging.error(f"Unexpected error running: {cmd} - {e}")
        return "N/A"


# --------------------------------------------
# OS-specific Data Collectors
# --------------------------------------------

def collect_macos():
    logging.info("Collecting macOS inventory.")
    apps = run("ls /Applications")
    return {
        "inventory": {
            "hostname": run("scutil --get LocalHostName"),
            "os_version": run("sw_vers"),
            "cpu": run("sysctl -n machdep.cpu.brand_string"),
            "ip_address": run("ipconfig getifaddr en0"),
            "firewall": run("/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate"),
            "file_sharing": run("sharing -l"),
            "disk_encryption": run("fdesetup status"),
        },
        "applications": apps.split("\n") if apps != "N/A" else []
    }


def collect_linux():
    logging.info("Collecting Linux inventory.")
    packages = run("dpkg -l || rpm -qa")
    return {
        "inventory": {
            "hostname": run("hostname"),
            "os_version": run("cat /etc/os-release"),
            "cpu": run("lscpu"),
            "ip_address": run("hostname -I"),
            "firewall": run("sudo ufw status"),
            "disk_encryption": run("lsblk -o NAME,FSTYPE,MOUNTPOINT"),
        },
        "applications": packages.split("\n") if packages != "N/A" else []
    }


def collect_windows():
    logging.info("Collecting Windows inventory.")
    programs = run("wmic product get Name,Version")
    return {
        "inventory": {
            "hostname": run("hostname"),
            "os_version": run("wmic os get Caption,Version /value"),
            "cpu": run("wmic cpu get Name /value"),
            "ip_address": run("ipconfig"),
            "firewall": run("netsh advfirewall show allprofiles"),
            "disk_encryption": run("manage-bde -status"),
        },
        "applications": programs.split("\n") if programs != "N/A" else []
    }


# --------------------------------------------
# Main Function
# --------------------------------------------

def main(output_file, apps_file):
    setup_logging()

    system = platform.system().lower()
    logging.info(f"Detected OS: {system}")

    if system == "darwin":
        os_name = "macOS"
        data = collect_macos()
    elif system == "linux":
        os_name = "Linux"
        data = collect_linux()
    elif system == "windows":
        os_name = "Windows"
        data = collect_windows()
    else:
        logging.error("Unsupported OS.")
        print("Unsupported OS.")
        sys.exit(1)

    output = {
        "os_detected": os_name,
        "timestamp": datetime.utcnow().isoformat(),
        "inventory": data["inventory"]
    }

    # Write inventory
    with open(output_file, "w") as f:
        json.dump(output, f, indent=4)
    logging.info(f"Inventory written to {output_file}")

    # Write applications separately
    with open(apps_file, "w") as f:
        json.dump({"applications": data["applications"]}, f, indent=4)
    logging.info(f"Applications written to {apps_file}")

    print(f"Inventory saved to {output_file}")
    print(f"Applications saved to {apps_file}")


# --------------------------------------------
# CLI Argument Parsing
# --------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cross-platform host inventory tool.")
    
    parser.add_argument(
        "--output", 
        default="host_inventory.json", 
        help="JSON file to write inventory data to."
    )
    
    parser.add_argument(
        "--apps", 
        default="installed_apps.json", 
        help="JSON file to write installed applications/packages."
    )
    
    args = parser.parse_args()
    main(args.output, args.apps)