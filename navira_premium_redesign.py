from pathlib import Path
from datetime import datetime
import sys

root = Path(__file__).resolve().parent
# Script is intended to be copied into the site folder.
page = root / 'index.html'
if not page.exists():
    sys.exit('STOP: Put this script beside index.html in your website folder.')
s = page.read_text(encoding='utf-8')
marker = '/* NAVIRAYOGA PREMIUM EDITORIAL V2 — SAFE CSS ONLY */'
if marker in s:
    sys.exit('Already applied. No changes made.')
if s.count('</style>') != 1 or s.count('<style>') != 1:
    sys.exit('STOP: Expected exactly one CSS style block.')
for required in ['class="hero"','class="services"','class="navira-instructor"','class="navira-pricing"','class="testimonials"','class="faq"','class="cta-section"']:
    if required not in s:
        sys.exit(f'STOP: Missing expected section {required}. No changes made.')
css = r'''
/* NAVIRAYOGA PREMIUM EDITORIAL V2 — SAFE CSS ONLY */
:root {
  --ivory:#f8f7f1;--paper:#f1efe6;--olive:#31432e;
  --olive-ink:#263b2b;--olive-deep:#263b2b;--olive-black:#1d3023;
  --sage:#879775;--sage-pale:#edf0e7;--gold:#b68b42;
  --gold-deep:#956d2f;--gold-pale:#e9d7b4;
  --ink:#263b2b;--muted:#5f6c5e;
}
body{background:var(--ivory);color:var(--ink)}
main{overflow:clip}
main section{scroll-margin-top:88px}
.section-header{max-width:800px;margin-bottom:56px}
.section-title{font-size:clamp(2.45rem,4.1vw,4.25rem);line-height:1.12;letter-spacing:-.035em;font-weight:600;text-wrap:balance}
.section-sub{font-size:clamp(.94rem,1.05vw,1.04rem);line-height:1.9;max-width:630px}
.section-badge{letter-spacing:.19em;font-size:.69rem}
.section-badge:before{width:22px}
nav{background:rgba(248,247,241,.96);border-bottom:1px solid rgba(38,59,43,.12)}
.nav-links .nav-cta{box-shadow:0 10px 25px rgba(29,48,35,.14)}
.hero{min-height:780px;padding-top:158px;padding-bottom:105px;gap:clamp(45px,6vw,100px);background:radial-gradient(ellipse 540px 540px at 85% 43%,#e8e9dc 0%,transparent 75%),var(--ivory)}
.hero h1{font-size:clamp(3.5rem,5.7vw,6rem);line-height:1.07;letter-spacing:-.047em}
.hero h1 em{color:var(--olive);font-style:italic}
.hero-desc{line-height:1.95;max-width:560px}
.hero-tag{background:#fffdf8;border-color:rgba(49,67,46,.13);padding:10px 15px}
.hero-logo-disc{background:#fffdf9;box-shadow:0 28px 85px rgba(29,48,35,.12),0 0 0 12px rgba(255,255,255,.55)}
.hero-logo-ring{border-color:rgba(182,139,66,.33)}
.hero-float-card{border-radius:18px;box-shadow:0 18px 45px rgba(29,48,35,.11)}
.marquee{background:#30452f;padding:17px 0}
.marquee-track>span{font-size:1.03rem}
.stats{background:#263b2b;padding-top:47px;padding-bottom:47px}
.stat-num{font-size:clamp(1.65rem,2.5vw,2.5rem)}
.stat-label{letter-spacing:.02em}
.services,.how,.conditions,.faq,.testimonials,.navira-pricing{padding-top:clamp(90px,9vw,140px);padding-bottom:clamp(90px,9vw,140px)}
.services{background:#f8f7f1}
.services-grid{max-width:1170px;gap:22px}
.service-card{background:#fffefa;border:1px solid rgba(38,59,43,.1);border-radius:22px;padding:38px 32px;min-height:295px;box-shadow:0 12px 35px rgba(29,48,35,.035)}
.service-card:before{height:2px;opacity:.55}
.service-card:hover{box-shadow:0 24px 60px rgba(29,48,35,.1);border-color:rgba(182,139,66,.38)}
.service-icon{background:#edf0e7;border-radius:50%;width:58px;height:58px;margin-bottom:30px}
.service-card h3{font-size:1.48rem;line-height:1.25}
.service-card p{font-size:.88rem;line-height:1.9}
.service-tag{background:#f1efe6;border-radius:999px;padding:9px 14px}
.philosophy{background:linear-gradient(135deg,#304631,#1d3023);padding-top:clamp(100px,10vw,150px);padding-bottom:clamp(100px,10vw,150px)}
.philosophy-grid{gap:clamp(40px,6vw,95px)}
.philosophy h2{font-size:clamp(2.6rem,4vw,4.5rem);letter-spacing:-.035em}
.philosophy-grid>div:first-child>p{line-height:2}
.philosophy-quote{font-size:clamp(1.18rem,1.5vw,1.45rem);line-height:1.8}
.navira-instructor{background:#f8f7f1;padding-top:clamp(90px,9vw,140px);padding-bottom:clamp(90px,9vw,140px)}
.navira-instructor-grid{max-width:1170px;gap:clamp(40px,6vw,90px)}
.navira-instructor-photo{border-radius:24px;box-shadow:0 24px 70px rgba(29,48,35,.12)}
.navira-instructor-content .section-title{font-size:clamp(2.5rem,3.6vw,3.85rem)}
.navira-instructor-content>p:not(.navira-instructor-role){font-size:.96rem;line-height:1.95}
.how{background:#f1efe6}
.steps{max-width:1170px;gap:22px}
.step{background:#fffefa;border-radius:22px;padding:42px 35px;border:1px solid rgba(38,59,43,.1);box-shadow:0 12px 32px rgba(29,48,35,.035)}
.step-num{font-size:3rem;margin-bottom:24px;color:var(--gold-deep)}
.step h3{font-size:1.45rem;line-height:1.3}
.step p{font-size:.88rem;line-height:1.9}
.conditions{background:#f8f7f1}
.conditions-grid{max-width:1100px;gap:16px}
.condition-pill{background:#fffefa;border:1px solid rgba(38,59,43,.1);border-radius:17px;min-height:76px;padding:21px 24px;box-shadow:0 8px 26px rgba(29,48,35,.025)}
.condition-pill span:last-child{font-size:.85rem}
.navira-pricing{background:#f1efe6}
.navira-pricing-grid{max-width:1060px;gap:28px}
.navira-price-card{background:#fffefa;border:1px solid rgba(38,59,43,.12);border-radius:24px;padding:clamp(32px,4vw,50px);box-shadow:0 18px 48px rgba(29,48,35,.05)}
.navira-price-card h3{font-size:clamp(2rem,3vw,2.7rem);line-height:1.2}
.navira-price-option{padding:24px 0}
.navira-price-option strong{color:var(--olive-black)}
.navira-price-link{display:inline-flex;align-items:center;min-height:46px}
.testimonials{background:#edf0e7}
.tcarousel-track{gap:22px}
.t-card{background:#fffefa;border-radius:22px;padding:35px 32px;box-shadow:0 14px 40px rgba(29,48,35,.045)}
.t-card p.quote{font-size:.92rem;line-height:1.95}
.t-avatar{background:#344d35}
.faq{background:#f8f7f1}
.faq-list{max-width:920px;gap:15px}
.faq-item{background:#fffefa;border-radius:17px;border:1px solid rgba(38,59,43,.12)}
.faq-q{font-size:1.17rem;padding:28px 32px}
.faq-a p{font-size:.9rem;line-height:1.95;padding-left:32px;padding-right:32px}
.cta-section{background:#2c432e;padding:clamp(95px,10vw,150px) 24px}
.cta-section h2{font-size:clamp(2.8rem,4.5vw,4.8rem);letter-spacing:-.035em}
.cta-section>p{line-height:1.95}
.btn-primary,.btn-outline,.btn-gold,.btn-whatsapp{transition:transform .2s,background .2s,box-shadow .2s}
.btn-primary:hover,.btn-gold:hover,.btn-whatsapp:hover{transform:translateY(-2px)}
footer{background:#1d3023;padding-top:90px}
.footer-top{gap:clamp(25px,4vw,55px)}
.footer-desc{line-height:2}
.footer-col h2{font-size:1.16rem}
.footer-col a,.footer-col p{line-height:2.35}
@media(max-width:1150px){.hero{min-height:auto}.services-grid{gap:18px}}
@media(max-width:850px){.hero{padding-top:135px;padding-bottom:85px;gap:50px}.hero h1{font-size:clamp(2.9rem,7.7vw,4.5rem)}.philosophy-grid{gap:45px}.navira-instructor-grid{grid-template-columns:1fr}.navira-instructor-photo{max-width:510px;margin:0 auto}.navira-instructor-content{max-width:700px;margin:auto}}
@media(max-width:760px){.navira-pricing-grid{grid-template-columns:1fr}.navira-price-card{padding:30px}.navira-instructor,.navira-pricing{padding:76px 6%}}
@media(max-width:600px){.section-header{margin-bottom:38px}.section-title{font-size:clamp(2.1rem,9vw,2.8rem)}.hero{padding:10rem 21px 65px;gap:40px}.hero h1{font-size:clamp(2.35rem,10vw,3.25rem)}.hero-desc{line-height:1.8}.services,.how,.conditions,.faq,.testimonials{padding:78px 20px}.service-card{min-height:0;padding:31px 26px}.step{padding:33px 27px}.condition-pill{min-height:60px;padding:15px 20px}.philosophy{padding:90px 22px}.philosophy h2{font-size:2.35rem}.t-card{padding:27px}.faq-q{font-size:1.02rem;padding:23px}.faq-a p{padding:0 23px 23px}.cta-section{padding:90px 20px}.footer-top{gap:30px}footer{padding-top:75px}}
@media(prefers-reduced-motion:reduce){.service-card:hover,.btn-primary:hover,.btn-gold:hover,.btn-whatsapp:hover{transform:none}}
'''
# Check before writing. Never touch meta tags, HTML, JS or original CSS.
updated = s.replace('</style>', css + '\n</style>', 1)
backup = root / ('index.before-premium-editorial-v2-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.html')
backup.write_text(s, encoding='utf-8')
page.write_text(updated, encoding='utf-8')
print('SUCCESS: Premium editorial CSS applied to all sections.')
print('Backup:', backup.name)
print('Only index.html changed; no deployment performed.')
