# Fix Git Corruption on Raspberry Pi

## Problem
Multiple corrupt git objects detected. This usually happens when git operations are interrupted.

## Solution: Remove All Corrupt Objects and Re-fetch

Run these commands on your Raspberry Pi:

```bash
cd ~/Projects/ProgForIoT

# Remove the corrupt objects
rm -f .git/objects/fc/61fd41176469e3c50f1bf0198e08bab77ea5c3
rm -f .git/objects/be/02a4e8292c4addce22a2c4f8d46751e6ff9c5e

# Find and remove any other empty/corrupt objects
find .git/objects -type f -empty -delete

# Run git fsck to check for more issues
git fsck --full 2>&1 | grep "corrupt\|dangling\|missing" || echo "No more issues found"

# Prune and re-fetch everything
git fetch --all --prune

# Reset to match remote
git reset --hard origin/main
```

## Alternative: Clone Fresh (If above doesn't work)

```bash
cd ~/Projects

# Backup any local changes (if you have uncommitted work)
cp -r ProgForIoT ProgForIoT_backup

# Remove corrupted repo
rm -rf ProgForIoT

# Clone fresh
git clone https://github.com/Vatsal-Jha256/ProgForIoT.git

cd ProgForIoT
```

## Quick One-Liner Fix

```bash
cd ~/Projects/ProgForIoT && find .git/objects -type f -empty -delete && git fetch --all --prune && git reset --hard origin/main
```
