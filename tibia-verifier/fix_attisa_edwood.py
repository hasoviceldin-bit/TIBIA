"""Restore screenshot-confirmed Non Lifers PvP deaths lost on free-instance restarts.

Runs after fix_missing_pvp.py. Does not change presentation or invent live scan results.
"""
from pathlib import Path
p = Path(__file__).with_name('intel.py')
s = p.read_text(encoding='utf-8')
anchor = "        ('Warlord Gomez', '2026-11-25T19:08:00+00:00', 1260, 'Bep Bep Beeeep'),"
assert s.count(anchor) == 1, 'Historical death checkpoint changed'
new = """        # Three archived records from the November 27 dashboard screenshot.
        ('Attisa', '2026-11-27T00:59:00', 1227, 'Bep Bep Beeeep'),
        ('Edwood', '2026-11-26T22:03:00', 519, 'Bep Bep Beeeep'),
        ('Attisa', '2026-11-26T21:59:00', 1227, 'Bep Bep Beeeep'),"""
s = s.replace(anchor, anchor + '\n' + new, 1)
old = "for priority in ('Deadshoot','Warlord Gomez'):"
assert s.count(old) == 1, 'Priority scanner changed'
s = s.replace(old,"for priority in ('Deadshoot','Warlord Gomez','Edwood','Attisa'):",1)
p.write_text(s,encoding='utf-8')
print('Restored historical Attisa/Edwood PvP entries and priority checks')
