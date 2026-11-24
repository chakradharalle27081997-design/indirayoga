from pathlib import Path
from datetime import datetime
import re

path = Path('index.html')
if not path.is_file():
    raise SystemExit('ERROR: Run this from the website folder containing index.html.')
html = path.read_text(encoding='utf-8')
marker_start = '/* NAVIRA SHORT HOMEPAGE V1 START */'
marker_end = '/* NAVIRA SHORT HOMEPAGE V1 END */'
if marker_start in html:
    raise SystemExit('Already applied. No changes made.')
required = ['class="hero"', 'class="services"', 'class="philosophy"', 'class="how"', 'class="navira-instructor"', 'class="navira-pricing"', 'class="faq"', '</style>']
missing = [x for x in required if x not in html]
if missing:
    raise SystemExit('ERROR: Expected elements missing: ' + ', '.join(missing))

# Move the pricing section immediately after Programs without changing its contents.
pricing_pattern = re.compile(r'\s*<section\b[^>]*class="[^"]*\bnavira-pricing\b[^"]*"[^>]*>.*?</section>', re.S)
pricing_matches = list(pricing_pattern.finditer(html))
if len(pricing_matches) != 1:
    raise SystemExit(f'ERROR: Expected exactly one pricing section, found {len(pricing_matches)}.')
pricing = pricing_matches[0].group().strip()
without_pricing = html[:pricing_matches[0].start()] + html[pricing_matches[0].end():]
services_pattern = re.compile(r'(<section\b[^>]*class="[^"]*\bservices\b[^"]*"[^>]*>.*?</section>)', re.S)
if len(services_pattern.findall(without_pricing)) != 1:
    raise SystemExit('ERROR: Cannot uniquely identify Programs section.')
html = services_pattern.sub(lambda m: m.group(1) + '\n' + pricing, without_pricing, count=1)

# All layout changes are scoped, reversible CSS. Original HTML/content remains intact.
css = r'''
/* NAVIRA SHORT HOMEPAGE V1 START */
/* Remove nonessential repetition, while retaining markup for easy rollback. */
.marquee,.stats,.conditions{display:none!important}

/* A shorter hero, with the same brand identity. */
.hero{min-height:0;padding-top:122px;padding-bottom:48px;gap:clamp(20px,3vw,48px)}
.hero h1{font-size:clamp(2.85rem,4.65vw,4.9rem);margin-bottom:17px}
.hero-badge{margin-bottom:16px}
.hero-desc{margin-bottom:18px;line-height:1.7}
.hero-tags{margin-bottom:20px}
.hero-btns{margin-bottom:20px}
.hero-proof{padding-top:14px}
.hero-visual{min-height:355px}
.hero-logo-wrap{width:min(29vw,355px);height:min(29vw,355px);min-width:260px;min-height:260px}
.hero-float-card{padding:12px 15px}

/* Editorial rhythm, not oversized blank spaces. */
.services,.how,.faq,.testimonials,.navira-pricing,.navira-instructor,.philosophy{
  padding-top:clamp(48px,5vw,72px);padding-bottom:clamp(48px,5vw,72px)
}
.section-header{margin-bottom:30px}
.section-title{font-size:clamp(1.9rem,3vw,3.05rem);margin-bottom:12px}
.section-sub{line-height:1.7}
.section-badge{margin-bottom:12px}

/* Six programs remain accessible, but read as concise offerings. */
.services-grid{gap:14px;max-width:1100px}
.service-card{min-height:0;padding:23px 23px 20px;border-radius:17px}
.service-icon{width:43px;height:43px;margin-bottom:15px}
.service-card h3{font-size:1.17rem;margin-bottom:8px}
.service-card p{font-size:.82rem;line-height:1.65;margin-bottom:12px}
.service-tag{padding:6px 10px}

/* Pricing follows programs, and reads like a clear choice. */
.navira-pricing{background:#f5f3eb}
.navira-pricing-grid{gap:16px}
.navira-price-card{padding:clamp(22px,3vw,30px);border-radius:18px}
.navira-price-card h3{margin:9px 0 6px}
.navira-price-option{padding:12px 0}
.navira-price-card .navira-price-note{margin:12px 0}
.navira-pricing-footnote{margin-top:17px}

/* Preserve the instructor as the site's premium focal point. */
.navira-instructor-grid{gap:clamp(26px,4vw,64px)}
.navira-instructor-photo{max-width:450px}
.navira-instructor-content h3{margin-top:14px}
.navira-instructor-content>p:not(.navira-instructor-role){line-height:1.7;margin-bottom:10px}
.navira-instructor-role{margin-bottom:14px}

/* Philosophy and enrollment: visually tighter without deleting information. */
.philosophy-grid{gap:clamp(25px,4vw,50px)}
.philosophy h2{font-size:clamp(2rem,3.1vw,3.2rem);margin-bottom:16px}
.philosophy-grid>div:first-child>p{line-height:1.7}
.philosophy-quote{margin:18px 0;font-size:1.08rem}
.philosophy-points{gap:9px}
.infinity-svg{max-width:340px}
.steps{gap:14px}
.step{padding:25px 23px;border-radius:17px}
.step-num{font-size:1.9rem;margin-bottom:12px}
.step h3{margin-bottom:8px}
.step p{line-height:1.65;margin-bottom:0}

/* Social proof and FAQ should be quick to scan. */
.tcarousel-track{gap:14px}
.t-card{padding:22px;gap:13px}
.t-card p.quote{line-height:1.7}
.t-more{margin-top:20px}
.faq-list{gap:9px}
.faq-q{padding:18px 22px}
.faq-a p{padding:0 22px 19px}
.cta-section{padding:65px 22px}
.cta-section h2{font-size:clamp(2.2rem,3.4vw,3.35rem);margin-bottom:15px}
footer{padding-top:48px}
.footer-top{gap:26px;padding-bottom:35px}

@media(max-width:850px){
  .hero{padding:112px 24px 44px;gap:35px}
  .hero-visual{min-height:265px}
  .hero-logo-wrap{width:235px;height:235px;min-width:0;min-height:0}
  .hero-float-card{left:50%;bottom:-7%;transform:translateX(-50%)}
  .navira-instructor-photo{margin-inline:auto}
}
@media(max-width:600px){
  .hero{padding:108px 20px 43px;gap:29px}
  .hero h1{font-size:clamp(2.15rem,9vw,2.85rem)}
  .hero-visual{min-height:245px}
  .hero-logo-wrap{width:190px;height:190px}
  .services,.how,.faq,.testimonials,.navira-pricing,.navira-instructor,.philosophy{
    padding:48px 20px
  }
  .section-header{margin-bottom:24px}
  .service-card{padding:20px}
  .step{padding:22px}
  .navira-price-card{padding:22px}
  .faq-q{padding:17px 18px}
  .faq-a p{padding:0 18px 18px}
  .cta-section{padding:55px 20px}
  footer{padding-top:43px}
}
/* NAVIRA SHORT HOMEPAGE V1 END */
'''
html = html.replace('</style>', css + '\n</style>', 1)
if html.count(marker_start) != 1 or html.count('class="navira-pricing"') != 1:
    raise SystemExit('ERROR: Validation failed; no file written.')
backup = Path('index.before-short-homepage-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.html')
backup.write_text(path.read_text(encoding='utf-8'), encoding='utf-8')
path.write_text(html, encoding='utf-8')
print('SUCCESS: Shorter homepage layout applied.')
print('Pricing moved directly after Programs.')
print('Marquee, statistics and wellness-goals grid hidden (not deleted).')
print('Original content, links, scripts and SEO retained.')
print('Backup:', backup)
print('Preview locally before committing.')
