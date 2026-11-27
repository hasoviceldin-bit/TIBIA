"""Deploy-time fix for confirmed historical transfer and source-free UI."""
from pathlib import Path
base=Path(__file__).resolve().parent
p=base/'intel.py';s=p.read_text(encoding='utf-8')
needle='''        else:
            for statement in statements:
                db.execute(statement)
'''
add='''    # Verified historical checkpoint, not a newly ingested event.
    verified=('Bep Bep Beeeep','Antica','Premia','2026-11-25 06:06',1514,'',
              'Archived transfer','https://tibtr.com/worlds/Premia?r=all')
    record_id=hashlib.sha256(b'verified:Bep Bep Beeeep:Antica:Premia:2026-11-25 06:06').hexdigest()[:40]
    with s.connect() as db:
        db.execute("INSERT INTO intel_transfers (id,name,from_world,to_world,moved_at,level,guild,source,source_url,observed_at) VALUES (?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO NOTHING",
            (record_id,*verified,now()))
'''
if needle not in s:raise RuntimeError('intel insertion point changed')
s=s.replace(needle,needle+add,1)
s=s.replace("'source':d['source'],'link':clean_tibia_url(d['victim'])","'link':clean_tibia_url(d['victim'])")
s=s.replace("('id','name','from_world','to_world','moved_at','level','guild','source','source_url')","('id','name','from_world','to_world','moved_at','level','guild')")
s=s.replace("'errors':json.loads(meta('last_errors','[]')),","'source_warnings':len(json.loads(meta('last_errors','[]'))),")
old='''    ts=[]
    for t in transfers:
        if not in_range(t['moved_at']) or not match(t['name'],t['from_world'],t['guild']):continue
        ts.append({key:t[key] for key in ('id','name','from_world','to_world','moved_at','level','guild')})
'''
new='''    ts=[]; seen_events=set()
    for t in transfers:
        if not in_range(t['moved_at']) or not match(t['name'],t['from_world'],t['guild']):continue
        event=(norm(t['name']),norm(t['from_world']),norm(t['to_world']),str(t['moved_at'] or '')[:16])
        if event in seen_events:continue
        seen_events.add(event)
        ts.append({key:t[key] for key in ('id','name','from_world','to_world','moved_at','level','guild')})
'''
if old not in s:raise RuntimeError('transfer api layout changed')
s=s.replace(old,new)
p.write_text(s,encoding='utf-8')
p=base/'static/intel.js';s=p.read_text(encoding='utf-8')
d=chr(36)
s=s.replace('<td><small>'+d+'{escape(d.source)}</small></td>','')
s=s.replace('<td><a href="'+d+'{escape(t.source_url||\'#\')}" target="_blank" rel="noopener noreferrer">'+d+'{escape(t.source)}</a></td>','')
s=s.replace("'Classification','Source'","'Classification'")
s=s.replace("'Level','Source'","'Level'")
s=s.replace('const warnings=st.errors||[];','const warnings=Number(st.source_warnings||0);')
s=s.replace("(warnings.length?' warning':'')","(warnings?' warning':'')")
i=s.index('note.textContent=warnings.length?')
j=s.index(':st.running?',i)
s=s[:i]+"note.textContent=warnings?'Some tracking updates are temporarily unavailable. Existing data is retained.'"+s[j:]
s=s.replace('Observed world changes published by external trackers; data may be delayed.','Transfers into Premia. Recent changes may take time to appear.')
if "'Level','Source'" in s or 'source_url' in s:raise RuntimeError('public sources still appear')
p.write_text(s,encoding='utf-8')
p=base/'templates/intel.html';s=p.read_text(encoding='utf-8')
s=s.replace('<span class="intel-source">Source: TibiaData + public transfer trackers</span>','')
s=s.replace('<p>Data sources: <a href="https://tibiadata.com" target="_blank" rel="noopener noreferrer">TibiaData</a> · <a href="https://tibtr.com/worlds/Premia" target="_blank" rel="noopener noreferrer">Tibia Tracker</a> · <a href="https://guildstats.eu/world-transfer" target="_blank" rel="noopener noreferrer">GuildStats</a></p>','')
s=s.replace('Observed from public sources','Tracked arrivals')
p.write_text(s,encoding='utf-8')
print('Historical transfer and attribution display fix applied')
