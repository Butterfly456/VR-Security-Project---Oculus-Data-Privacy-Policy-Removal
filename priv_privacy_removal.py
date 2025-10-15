python3 - <<'PY'
import json, re, sys
from pathlib import Path
from collections import deque

# Configuration
SRC = Path("data/oculus")
OUT = Path("privacy_urls_2.json")

if not SRC.is_dir():
    sys.exit("Folder data/oculus not found. Run this from the MetaMetadata-main folder.")

HTTP_RE = re.compile(r"^https?://", re.I)

def find_privacy_url(obj):
    """Recursively search for the key 'developer_privacy_policy_url' (case-insensitive)."""
    q = deque([obj])
    while q:
        cur = q.popleft()
        if isinstance(cur, dict):
            for k, v in cur.items():
                if isinstance(k, str) and k.lower() == "developer_privacy_policy_url":
                    if isinstance(v, str) and HTTP_RE.match(v.strip()):
                        return v.strip()
                q.append(v)
        elif isinstance(cur, list):
            for v in cur:
                q.append(v)
    return None

records = []
found = 0
total = 0

for f in sorted(SRC.glob("*.json")):
    total += 1
    pkg = f.stem
    try:
        data = json.loads(f.read_text(encoding="utf-8", errors="ignore"))
        url = find_privacy_url(data)
    except Exception:
        url = None
    if url:
        found += 1
    records.append({"package_name": pkg, "privacy_policy_url": url})

OUT.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Wrote {OUT.resolve()} with {total} entries.")
print(f"Found privacy_policy_url in {found} apps; {total - found} missing the key.")
PY
