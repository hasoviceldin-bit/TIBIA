"""Restore the existing dashboard layout and replace the large enemy card wall with a compact summary widget."""
from pathlib import Path
import re
root = Path(__file__).resolve().parent
jsfile = root/'static/intel.js'
htmlfile = root/'templates/intel.html'
cssfile = root/'static/intel.css'
js = jsfile.read_text(encoding='utf-8')
start = js.index('  function summaryCard(enemy) {')
end = js.index('\n  function paint(){', start)
compact = '''  function summaryCard(enemy) {
    const losses = enemy.losses.size;
    const revenge = enemy.revenge.size;
    const entries = [...enemy.revenge.values()]
      .sort((a,b) => String(b.time).localeCompare(String(a.time)));
    const latest = entries[0];
    const killList = entries.map(d => `<li><span>${date(d.time)}</span><span>${names(d.guild_killers)}</span></li>`).join('');
    return `<div class="compact-enemy-row">
      <span class="compact-enemy-name">${char(enemy.name)}</span>
      <span class="compact-enemy-num compact-red" title="Non Lifers players killed">${losses}</span>
      <span class="compact-enemy-num compact-green" title="Times killed by Non Lifers">${revenge}</span>
      ${revenge ? `<details class="compact-enemy-detail"><summary>Details</summary><ul>${killList}</ul></details>` : '<span class="compact-enemy-no-detail">—</span>'}
    </div>`;
  }
'''
js = js[:start] + compact + js[end:]
old = '''    $('intelEnemyCount').textContent=String(enemies.length);
    $('intelEnemySummary').innerHTML=enemies.length ? enemies.map(summaryCard).join('')
      : '<p class="intel-enemy-empty">No enemy encounters recorded for this period.</p>';'''
new = '''    $('intelEnemyCount').textContent=String(enemies.length);
    const topEnemies = enemies.slice(0, 5);
    const extraEnemies = enemies.slice(5);
    $('intelEnemySummary').innerHTML = enemies.length
      ? topEnemies.map(summaryCard).join('') + (extraEnemies.length ? `<details class="compact-enemy-more"><summary>Show ${extraEnemies.length} more enemies</summary>${extraEnemies.map(summaryCard).join('')}</details>` : '')
      : '<p class="compact-enemy-empty">No enemy encounters recorded for this period.</p>';'''
assert old in js, 'Enemy renderer changed'
js = js.replace(old, new, 1)
jsfile.write_text(js, encoding='utf-8')
html = htmlfile.read_text(encoding='utf-8')
a = html.index('<section class="intel-enemy-section"')
b = html.index('<div class="intel-dashboard-grid">', a)
small = '''<section class="compact-enemy-box" id="enemy-overview" aria-label="Enemy kill summary">
  <div class="compact-enemy-title"><div><h2>Enemy kill summary</h2><p>Each enemy shown once · selected period</p></div><span><strong id="intelEnemyCount">—</strong> tracked</span></div>
  <div class="compact-enemy-labels"><span>Enemy</span><span>Our losses</span><span>Revenge</span><span></span></div>
  <div id="intelEnemySummary" aria-live="polite"><p class="compact-enemy-empty">Loading…</p></div>
</section>
'''
html = html[:a] + small + html[b:]
htmlfile.write_text(html, encoding='utf-8')
cssfile.write_text(cssfile.read_text(encoding='utf-8') + '''\n/* Small revenge summary only: leave the main dashboard and tables unchanged. */
.compact-enemy-box{box-sizing:border-box;max-width:620px;margin:0 0 18px;background:#151e2d;border:1px solid #314158;border-radius:12px;padding:14px 16px}
.compact-enemy-title{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:12px}
.compact-enemy-title h2{font-size:15px;font-weight:700;margin:0 0 3px;color:#f2f5fa}
.compact-enemy-title p{margin:0;color:#92a5bf;font-size:11px}
.compact-enemy-title>span{color:#98aac0;font-size:11px;white-space:nowrap}
.compact-enemy-title>span strong{color:#e3c47e;font-size:14px}
.compact-enemy-labels,.compact-enemy-row{display:grid;grid-template-columns:minmax(95px,1fr) 70px 60px 56px;align-items:center;gap:6px}
.compact-enemy-labels{font-size:10px;color:#8fa1b8;margin-bottom:4px}
.compact-enemy-labels span:not(:first-child){text-align:center}
.compact-enemy-row{padding:9px 0;border-top:1px solid #2c394b;font-size:12px}
.compact-enemy-name{min-width:0;overflow-wrap:anywhere;font-weight:650}
.compact-enemy-name a{color:#eccb85;text-decoration:none}
.compact-enemy-name a:hover{text-decoration:underline}
.compact-enemy-num{text-align:center;font-weight:700;font-size:14px;font-variant-numeric:tabular-nums}
.compact-red{color:#eca0a4}.compact-green{color:#8ed9ab}
.compact-enemy-detail{position:relative;text-align:center;font-size:11px}
.compact-enemy-detail summary,.compact-enemy-more>summary{cursor:pointer;color:#c8cfe1}
.compact-enemy-detail[open]{grid-column:1/-1;text-align:left;padding:8px 0 1px}
.compact-enemy-detail ul{margin:8px 0 0;padding:0;list-style:none}
.compact-enemy-detail li{display:flex;justify-content:space-between;gap:9px;padding:6px 0;border-top:1px solid #2c394b;flex-wrap:wrap}
.compact-enemy-detail li a{color:#eccb85}
.compact-enemy-no-detail{text-align:center;color:#657892}
.compact-enemy-more{border-top:1px solid #34435a;padding-top:10px;font-size:11px}
.compact-enemy-more>summary{margin-bottom:6px}
.compact-enemy-empty{font-size:12px;color:#96a9c1;margin:10px 0}
@media(max-width:520px){.compact-enemy-box{padding:12px}.compact-enemy-labels,.compact-enemy-row{grid-template-columns:minmax(70px,1fr) 52px 53px 48px;gap:4px}.compact-enemy-labels{font-size:9px}}
''', encoding='utf-8')
print('Compact revenge widget installed; original dashboard tables preserved.')