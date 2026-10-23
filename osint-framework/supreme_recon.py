import sys
import subprocess
import os
import urllib.request
import urllib.error
import json
from datetime import datetime

def banner():
    print("=" * 60)
    print("      MACE SUPREME OSINT & DEFENSE FRAMEWORK - v3.0")
    print("=" * 60)

def ensure_dirs():
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

def run_subdomains(target):
    print(f"\n[*] [Module 1] Running Subfinder for passive infrastructure mapping: {target}")
    sub_cmd = ["subfinder", "-d", target, "-silent"]
    res = subprocess.run(sub_cmd, capture_output=True, text=True)
    subs = res.stdout.splitlines() if res.stdout else []
    print(f"[+] Discovered {len(subs)} subdomains.")
    return subs

def run_harvest(target):
    print(f"\n[*] [Module 2] Running theHarvester for email & asset exposure: {target}")
    harvest_cmd = ["theHarvester", "-d", target, "-b", "duckduckgo", "-l", "50"]
    try:
        res = subprocess.run(harvest_cmd, capture_output=True, text=True, timeout=60)
        output = res.stdout if res.stdout else "[!] theHarvester execution completed."
        print(output)
        return output
    except Exception as e:
        err_msg = f"[!] Note on execution: {e}"
        print(err_msg)
        return err_msg

def run_metadata_inspection():
    print(f"\n[*] [Module 3] Checking for local files in 'outputs/' for Exiftool analysis...")
    output_dir = "outputs"
    files = os.listdir(output_dir)
    meta_results = {}
    if not files:
        print("[-] No target files found in 'outputs/'.")
        return meta_results

    for file in files:
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path):
            print(f"\n[+] Extracting metadata from: {file}")
            meta_cmd = ["exiftool", file_path]
            res = subprocess.run(meta_cmd, capture_output=True, text=True)
            print(res.stdout)
            meta_results[file] = res.stdout
    return meta_results

def run_username_profiling(username):
    print(f"\n[*] [Module 4] Scanning digital footprint for username: {username}")
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Twitter/X": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}"
    }
    
    found_profiles = {}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for platform, url in platforms.items():
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    print(f"    [+] [FOUND] {platform}: {url}")
                    found_profiles[platform] = url
        except Exception:
            print(f"    [-] [NOT FOUND/UNREACHABLE] {platform}")
    return found_profiles

def run_network_scan(target_ip):
    print(f"\n[*] [Upgrade 1] Running Safe Network Port Scan (Nmap) on: {target_ip}")
    nmap_cmd = ["nmap", "-F", target_ip] # Fast scan top 100 ports
    try:
        res = subprocess.run(nmap_cmd, capture_output=True, text=True, timeout=60)
        print(res.stdout)
        return res.stdout
    except Exception as e:
        print(f"[!] Nmap scan error: {e}")
        return str(e)

def run_log_parser(log_path):
    print(f"\n[*] [Upgrade 2] Parsing defensive logs from: {log_path}")
    anomalies = []
    if not os.path.exists(log_path):
        print(f"[-] Log file not found at {log_path}")
        return anomalies
    
    with open(log_path, "r") as f:
        for line in f:
            if any(keyword in line.lower() for keyword in ["fail", "error", "unauthorized", "invalid"]):
                anomalies.append(line.strip())
    
    print(f"[+] Discovered {len(anomalies)} potential security anomalies in log.")
    for anom in anomalies[:5]:
        print(f"    [!]: {anom}")
    return anomalies

def export_report(target, data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"reports/scan_report_{timestamp}.json"
    with open(report_filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\n[+] [Upgrade 3] Enterprise JSON Report successfully generated: {report_filename}")

if __name__ == "__main__":
    banner()
    ensure_dirs()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Domain Recon:   python3 supreme_recon.py <target-domain.com>")
        print("  User Profiling: python3 supreme_recon.py --user <username>")
        print("  Network Scan:   python3 supreme_recon.py --nmap <target-ip>")
        print("  Log Parser:     python3 supreme_recon.py --parse <logfile.log>")
        sys.exit(1)
    
    scan_data = {"target": sys.argv[2] if len(sys.argv) > 2 else sys.argv[1], "timestamp": str(datetime.now())}
    
    if sys.argv[1] == "--user" and len(sys.argv) >= 3:
        scan_data["profiles"] = run_username_profiling(sys.argv[2])
    elif sys.argv[1] == "--nmap" and len(sys.argv) >= 3:
        scan_data["nmap_results"] = run_network_scan(sys.argv[2])
    elif sys.argv[1] == "--parse" and len(sys.argv) >= 3:
        scan_data["log_anomalies"] = run_log_parser(sys.argv[2])
    else:
        target_domain = sys.argv[1]
        scan_data["subdomains"] = run_subdomains(target_domain)
        scan_data["harvester"] = run_harvest(target_domain)
        scan_data["metadata"] = run_metadata_inspection()
    
    export_report(sys.argv[1], scan_data)
    print("\n[+] Reconnaissance & reporting suite execution complete.")
