import sys
import subprocess

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
    # Fixing command call to match Kali's expected binary/wrapper
    harvest_cmd = ["theHarvester", "-d", target, "-b", "duckduckgo", "-l", "50"]
    try:
        res = subprocess.run(harvest_cmd, capture_output=True, text=True, timeout=60)
        print(res.stdout if res.stdout else "[!] theHarvester execution completed.")
    except Exception as e:
        print(f"[!] Note on execution: {e}")

if __name__ == "__main__":
    banner()
    if len(sys.argv) < 2:
        print("Usage: python3 supreme_recon.py <target-domain.com>")
        sys.exit(1)
    
    target_domain = sys.argv[1]
    run_subdomains(target_domain)
    run_harvest(target_domain)
    print("\n[+] Reconnaissance suite execution complete.")
