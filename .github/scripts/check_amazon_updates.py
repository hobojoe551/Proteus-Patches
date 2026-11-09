#!/usr/bin/env python3
import os
import re
import urllib.request

PKG = "com.amazon.mShop.android.business.shopping"
PLAY_URL = f"https://play.google.com/store/apps/details?id={PKG}&hl=en_US"
CONSTANTS_FILE = "patches/src/main/kotlin/app/template/patches/shared/Constants.kt"

def get_latest_play_version():
    req = urllib.request.Request(PLAY_URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
    html = urllib.request.urlopen(req).read().decode("utf-8")
    versions = re.findall(r'\[\[\[\"(\d+\.\d+\.\d+\.\d+)\"', html)
    if not versions:
        raise RuntimeError("Could not find version string in Play Store HTML")
    return versions[0]

def main():
    latest_ver = get_latest_play_version()
    print(f"Latest Play Store version for {PKG}: {latest_ver}")

    with open(CONSTANTS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if this version is already supported
    if f'version = "{latest_ver}"' in content or f'"{latest_ver}"' in content:
        print(f"Version {latest_ver} is already present in {CONSTANTS_FILE}. No update needed.")
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as gh_out:
                gh_out.write("has_update=false\n")
        return

    print(f"New version detected: {latest_ver}. Updating {CONSTANTS_FILE}...")

    # Pattern to find AMAZON_BUSINESS_COMPATIBILITY targets
    pattern = r'(val AMAZON_BUSINESS_COMPATIBILITY = Compatibility\(.*?targets = listOf\()(.*?)(\n\s*\)\s*\n\s*\))'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise RuntimeError("Could not locate AMAZON_BUSINESS_COMPATIBILITY targets block")

    header, existing_targets, footer = match.groups()
    new_target_entry = f'\n            AppTarget(version = "{latest_ver}"),'
    new_targets = existing_targets + new_target_entry
    new_content = content[:match.start()] + header + new_targets + footer + content[match.end():]

    with open(CONSTANTS_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Successfully added AppTarget(version = \"{latest_ver}\")")
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as gh_out:
            gh_out.write("has_update=true\n")
            gh_out.write(f"new_version={latest_ver}\n")

if __name__ == "__main__":
    main()
