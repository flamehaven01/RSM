#!/usr/bin/env python3
"""
Automated sync script for RSM implementation
Syncs GitHub main branch with Hugging Face Space
"""

import os
import subprocess
import shutil
from pathlib import Path

def sync_github_to_hf():
    """Sync GitHub repository to Hugging Face Space."""

    print("[>] Starting GitHub → HF sync process...")

    # Paths
    github_demo_path = Path("D:/Sanctum/Resonant Structures of Meaning A Machine-Executable Ontology for Interpretive AI/huggingface_deployment")
    hf_clone_path = Path("D:/Sanctum/rms-simulator")

    # Files to sync
    sync_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        ".gitignore"
    ]

    print(f"[>] Syncing {len(sync_files)} files...")

    # Copy files from GitHub to HF clone
    for file in sync_files:
        src = github_demo_path / file
        dst = hf_clone_path / file

        if src.exists():
            shutil.copy2(src, dst)
            print(f"[+] Synced: {file}")
        else:
            print(f"[-] Missing: {file}")

    # Git operations
    os.chdir(hf_clone_path)

    # Check for changes
    result = subprocess.run(['git', 'status', '--porcelain'],
                          capture_output=True, text=True)

    if result.stdout.strip():
        print("[>] Changes detected, committing...")

        # Add and commit
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m',
                       'Auto-sync from GitHub: RSM Simulator updates'])

        # Push to HF
        push_result = subprocess.run(['git', 'push'],
                                   capture_output=True, text=True)

        if push_result.returncode == 0:
            print("[+] Successfully pushed to HF Space!")
            print("    URL: https://huggingface.co/spaces/Flamehaven/rms-simulator")
        else:
            print(f"[-] Push failed: {push_result.stderr}")
    else:
        print("[=] No changes to sync")

def sync_hf_to_github():
    """Sync HF Space back to GitHub (manual review recommended)."""

    print("[>] Starting HF → GitHub sync process...")

    # This would require manual review
    # Create a report of differences instead
    github_path = Path("D:/Sanctum/RSM_Implementation/huggingface_deployment")
    hf_path = Path("D:/Sanctum/rms-simulator")

    sync_files = ["app.py", "requirements.txt", "README.md"]

    differences = []
    for file in sync_files:
        github_file = github_path / file
        hf_file = hf_path / file

        if github_file.exists() and hf_file.exists():
            # Compare file modification times
            github_mtime = github_file.stat().st_mtime
            hf_mtime = hf_file.stat().st_mtime

            if abs(github_mtime - hf_mtime) > 60:  # 1 minute tolerance
                differences.append({
                    'file': file,
                    'github_newer': github_mtime > hf_mtime
                })

    if differences:
        print("[!] Differences detected:")
        for diff in differences:
            source = "GitHub" if diff['github_newer'] else "HF Space"
            print(f"    {diff['file']}: {source} is newer")
    else:
        print("[+] Repositories are in sync")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python sync_to_hf.py [github-to-hf|hf-to-github|check]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "github-to-hf":
        sync_github_to_hf()
    elif command == "hf-to-github":
        sync_hf_to_github()
    elif command == "check":
        sync_hf_to_github()  # Just check differences
    else:
        print("Invalid command. Use: github-to-hf, hf-to-github, or check")