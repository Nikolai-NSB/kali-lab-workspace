import sys
import subprocess
import os

def banner():
    print("=" * 60)
    print("      MACE SUPREME OSINT FRAMEWORK - v1.0")
    print("=" * 60)

def run_subdomains(target):
    print(f"\n[*] [Module 1] Running Subfinder for passive infrastructure mapping: {target}")
    sub_cmd = ["subfinder", "-d", target, "-silent"]
    res = subprocess.run(sub_cmd, capture_output=True, text=True)
    subs = res.stdout.splitlines() if res.stdout else []
    print(f"[+] Discovered {len(subs)} subdomains.")
    for s in subs[:5]:
        print(f"    - {s}")
    if len(subs) > 5:
        print(f"    ... and {len(subs) - 5} more.")

def run_harvest(target):
    print(f"\n[*] [Module 2] Running theHarvester for email & asset exposure: {target}")
    harvest_cmd = ["theHarvester", "-d", target, "-b", "duckduckgo", "-l", "50"]
    try:
        res = subprocess.run(harvest_cmd, capture_output=True, text=True, timeout=60)
        print(res.stdout if res.stdout else "[!] theHarvester execution completed.")
    except Exception as e:
        print(f"[!] Note on execution: {e}")

def run_metadata_inspection():
    print(f"\n[*] [Module 3] Checking for local files in 'outputs/' for Exiftool analysis...")
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[-] Created missing '{output_dir}/' directory.")
    
    files = os.listdir(output_dir)
    if not files:
        print("[-] No target files found in 'outputs/'. Drop files there to auto-inspect metadata.")
        return

    for file in files:
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path):
            print(f"\n[+] Extracting metadata from: {file}")
            meta_cmd = ["exiftool", file_path]
            subprocess.run(meta_cmd)

if __name__ == "__main__":
    banner()
    if len(sys.argv) < 2:
        print("Usage: python3 supreme_recon.py <target-domain.com>")
        sys.exit(1)
    
    target_domain = sys.argv[1]
    run_subdomains(target_domain)
    run_harvest(target_domain)
    run_metadata_inspection()
    print("\n[+] Reconnaissance suite execution complete.")
