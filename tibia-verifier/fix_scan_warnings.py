"""Distinguish partial source failures from an unavailable tracker."""
from pathlib import Path
root = Path(__file__).resolve().parent
p = root / 'intel.py'
s = p.read_text(encoding='utf-8')
old = "if not records:raise ValueError('No matching Premia transfers in the fetched page')"
assert old in s, 'Transfer handling changed; review needed'
s = s.replace(old, "if not records:continue  # No matching transfers is not a source error", 1)
needle = "\n\n@router.get('/intel',response_class=HTMLResponse)"
assert needle in s, 'Missing routes'
health = '''\n\ndef _scan_health():
    """Report real outages, not isolated retries or zero-new-transfer pages."""
    errors = json.loads(meta('last_errors', '[]'))
    summary = json.loads(meta('last_summary', '{}'))
    guild_problem = any(e.startswith('Guild roster:') for e in errors)
    feed_failures = sum(e.startswith('Tibia Tracker feed:') for e in errors)
    transfer_failures = sum(e.startswith(('Tibia Tracker:', 'Tibia Tracker recent:', 'GuildStats:')) for e in errors)
    unexpected = any(e.startswith('Unexpected ') for e in errors)
    no_character_checks = summary.get('members_checked', 0) == 0
    deaths_down = unexpected or (guild_problem and feed_failures >= 2 and no_character_checks)
    transfers_down = unexpected or transfer_failures >= 3
    return {
        'deaths': 'Death updates are temporarily unavailable. Previously recorded deaths remain visible.' if deaths_down else '',
        'transfers': 'World-transfer updates are temporarily unavailable. Previously recorded transfers remain visible.' if transfers_down else '',
        'partial': bool(errors),
    }
'''
s = s.replace(needle, health+needle,1)
old_status = "'source_warnings':len(json.loads(meta('last_errors','[]'))),"
assert old_status in s, 'Warning shape changed; review needed'
s = s.replace(old_status, "'health':_scan_health(),", 1)
s += '''\n\n@router.get('/api/intel/diagnostics')
def intel_admin_diagnostics(request:Request):
    main().require_admin(request)
    return {'last_attempt':meta('last_attempt'),
            'summary':json.loads(meta('last_summary','{}')),
            'errors':json.loads(meta('last_errors','[]'))}
'''
p.write_text(s, encoding='utf-8')
p = root / 'static/intel.js'
s = p.read_text(encoding='utf-8')
old_ui = """    $('intelNotice').className = 'intel-notice' + (status.source_warnings ? ' warning' : '');
    $('intelNotice').textContent = status.source_warnings
      ? 'Some updates are temporarily unavailable. The list may be incomplete.'
      : status.running ? 'Checking for new events…'
      : 'Showing recorded events. Some older deaths or transfers may be missing.';"""
assert old_ui in s, 'Simplified UI changed; review needed'
new_ui = """    const health = status.health || {};
    const outage = state.tab === 'transfers' ? health.transfers : health.deaths;
    $('intelNotice').className = 'intel-notice' + (outage ? ' warning' : '');
    $('intelNotice').textContent = outage || (status.running
      ? 'Checking for new events…'
      : health.partial ? 'Showing recorded events. Some sources could not be checked; recent results may be incomplete.'
      : 'Showing recorded events. Older events may be missing.');"""
s = s.replace(old_ui,new_ui,1)
p.write_text(s,encoding='utf-8')
print('Severity-aware scan status and protected diagnostics applied')
