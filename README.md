# Kali Lab Workspace (Managed by MACE)

Welcome to your personal security and virtualization control center. This repository contains the documentation and guides for running Kali Linux safely alongside Windows.

## 🚀 Quick Reference: Running Kali Simultaneously with Windows

1. **Virtualization Software:** Oracle VM VirtualBox (Free & Safe).
   * Download from: [virtualbox.org](https://www.virtualbox.org/)
2. **Virtual Machine Image:** Official Kali Linux pre-built VirtualBox image (`.ova`).
   * Download from: [kali.org/get-kali/#kali-virtual-machines](https://www.kali.org/get-kali/#kali-virtual-machines)
3. **Execution Steps:**
   * Install VirtualBox on your Windows host.
   * Open VirtualBox > Click **File > Import Appliance** > Select the downloaded Kali `.ova` file.
   * Hit **Start** to run Kali in its own independent window simultaneously with Windows.

## 🔒 System Isolation Guarantee
Your host Windows file system and personal data remain completely segregated inside the host operating system, while Kali runs safely inside its own dedicated virtual hypervisor window.
