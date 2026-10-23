import sys
import subprocess
import os
import urllib.request
import urllib.error

def banner():
    print("=" * 60)
    print("      MACE SUPREME OSINT FRAMEWORK - v2.0")
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
    
    files = os.listdir(output_dir)
    if not files:
        print("[-] No target files found in 'outputs/'.")
        return

    for file in files:
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path):
            print(f"\n[+] Extracting metadata from: {file}")
            meta_cmd = ["exiftool", file_path]
            subprocess.run(meta_cmd)

def run_username_profiling(username):
    print(f"\n[*] [Module 4] Scanning digital footprint for username: {username}")
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Twitter/X": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}"
    }
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for platform, url in platforms.items():
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    print(f"    [+] [FOUND] {platform}: {url}")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"    [-] [NOT FOUND] {platform}")
            else:
                print(f"    [?] [{e.code}] {platform}")
        except Exception:
            print(f"    [-] [UNREACHABLE] {platform}")

if __name__ == "__main__":
    banner()
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Domain Recon:  python3 supreme_recon.py <target-domain.com>")
        print("  User Profiling: python3 supreme_recon.py --user <username>")
        sys.exit(1)
    
    if sys.argv[1] == "--user" and len(sys.argv) >= 3:
        target_user = sys.argv[2]
        run_username_profiling(target_user)
    else:
        target_domain = sys.argv[1]
        run_subdomains(target_domain)
        run_harvest(target_domain)
        run_metadata_inspection()
    
    print("\n[+] Reconnaissance suite execution complete.")
