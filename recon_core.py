import sys
import subprocess

def execute_recon(target):
    print(f"\n[+] [MACE OSINT Engine] Initializing target assessment for: {target}")
    
    # 1. Subdomain Enumeration via Subfinder
    print("[*] Running Subfinder for passive infrastructure mapping...")
    sub_cmd = ["subfinder", "-d", target, "-silent"]
    sub_res = subprocess.run(sub_cmd, capture_output=True, text=True)
    
    subdomains = sub_res.stdout.splitlines() if sub_res.stdout else []
    print(f"[+] Discovered {len(subdomains)} potential subdomains.")
    
    print("\n[--- Subdomain Preview ---]")
    for sub in subdomains[:10]:  # Show first 10
        print(f"  - {sub}")
        
    if len(subdomains) > 10:
        print(f"  ... and {len(subdomains) - 10} more.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 recon_core.py <target-domain.com>")
        sys.exit(1)
    
    target_host = sys.argv[1]
    execute_recon(target_host)
