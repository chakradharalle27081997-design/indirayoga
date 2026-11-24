from pathlib import Path
from datetime import datetime
import re

page = Path('index.html')
if not page.is_file():
    raise SystemExit('ERROR: Run this from the website folder containing index.html.')
html = page.read_text(encoding='utf-8')
marker_start = '/* NAVIRA COMPACT PREMIUM REFINEMENT START */'
marker_end = '/* NAVIRA COMPACT PREMIUM REFINEMENT END */'
if marker_start in html:
    raise SystemExit('Already applied. No changes made.')

start = html.find('<section class="faq" id="faq">')
if start == -1:
    raise SystemExit('ERROR: FAQ section not found. No changes made.')
end = html.find('</section>', start)
if end == -1:
    raise SystemExit('ERROR: FAQ closing section not found. No changes made.')
end += len('</section>')
faq = html[start:end]
header_open = '<div class="section-header reveal">'
list_open = '<div class="faq-list">'
if faq.count(header_open) != 1 or faq.count(list_open) != 1:
    raise SystemExit('ERROR: Unexpected FAQ structure. No changes made.')
head_pos = faq.index(header_open)
list_pos = faq.index(list_open)
header_region = faq[head_pos:list_pos]
items = re.findall(r'    <div class="faq-item reveal">\s*<button class="faq-q".*?</div>\s*</div>', header_region, flags=re.S)
if len(items) != 3:
    raise SystemExit(f'ERROR: Expected 3 misplaced questions, found {len(items)}. No changes made.')
# Remove only the exact three FAQ blocks, leaving the header closing div intact.
new_header = header_region
for item in items:
    if new_header.count(item) != 1:
        raise SystemExit('ERROR: FAQ item ambiguous. No changes made.')
    new_header = new_header.replace(item, '', 1)
# Insert moved items at the top of the FAQ list.
faq = faq[:head_pos] + new_header + faq[list_pos:]
faq = faq.replace(list_open, list_open + '\n' + '\n'.join(items), 1)
if faq.count('class="faq-item reveal"') != 8:
    raise SystemExit('ERROR: FAQ count is not 8. No changes made.')

css = '''
/* NAVIRA COMPACT PREMIUM REFINEMENT START */
/* Keep the editorial look; remove excessive vertical whitespace. */
.hero{min-height:0;padding-top:124px;padding-bottom:56px;gap:clamp(24px,4vw,65px)}
.hero-visual{min-height:390px}
.hero-logo-wrap{width:min(31vw,390px);height:min(31vw,390px)}
.hero h1{margin-bottom:18px}
.hero-desc{margin-bottom:18px}
.hero-tags{margin-bottom:23px}
.hero-btns{margin-bottom:23px}
.marquee{padding:10px 0}
.stats{padding:23px clamp(20px,5vw,80px)}
.stat-item{padding:11px}
.services,.how,.conditions,.faq,.testimonials,.navira-instructor,.navira-pricing{padding-top:clamp(54px,6vw,80px);padding-bottom:clamp(54px,6vw,80px)}
.philosophy{padding-top:clamp(62px,7vw,92px);padding-bottom:clamp(62px,7vw,92px)}
.section-header{margin-bottom:32px}
.section-title{margin-bottom:13px}
.services-grid,.steps,.tcarousel-track{gap:16px}
.service-card{min-height:0;padding:25px 23px}
.service-icon{margin-bottom:17px}
.service-card p{margin-bottom:12px}
.step{padding:27px 24px}
.step-num{margin-bottom:14px}
.conditions-grid{gap:10px}
.condition-pill{padding:14px 17px;min-height:55px}
.t-card{padding:24px 22px;gap:15px}
.navira-instructor-grid{gap:clamp(25px,5vw,65px)}
.navira-instructor-content h3{margin-top:17px}
.navira-price-card{padding:clamp(22px,3vw,32px)}
.navira-price-option{padding:14px 0}
.navira-pricing-footnote{margin-top:19px}
.faq-list{max-width:860px;gap:10px}
.faq-q{padding:19px 23px}
.faq-a p{padding:0 23px 19px}
.cta-section{padding:70px 24px}
footer{padding-top:55px}
.footer-top{padding-bottom:37px}
@media(max-width:850px){
  .hero{padding-top:116px;padding-bottom:54px;gap:35px}
  .hero-visual{min-height:310px}
  .hero-logo-wrap{width:265px;height:265px;min-width:0;min-height:0}
}
@media(max-width:600px){
  .hero{padding-top:112px;padding-bottom:47px;gap:32px}
  .hero-visual{min-height:245px}
  .hero-logo-wrap{width:205px;height:205px}
  .hero-float-card{bottom:-7%}
  .services,.how,.conditions,.faq,.testimonials,.navira-instructor,.navira-pricing{padding:54px 20px}
  .philosophy{padding:58px 22px}
  .section-header{margin-bottom:26px}
  .service-card{padding:23px 21px}
  .step{padding:24px 22px}
  .faq-q{padding:17px 18px}
  .faq-a p{padding:0 18px 18px}
  .cta-section{padding:62px 20px}
  footer{padding-top:48px}
}
/* NAVIRA COMPACT PREMIUM REFINEMENT END */
'''
if html.count('</style>') != 1:
    raise SystemExit('ERROR: Expected one closing style tag. No changes made.')
updated = html[:start] + faq + html[end:]
updated = updated.replace('</style>', css + '\n</style>', 1)
if updated.count('class="faq-item reveal"') != html.count('class="faq-item reveal"'):
    raise SystemExit('ERROR: FAQ item count changed unexpectedly. No changes made.')
for required in ('https://app.navirayoga.in/register', 'https://app.navirayoga.in/student'):
    if required in html and required not in updated:
        raise SystemExit('ERROR: A registration link was lost. No changes made.')
backup = page.with_name('index.before-compact-faq-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.html')
backup.write_text(html, encoding='utf-8')
page.write_text(updated, encoding='utf-8')
print('Success: Moved 3 FAQ questions into the same list as the original 5.')
print('Success: Applied compact spacing across the website.')
print('Backup:', backup)
print('Review locally before committing or pushing.')
