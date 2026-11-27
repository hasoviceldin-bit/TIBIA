"""Simplify the public PvP dashboard while leaving ingestion and APIs intact."""
from pathlib import Path
root=Path(__file__).resolve().parent
js=r'''(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const state = { tab: location.pathname.endsWith('/transfers') ? 'transfers' : 'deaths', data: null };
  const escape = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const link = name => `<a href="https://www.tibia.com/community/?subtopic=characters&name=${encodeURIComponent(name)}" target="_blank" rel="noopener noreferrer">${escape(name)}</a>`;
  const formatDate = value => {
    if (!value) return 'Unknown date';
    const dt = new Date(String(value).replace(' ', 'T'));
    return Number.isNaN(dt.getTime()) ? escape(value) : dt.toLocaleString('en-GB', {day:'numeric',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'});
  };
  const names = (list) => (list || []).length ? list.map(link).join(', ') : 'Unknown player';
  const head = columns => `<tr>${columns.map(name => `<th>${escape(name)}</th>`).join('')}</tr>`;
  const lostRow = row => `<tr><td><strong>${link(row.victim)}</strong><small>Level ${escape(row.level || '—')}</small></td><td>${names(row.killers)}</td><td>${formatDate(row.time)}</td></tr>`;
  const revengeRow = row => `<tr><td><strong>${link(row.victim)}</strong><small>Enemy who died</small></td><td>${names(row.guild_killers)}</td><td>${formatDate(row.time)}</td></tr>`;
  const transferRow = row => `<tr><td><strong>${link(row.name)}</strong><small>${escape(row.guild || '')}</small></td><td>${escape(row.from_world || 'Unknown')} → Premia</td><td>${formatDate(row.moved_at)}</td></tr>`;

  function show() {
    if (!state.data) return;
    const data = state.data;
    const counts = data.counts || {};
    $('metricDeaths').textContent = counts.member_pvp_deaths ?? 0;
    $('metricReturns').textContent = counts.retaliation ?? 0;
    $('metricEnemies').textContent = counts.watched_enemies ?? 0;
    $('metricTransfers').textContent = counts.transfers ?? 0;
    const transfer = state.tab === 'transfers';
    $('intelMetrics').classList.toggle('transfers-view', transfer);
    $('intelHeroTitle').textContent = transfer ? 'Who moved to Premia?' : 'Non Lifers PvP deaths';
    $('intelHeroDesc').textContent = transfer
      ? 'See which characters transferred from other worlds to Premia.'
      : 'See who killed our members — and who Non Lifers killed afterwards.';
    const settings = state.tab === 'deaths'
      ? {title:'Our members who died', desc:'Only deaths caused by other players.', columns:['Non Lifers player','Killed by','Date'], rows:data.deaths.filter(x=>x.type==='member_death'), render:lostRow, empty:'No recorded PvP deaths for Non Lifers in this period.'}
      : state.tab === 'retaliation'
      ? {title:'Enemies killed by Non Lifers', desc:'Tracked enemies who later died with a Non Lifers player among the killers.', columns:['Enemy who died','Non Lifers killers','Date'], rows:data.deaths.filter(x=>x.type==='retaliation'), render:revengeRow, empty:'No recorded revenge kills for the selected period.'}
      : {title:'New players on Premia', desc:'Characters observed moving from another world to Premia.', columns:['Character','Moved from','Date'], rows:data.transfers, render:transferRow, empty:'No transfers have been recorded for this period.'};
    $('intelPanelTitle').textContent = settings.title;
    $('intelPanelDesc').textContent = settings.desc;
    $('intelHead').innerHTML = head(settings.columns);
    $('intelBody').innerHTML = settings.rows.length ? settings.rows.map(settings.render).join('')
      : `<tr><td colspan="3" class="intel-empty">${escape(settings.empty)}<small>Tracking is not complete when external data is missing or delayed.</small></td></tr>`;
    document.querySelectorAll('[data-tab]').forEach(button => button.classList.toggle('on', button.dataset.tab === state.tab));
    $('intelSearch').placeholder = transfer ? 'Search character or old world…' : 'Search player name…';
    const status = data.status || {};
    $('intelUpdated').textContent = status.last_attempt ? `Last checked: ${formatDate(status.last_attempt)}` : 'Checking for updates…';
    $('intelNotice').className = 'intel-notice' + (status.source_warnings ? ' warning' : '');
    $('intelNotice').textContent = status.source_warnings
      ? 'Some updates are temporarily unavailable. The list may be incomplete.'
      : status.running ? 'Checking for new events…'
      : 'Showing recorded events. Some older deaths or transfers may be missing.';
  }
  async function load() {
    try {
      const params = new URLSearchParams({days:$('intelDays').value, search:$('intelSearch').value});
      const result = await fetch('/api/intel?' + params, {cache:'no-store'});
      if (!result.ok) throw new Error('HTTP '+result.status);
      state.data = await result.json();
      show();
    } catch(e) {
      $('intelNotice').className = 'intel-notice warning';
      $('intelNotice').textContent = 'Could not load tracking data. Please try again.';
    }
  }
  function switchTab(tab) {
    state.tab = tab;
    history.replaceState(null, '', tab === 'transfers' ? '/intel/transfers' : '/intel');
    show();
  }
  document.querySelectorAll('[data-tab]').forEach(button => button.addEventListener('click', () => switchTab(button.dataset.tab)));
  let timer;
  $('intelSearch').addEventListener('input', () => {clearTimeout(timer);timer=setTimeout(load,250)});
  $('intelDays').addEventListener('change', load);
  $('intelRefresh').addEventListener('click', async () => {
    try {
      const result = await fetch('/api/intel/refresh',{method:'POST'});
      if (result.status === 401) {location.href='/admin/login';return;}
      if (!result.ok) throw new Error('Request failed');
      $('intelNotice').textContent='Update requested. New events will appear when scanning finishes.';
      setTimeout(load,1800);
    } catch(e) {$('intelNotice').textContent='Could not check for updates right now.';}
  });
  load();
  setInterval(load,60000);
})();
'''
(root/'static/intel.js').write_text(js,encoding='utf-8')
html=(root/'templates/intel.html').read_text(encoding='utf-8')
html=html.replace('<h1>Guild intelligence <em>command center.</em></h1><p>Track player-versus-player deaths of Non Lifers, watch their killers for subsequent deaths to guild members, and follow transfers into Premia.</p>', '<h1 id="intelHeroTitle">Non Lifers PvP deaths</h1><p id="intelHeroDesc">See who killed our members — and who Non Lifers killed afterwards.</p>')
html=html.replace('class="intel-metrics"','class="intel-metrics" id="intelMetrics"')
html=html.replace('NON LIFERS PVP DEATHS','OUR PVP DEATHS').replace('Player-caused deaths','Our members killed by players')
html=html.replace('RETALIATION DEATHS','OUR REVENGE KILLS').replace('Enemy victims killed by guild members','Enemy deaths involving Non Lifers')
html=html.replace('ENEMY PLAYERS WATCHED','ENEMIES TRACKED').replace('Unique attackers seen','Players who killed our members')
html=html.replace('TRANSFERS TO PREMIA','WORLD TRANSFERS')
html=html.replace('⚔ Guild PvP deaths','☠ Non Lifers died').replace('◎ Retaliation tracker','⚔ Non Lifers got revenge').replace('⇄ World transfers','⇄ Moved to Premia')
html=html.replace('placeholder="Search characters, killers, worlds…"','placeholder="Search player name…"')
html=html.replace('PvP deaths of Non Lifers</h2><p id="intelPanelDesc">Only deaths with identifiable player killers are listed.', 'Our members who died</h2><p id="intelPanelDesc">Only deaths caused by other players.')
html=html.replace('<footer class="intel-footer"><p>Public-game-data analysis only. Tibia.com character deaths show a limited recent history; a missing record does not establish that a death never happened. Transfer listings may be delayed or incomplete.</p></footer>', '<footer class="intel-footer"><p>Only recorded events are shown. Missing events can occur when tracking data is delayed or incomplete.</p></footer>')
(root/'templates/intel.html').write_text(html,encoding='utf-8')
css=(root/'static/intel.css').read_text(encoding='utf-8')
css+='''\n/* Simplified PvP overview */\n.intel-hero{padding:36px 0 24px}.intel-hero h1{font-size:clamp(30px,4.5vw,46px)}\n.intel-metrics{grid-template-columns:repeat(3,minmax(0,1fr))}.intel-metric:last-child{display:none}\n.intel-metrics.transfers-view{grid-template-columns:minmax(0,350px)}.intel-metrics.transfers-view .intel-metric{display:none}.intel-metrics.transfers-view .intel-metric:last-child{display:block}\n.intel-tabs button{background:#142031;border:1px solid #2d4056;padding:12px 16px;font-weight:700}\n.intel-tabs button.on{background:#354b64;border-color:#d6b87b;color:#fff}\n.intel-table{min-width:560px}.intel-table td{padding:17px 19px}.intel-table strong{font-weight:650}.intel-empty small{display:block;margin:10px auto 0;max-width:480px}\n@media(max-width:750px){.intel-metrics{grid-template-columns:repeat(2,minmax(0,1fr))}.intel-metrics .intel-metric:nth-child(3){grid-column:1/-1}.intel-tabs button{flex:1 1 140px}.intel-filter-controls{display:grid;grid-template-columns:1fr 1fr}.intel-filter-controls input{grid-column:1/-1}.intel-table{min-width:540px}}\n'''
(root/'static/intel.css').write_text(css,encoding='utf-8')
print('Simplified PvP dashboard UI applied')