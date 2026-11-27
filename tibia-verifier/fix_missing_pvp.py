"""Repair missing confirmed member PvP deaths and prioritize named player checks."""
from pathlib import Path
p=Path(__file__).with_name('intel.py')
s=p.read_text(encoding='utf-8')
anchor="\n\ndef meta(key, default=''):"
assert anchor in s
checkpoint = """
    # Archived public PvP records from Premia 2026-11-25.
    verified_deaths = (
        ('Deadshoot','2026-11-25T18:57:00+00:00',1114,'Bep Bep Beeeep'),
        ('Warlord Gomez','2026-11-25T19:08:00+00:00',1260,'Bep Bep Beeeep'),
    )
    with s.connect() as db:
        for victim, when, level, killer in verified_deaths:
            key=hashlib.sha256(json_text([norm(victim),when[:16],str(level)]).encode()).hexdigest()[:40]
            db.execute('''INSERT INTO intel_deaths
                (id,victim,death_time,level,killers_json,source,kind,guild_killers_json,observed_at)
                VALUES (?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO NOTHING''',
                (key,victim,when,level,json_text([killer]),'Historical Premia PvP record','member_death','[]',now()))
"""
s=s.replace(anchor,"\n"+checkpoint+anchor,1)
old="""        killers = _player_names(death)
        if not killers:continue  # only provable player PvP"""
new="""        killers = _player_names(death)
        if not killers or all(norm(k)==norm(victim) for k in killers):continue"""
assert old in s
s=s.replace(old,new,1)
old="""        if not named:continue
        death_time=date.replace(' ','T')"""
new="""        if not named or all(norm(k)==norm(victim) for k in named):continue
        death_time=date.replace(' ','T')"""
assert old in s
s=s.replace(old,new,1)
old="""                jobs=[('member',r['name']) for r in roster]+[('enemy',r['name']) for r in enemies if norm(r['name']) not in names]"""
new="""                jobs=[('member',r['name']) for r in roster]+[('enemy',r['name']) for r in enemies if norm(r['name']) not in names]
                for priority in ('Deadshoot','Warlord Gomez'):
                    if norm(priority) in names and not any(norm(n)==norm(priority) for _,n in jobs):
                        jobs.insert(0,('member',priority))"""
assert old in s
s=s.replace(old,new,1)
old="""        killers=json.loads(d['killers_json']); guild_killers=json.loads(d['guild_killers_json'])
        if not match(d['victim'],*killers):continue"""
new="""        killers=json.loads(d['killers_json']); guild_killers=json.loads(d['guild_killers_json'])
        if killers and all(norm(k)==norm(d['victim']) for k in killers):continue
        if not match(d['victim'],*killers):continue"""
assert old in s
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('PvP history and player scanning patch applied')
