from pathlib import Path
import json
import shutil

path = Path("index.html")
html = path.read_text(encoding="utf-8")

def change(old, new):
    global html
    count = html.count(old)
    if count != 1:
        raise SystemExit(
            f"STOPPED: Expected 1 match, found {count}: {old[:90]}"
        )
    html = html.replace(old, new, 1)

change(
    "<title>Navira Yoga Studio | Personalized Yoga, Hatha &amp; Pranayama</title>",
    "<title>Online Yoga Classes in Hyderabad | Navira Yoga Studio</title>"
)

change(
    '<meta name="description" content="Personalized yoga, Hatha Yoga and pranayama at Navira Yoga Studio. Based in Hyderabad, currently offering online sessions across India." />',
    '<meta name="description" content="Join personalized online yoga classes at Navira Yoga Studio, Hyderabad. Explore Hatha Yoga, Pranayama and mindful movement with instructor-led sessions across India." />'
)

change(
    "Every student receives a thoughtfully crafted asana sequence \u2014 designed around your health conditions, injuries, lifestyle and goals. Your plan evolves every cycle.",
    "Every student receives a thoughtfully prepared yoga sequence based on their experience, comfort and goals. Your instructor reviews and adapts your practice as you progress."
)

structured_data = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Navira Yoga Studio",
    "url": "https://www.navirayoga.in/",
    "logo": "https://www.navirayoga.in/logo-icon.png",
    "description": (
        "Navira Yoga Studio is based in Hyderabad, Telangana, "
        "and currently offers instructor-led online yoga classes "
        "across India, including personalized yoga, Hatha Yoga "
        "and Pranayama."
    ),
    "areaServed": {
        "@type": "Country",
        "name": "India"
    },
    "knowsAbout": [
        "Online yoga classes",
        "Hatha Yoga",
        "Pranayama",
        "Personalized yoga",
        "Mindful movement"
    ]
}

script = (
    '<script type="application/ld+json">\n'
    + json.dumps(structured_data, indent=2, ensure_ascii=True)
    + '\n</script>\n'
)

change(
    '<link rel="canonical" href="https://www.navirayoga.in/" />',
    '<link rel="canonical" href="https://www.navirayoga.in/" />\n'
    + script.rstrip("\n")
)

backup = Path("index.before-seo-update.html")

if backup.exists():
    raise SystemExit("STOPPED: SEO backup already exists.")

shutil.copy2(path, backup)
path.write_text(html, encoding="utf-8")

print("SUCCESS: SEO improvements saved.")
print("Backup:", backup)
