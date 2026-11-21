from pathlib import Path
p = Path(__file__).with_name("server.py")
s = p.read_text(encoding="utf-8")
before = 'root = data.get("characters") or {}'
after = 'root = data.get("character") or data.get("characters") or {}'
if before in s: s = s.replace(before, after)
if after not in s: raise RuntimeError("TibiaData v5 character parser not found")
before = 'if date in {"release", "since release", "from the beginning"}:'
after = 'if (world.get("battleye_date") == "") or date in {"release", "since release", "from the beginning"}:'
if before in s: s = s.replace(before, after)
if after not in s: raise RuntimeError("BattlEye world parser not found")
p.write_text(s, encoding="utf-8")
print("TibiaData v5 compatibility checks passed")
