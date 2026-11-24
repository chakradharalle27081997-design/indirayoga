from pathlib import Path
from datetime import datetime
import re

path = Path('index.html')
if not path.is_file():
    raise SystemExit('ERROR: Run this script from the website folder containing index.html.')
html = path.read_text(encoding='utf-8')
marker_start = '/* NAVIRA FINAL REFINEMENTS START */'
marker_end = '/* NAVIRA FINAL REFINEMENTS END */'
if marker_start in html:
    raise SystemExit('Already applied. No changes made.')
for required in ('</style>', 'class="philosophy', 'class="hero-logo-wrap', 'id="nav"'):
    if required not in html:
        raise SystemExit(f'ERROR: Expected site markup missing: {required}. No changes made.')

# Adjust only the desktop navigation link; leave other occurrences and footer links alone.
nav = re.search(r'<nav\b[^>]*>.*?</nav>', html, re.S | re.I)
if not nav:
    raise SystemExit('ERROR: Could not identify desktop navigation. No changes made.')
nav_text = nav.group(0)
# Link must exist to safely replace it.
new_nav, nav_count = re.subn(r'(<a\b[^>]*href=["\'])#conditions(["\'][^>]*>)\s*Wellness Goals\s*(</a>)',
                             r'\1#navira-pricing\2Pricing\3', nav_text, count=1, flags=re.I)
# Some versions use a different visible label; still replace its target.
if not nav_count:
    new_nav, nav_count = re.subn(r'(<a\b[^>]*href=["\'])#conditions(["\'][^>]*>).*?(</a>)',
                                 r'\1#navira-pricing\2Pricing\3', nav_text, count=1, flags=re.S | re.I)
if not nav_count:
    raise SystemExit('ERROR: Wellness Goals link not found in desktop navigation. No changes made.')
html = html[:nav.start()] + new_nav + html[nav.end():]

# Mobile menu may duplicate the same link; update only that menu, if present.
mobile = re.search(r'<div\b[^>]*class=["\'][^"\']*mobile-menu[^"\']*["\'][^>]*>.*?</div>', html, re.S | re.I)
if mobile:
    mobile_text = mobile.group(0)
    changed, _ = re.subn(r'(<a\b[^>]*href=["\'])#conditions(["\'][^>]*>).*?(</a>)',
                          r'\1#navira-pricing\2Pricing\3', mobile_text, count=1, flags=re.S | re.I)
    html = html[:mobile.start()] + changed + html[mobile.end():]

# CSS-only visual refinements: existing philosophy copy stays in HTML for safe rollback;
# redundant quote is hidden visually, and a concise caption is added beneath the SVG.
css = '''
/* NAVIRA FINAL REFINEMENTS START */
/* A compact, balanced editorial philosophy section. */
.philosophy { padding-top: clamp(54px, 5.5vw, 78px); padding-bottom: clamp(54px, 5.5vw, 78px); }
.philosophy-grid { gap: clamp(24px, 4vw, 56px); grid-template-columns: minmax(0, 1.12fr) minmax(0, .88fr); }
.philosophy h2 { font-size: clamp(2rem, 3.2vw, 3.25rem); margin-bottom: 17px; }
.philosophy-grid > div:first-child > p { line-height: 1.75; margin-bottom: 16px; }
.philosophy-quote { display: none; }
.philosophy-points { gap: 10px; margin-top: 20px; }
.philosophy-points div { line-height: 1.55; }
.philosophy-visual { align-content: center; gap: 8px; }
.infinity-svg { max-width: 510px; }
.philosophy-visual::after {
  content: "A practice that grows with you";
  display: block;
  color: #ead7ae;
  font-family: Fraunces, Georgia, serif;
  font-size: clamp(1rem, 1.55vw, 1.3rem);
  font-style: italic;
  text-align: center;
  line-height: 1.45;
  margin-top: 2px;
}
/* Make the hero emblem less dominant while preserving its circular design. */
@media (min-width: 851px) {
  .hero-logo-wrap { width: min(30vw, 385px); height: min(30vw, 385px); min-width: 270px; min-height: 270px; }
  .hero-float-card { left: -5%; bottom: -2%; }
}
@media (max-width: 850px) {
  .philosophy-grid { grid-template-columns: 1fr; gap: 18px; }
  .philosophy-visual { max-width: 360px; margin: 0 auto; }
  .infinity-svg { max-width: 360px; }
}
@media (max-width: 600px) {
  .philosophy { padding: 54px 22px; }
  .philosophy h2 { font-size: clamp(1.95rem, 8vw, 2.3rem); }
  .philosophy-visual { max-width: 270px; }
  .infinity-svg { max-width: 270px; }
  .hero-float-card { bottom: -14%; }
}
/* NAVIRA FINAL REFINEMENTS END */
'''
html = html.replace('</style>', css + '\n</style>', 1)
# Safety check: preserve known portal destinations if present in original.
original = path.read_text(encoding='utf-8')
for url in ('https://app.navirayoga.in/register', 'https://app.navirayoga.in/student'):
    if url in original and url not in html:
        raise SystemExit(f'ERROR: Protected portal link lost: {url}. No changes made.')
backup = path.with_name('index.before-final-refinements-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.html')
backup.write_text(original, encoding='utf-8')
path.write_text(html, encoding='utf-8')
print('SUCCESS: Final NaviraYoga refinements applied.')
print('Backup:', backup)
print('Updated: desktop navigation, mobile navigation (if present), hero, Navira Method.')
print('Next: git diff --check; preview locally; commit only index.html if satisfied.')
