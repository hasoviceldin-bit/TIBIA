"""Restore a consistent, responsive Non Lifers dashboard layout.

Runs after fix_compact_enemy.py. Only presentation files are modified.
"""
from pathlib import Path
from html.parser import HTMLParser

root = Path(__file__).resolve().parent
html_path = root / 'templates/intel.html'
css_path = root / 'static/intel.css'
js_path = root / 'static/intel.js'
html = html_path.read_text(encoding='utf-8')

start = html.index('<section class="compact-enemy-box"')
end = html.index('<div class="intel-dashboard-grid">', start)
widget = html[start:end]
assert 'id="intelEnemySummary"' in widget
html = html[:start] + html[end:]
rev = html.index('<section class="intel-panel" id="revenge-deaths">')
insertion = html.index('<div class="intel-table-scroll">', rev)
html = html[:insertion] + widget + html[insertion:]
html_path.write_text(html, encoding='utf-8')

# Replacing historical CSS overrides instead of appending another CSS stack
# avoids competing fixed min-widths / mobile breakpoints.
css = r'''/* Non Lifers unified dashboard — stable responsive layout */
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
body.intelligence{margin:0;min-width:0;overflow-x:hidden;background:#090e16;color:#e6edf5;font:14px/1.5 Inter,system-ui,-apple-system,"Segoe UI",sans-serif}
.intel-shell{width:min(100% - 48px,1380px);max-width:1380px;margin-inline:auto;padding:0 0 48px;min-width:0}
.intel-shell :is(section,div,header,article,nav){min-width:0}
.intel-header{display:flex;align-items:center;justify-content:space-between;gap:22px;padding:23px 0;border-bottom:1px solid #263348;flex-wrap:wrap}
.intel-brand{color:#f0c879;font-size:16px;font-weight:800;letter-spacing:.055em;text-decoration:none}
.intel-brand .muted{color:#9daebf;font-weight:600}
.intel-header nav{display:flex;flex-wrap:wrap;align-items:center;gap:20px}
.intel-header nav a{color:#a2b1c1;text-decoration:none;font-size:13px;font-weight:600}
.intel-header nav a:hover,.intel-header nav a.active{color:#f6ce82}
.intel-hero{padding:32px 0 19px}
.intel-hero .eyebrow{color:#d7b77d;font-size:11px;font-weight:800;letter-spacing:.14em}
.intel-hero h1{color:#f3f5fa;font-size:clamp(30px,3.2vw,44px);line-height:1.12;letter-spacing:-.035em;margin:9px 0 8px;font-weight:750}
.intel-hero h1 em{font-style:normal;color:#dfb878}
.intel-hero p{color:#9fafc1;font-size:13px;line-height:1.6;margin:0;max-width:790px}
.intel-controls{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;margin:16px 0 11px}
.intel-filter-controls{display:flex;align-items:center;flex-wrap:wrap;gap:10px;flex:1 1 330px}
.intel-filter-controls :is(input,select){min-height:41px;border:1px solid #37465a;background:#141e2c;color:#e6edf5;border-radius:8px;padding:9px 12px;font:inherit;font-size:12px}
.intel-filter-controls input{flex:1 1 230px;min-width:0;max-width:480px}
.intel-filter-controls select{flex:0 1 auto;max-width:180px}
.intel-actions{display:flex;align-items:center;flex-wrap:wrap;gap:9px;margin:0}
.intel-actions :is(button,a){display:inline-flex;align-items:center;justify-content:center;min-height:41px;margin:0;padding:9px 14px;border:1px solid #57677e;background:#1b2738;color:#f1cd8b;border-radius:8px;white-space:nowrap;font-size:12px;font-weight:700;text-decoration:none;cursor:pointer}
.intel-actions :is(button,a):hover{background:#29364a}
.intel-status-row{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin:8px 0 10px;color:#91a2b4;font-size:11px}
.intel-notice{padding:11px 13px;border:1px solid #31485c;border-radius:9px;background:#101d2b;color:#b0c1d4;font-size:12px;margin:0 0 19px}
.intel-notice.warning{border-color:#78553c;background:#2b211d;color:#f1ba91}
.intel-metrics,.intel-metrics.transfers-view{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px;margin:0 0 19px}
.intel-metrics .intel-metric,.intel-metrics.transfers-view .intel-metric{display:flex;flex-direction:column;min-width:0}
.intel-metric{position:relative;overflow:hidden;padding:18px 19px;border:1px solid #314056;border-radius:12px;background:#151f30;text-decoration:none!important;color:#eaf0f7;min-height:142px}
.intel-metric::before{content:"";position:absolute;inset:0 0 auto;height:3px;background:#96a9d2}
.intel-metric.loss::before{background:#ed909a}.intel-metric.win::before{background:#82d7b1}.intel-metric.neutral::before{background:#93a8d6}.intel-metric.transfer::before{background:#e3c17d}
.intel-metric>span{color:#a7b7c8;font-size:10px;font-weight:800;letter-spacing:.08em}
.intel-metric strong{display:block;margin:10px 0 4px;color:#fff;font-size:34px;letter-spacing:-.03em;line-height:1.05;font-weight:750}
.intel-metric small{display:flex;justify-content:space-between;gap:12px;margin-top:auto;color:#9faec0;font-size:11px;line-height:1.4}
.intel-metric small b{color:#d8bb7d}
.intel-metric:hover{background:#1c293b;border-color:#58677c}
.intel-dashboard-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));align-items:start;gap:16px}
.intel-panel{min-width:0;overflow:hidden;background:#131d2d;border:1px solid #334158;border-radius:13px}
.intel-panel.transfers-panel{grid-column:1/-1}
.intel-panel-top{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:17px 19px;border-bottom:1px solid #2d3b50}
.intel-panel-top>div{min-width:0}
.intel-panel-top h2{margin:0 0 4px;font-size:18px;line-height:1.3;color:#f0f4fa}
.intel-panel-top p{margin:0;color:#9bacbe;font-size:11px;line-height:1.5}
.intel-panel-pill{flex:0 0 auto;padding:5px 7px;border:1px solid #364456;border-radius:6px;color:#9aacc1;font-size:9px;font-weight:700;letter-spacing:.04em;white-space:nowrap}
.intel-section-icon{display:none}
.intel-table-scroll{max-width:100%;overflow-x:auto;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch}
.intel-table{width:100%;min-width:410px;table-layout:fixed;border-collapse:collapse;color:#dce5ee;font-size:12px}
.intel-table th{text-align:left;white-space:nowrap;text-transform:uppercase;letter-spacing:.05em;color:#94a6bb;background:#1b293b;font-size:9px;font-weight:800;padding:12px 14px}
.intel-table td{padding:13px 14px;border-top:1px solid #2b384b;vertical-align:top;overflow-wrap:anywhere;word-break:normal;line-height:1.5}
.intel-table th:nth-child(1){width:32%}.intel-table th:nth-child(2){width:40%}.intel-table th:nth-child(3){width:28%}
.intel-table tr:hover td{background:#1a2939}
.intel-table td a{color:#edcf94;text-decoration:none;font-weight:700;overflow-wrap:anywhere}
.intel-table td a:hover{text-decoration:underline}
.intel-table td strong{display:block;line-height:1.5}
.intel-table td small{display:block;margin-top:3px;color:#8c9dac;font-size:10px}
.intel-empty{padding:30px 12px!important;text-align:center;color:#a5b6c7}
.intel-arrow{color:#d8bd81;font-weight:800}
.intel-footer{margin:24px 0;color:#8495aa;font-size:11px;line-height:1.6}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
/* Compact summary sits inside the revenge panel, never as a detached card. */
.compact-enemy-box{width:100%;max-width:none;margin:0;padding:13px 17px 15px;background:#162337;border:0;border-bottom:1px solid #344258;border-radius:0}
.compact-enemy-title{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px}
.compact-enemy-title h2{margin:0;font-size:13px;font-weight:750;color:#e9eef6}
.compact-enemy-title p{margin:3px 0 0;font-size:10px;color:#a1b2c6}
.compact-enemy-title>span{white-space:nowrap;color:#9baec5;font-size:10px}
.compact-enemy-title>span strong{color:#e3c47e;font-size:13px}
.compact-enemy-labels,.compact-enemy-row{display:grid;grid-template-columns:minmax(0,1fr) 64px 58px 50px;align-items:center;column-gap:8px}
.compact-enemy-labels{padding:0 0 7px;color:#92a7bf;font-size:9px;font-weight:700}
.compact-enemy-labels span:not(:first-child){text-align:center}
.compact-enemy-row{border-top:1px solid #34445b;padding:9px 0;font-size:11px}
.compact-enemy-name{min-width:0;font-weight:700;overflow-wrap:anywhere}
.compact-enemy-name a{color:#edcf94;text-decoration:none}
.compact-enemy-num{text-align:center;font-size:13px;font-weight:800;font-variant-numeric:tabular-nums}
.compact-red{color:#ef9da5}.compact-green{color:#87d9b2}
.compact-enemy-detail{min-width:0;text-align:center;font-size:10px}
.compact-enemy-detail summary,.compact-enemy-more>summary{cursor:pointer;color:#d7c3a2}
.compact-enemy-detail[open]{grid-column:1/-1;text-align:left;border-top:1px solid #384963;padding:9px 0 2px;margin-top:7px}
.compact-enemy-detail ul{margin:8px 0 0;padding:0;list-style:none}
.compact-enemy-detail li{display:flex;flex-wrap:wrap;gap:6px;justify-content:space-between;padding:6px 0;border-top:1px solid #314158}
.compact-enemy-detail li a{color:#edcf94}
.compact-enemy-no-detail{text-align:center;color:#8495aa}
.compact-enemy-more{padding:10px 0 0;border-top:1px solid #3a4a62;font-size:11px}
.compact-enemy-empty{margin:5px 0;font-size:11px;color:#98abc0}
@media(max-width:1100px){.intel-dashboard-grid{grid-template-columns:minmax(0,1fr)}.intel-panel.transfers-panel{grid-column:auto}.intel-metrics,.intel-metrics.transfers-view{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:640px){
.intel-shell{width:calc(100% - 28px);padding-bottom:30px}
.intel-header{padding:17px 0;gap:12px}.intel-brand{font-size:13px}.intel-header nav{width:100%;gap:16px}
.intel-header nav a{font-size:12px}
.intel-hero{padding:24px 0 12px}.intel-hero h1{font-size:30px}.intel-hero p{font-size:12px}
.intel-controls{display:grid;grid-template-columns:minmax(0,1fr);gap:10px}
.intel-filter-controls{display:grid;grid-template-columns:minmax(0,1fr) 130px;width:100%}
.intel-filter-controls input{width:100%;min-width:0;max-width:none}
.intel-filter-controls select{width:100%;max-width:none}
.intel-actions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));width:100%}
.intel-actions :is(button,a){font-size:11px;padding:10px 8px;white-space:normal}
.intel-status-row{font-size:10px}
.intel-metrics,.intel-metrics.transfers-view{gap:9px}
.intel-metric{min-height:116px;padding:13px 12px}.intel-metric>span{font-size:9px}.intel-metric strong{font-size:27px}.intel-metric small{font-size:10px}
.intel-dashboard-grid{gap:12px}.intel-panel-top{padding:15px 12px;align-items:flex-start}.intel-panel h2{font-size:15px}.intel-panel-top p{font-size:10px}
.intel-panel-pill{display:none}
.intel-table{min-width:360px;font-size:11px}.intel-table th{padding:10px 9px;font-size:9px}.intel-table td{padding:12px 9px}
.compact-enemy-box{padding:13px 11px}.compact-enemy-labels,.compact-enemy-row{grid-template-columns:minmax(0,1fr) 47px 47px 46px;gap:4px}.compact-enemy-labels{font-size:8px}
}
@media(max-width:365px){.intel-filter-controls{grid-template-columns:minmax(0,1fr)}.intel-metrics,.intel-metrics.transfers-view{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.compact-enemy-labels,.compact-enemy-row{grid-template-columns:minmax(0,1fr) 44px 43px 43px}}
'''
css_path.write_text(css, encoding='utf-8')

# Make the number of enemies summarized small enough to keep the revenge
# panel balanced; expand only if the user requests more.
js = js_path.read_text(encoding='utf-8')
js = js.replace('const topEnemies = enemies.slice(0, 5);','const topEnemies = enemies.slice(0, 4);')
js = js.replace('const extraEnemies = enemies.slice(5);','const extraEnemies = enemies.slice(4);')
js_path.write_text(js,encoding='utf-8')

class Check(HTMLParser):
    def __init__(self): super().__init__(); self.ids=[]; self.stack=[]; self.ok=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='section' and a.get('id')=='revenge-deaths': self.stack.append('revenge')
        if a.get('id')=='intelEnemySummary' and 'revenge' in self.stack:self.ok=True
    def handle_endtag(self,tag):
        if tag=='section' and self.stack: self.stack.pop()
check=Check();check.feed(html)
assert check.ok and len(check.ids)==len(set(check.ids)), 'Dashboard ids broken'
assert html.count('id="intelEnemySummary"')==1
assert '@media(max-width:640px)' in css and '.intel-dashboard-grid' in css
print('Responsive dashboard cleanup applied; enemy summary nested in revenge panel')