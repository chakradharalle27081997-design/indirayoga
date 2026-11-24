from pathlib import Path
import shutil

path = Path("index.html")
backup = Path("index.before-hybrid-v1.html")

html = path.read_text(encoding="utf-8")

changes = [
    (
        '<div class="hero-badge">Personalized Yoga | Hatha Yoga | Pranayama</div>',
        '<div class="hero-badge">Live Online Yoga · Instructor-Led · Across India</div>'
    ),
    (
        '<p class="hero-desc">Discover personalized yoga, Hatha Yoga, pranayama and mindful movement to support flexibility, strength, balance and everyday well-being.</p>',
        '<p class="hero-desc">Discover live online yoga classes designed around your experience, comfort and goals. Practice Hatha Yoga, Pranayama and mindful movement with personal instructor guidance.</p>'
    ),
    (
        '''    <div class="hero-tags">
      <span class="hero-tag">Hatha Yoga</span>
      <span class="hero-tag">Pranayama</span>
      <span class="hero-tag">Mindful Movement</span>
      <span class="hero-tag">Online Sessions</span>
      <span class="hero-tag">Progressive Plans</span>
      <span class="hero-tag">EN &amp; Español</span>
    </div>''',
        '''    <div class="hero-tags">
      <span class="hero-tag">Personalized Guidance</span>
      <span class="hero-tag">Beginner-Friendly</span>
      <span class="hero-tag">Live Online Classes</span>
    </div>'''
    ),
    (
        '''      <a href="https://app.navirayoga.in/register" target="_blank" class="btn-primary">Start Your Journey</a>
      <a href="https://wa.me/917996272792" target="_blank" class="btn-outline">WhatsApp Us</a>''',
        '''      <a href="https://app.navirayoga.in/register" target="_blank" rel="noopener noreferrer" class="btn-primary">Start Your Journey</a>
      <a href="#services" class="btn-outline">Explore Programs</a>
      <a href="https://wa.me/917996272792" target="_blank" rel="noopener noreferrer" class="hero-contact-link">Questions? WhatsApp Us</a>'''
    ),
    (
        '''    .hero-visual { order: -1; }''',
        '''    .hero-visual { order: 0; }'''
    )
]

for old, new in changes:
    count = html.count(old)
    if count != 1:
        raise SystemExit(
            f"Stopped safely: expected one match, found {count}: {old[:65]!r}"
        )
    html = html.replace(old, new, 1)

css = """
  /* Hybrid redesign v1: hero actions and responsive improvements */
  .hero-contact-link {
    display: inline-flex;
    align-items: center;
    color: var(--olive);
    font-size: 0.88rem;
    font-weight: 700;
    text-decoration: underline;
    text-underline-offset: 4px;
    padding: 0.8rem 0.2rem;
  }

  .hero-contact-link:hover {
    color: var(--gold-deep);
  }

  .hero-btns {
    align-items: center;
    gap: 0.8rem;
  }

  @media (max-width: 768px) {
    .hero {
      min-height: auto;
      padding-top: 7.5rem;
    }

    .hero-badge {
      font-size: 0.67rem;
      line-height: 1.5;
      text-align: center;
    }

    .hero-btns {
      flex-direction: column;
      align-items: stretch;
      max-width: 360px;
      margin-left: auto;
      margin-right: auto;
    }

    .hero-btns .btn-primary,
    .hero-btns .btn-outline,
    .hero-contact-link {
      justify-content: center;
      text-align: center;
    }

    .hero-contact-link {
      padding: 0.65rem;
    }

    .hero-visual {
      order: 0;
    }
  }
"""

marker = "</style>"

if html.count(marker) != 1:
    raise SystemExit("Stopped safely: expected exactly one closing style tag.")

html = html.replace(marker, css + "\n" + marker, 1)

shutil.copy2(path, backup)
path.write_text(html, encoding="utf-8")

print("Hybrid redesign v1 applied successfully.")
print(f"Backup created: {backup}")
