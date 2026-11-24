from pathlib import Path
import re
import shutil

path = Path("index.html")
original = path.read_text(encoding="utf-8")
html = original

def change(old, new, count=1):
    global html
    found = html.count(old)
    if found != count:
        raise ValueError(
            f"Expected {count}, found {found}: {ascii(old)}"
        )
    html = html.replace(old, new)

def tag(pattern, replacement, count=1):
    global html
    html, found = re.subn(pattern, lambda m: replacement, html)
    if found != count:
        raise ValueError(
            f"Expected {count} matches, found {found}: {pattern}"
        )

# SEO
tag(r"<title>[^<]*</title>",
    "<title>Navira Yoga Studio | Personalized Yoga, Hatha &amp; Pranayama</title>")
tag(r'<meta name="description" content="[^"]*"',
    '<meta name="description" content="Personalized yoga, Hatha Yoga and pranayama at Navira Yoga Studio. Based in Hyderabad, currently offering online sessions across India."')
tag(r'<meta name="keywords" content="[^"]*"',
    '<meta name="keywords" content="personalized yoga, Hatha Yoga, pranayama, online yoga classes India, yoga Hyderabad, mindful movement, Navira Yoga Studio"')

# Hero
change("Heal your body.<br/><em>Transform your life.</em>",
       "Your Body. Your Breath.<br/><em>Your Journey.</em>")
change("Expert-guided therapeutic yoga tailored to your unique health needs. Personalized asana sequences, pranayama, and progressive plans that evolve with your practice.",
       "Discover personalized yoga, Hatha Yoga, pranayama and mindful movement to support flexibility, strength, balance and everyday well-being.")
change("Therapeutic Yoga \u00b7 Hatha \u00b7 Pranayama",
       "Personalized Yoga | Hatha Yoga | Pranayama")
change('<span class="hero-tag">Therapeutic</span>',
       '<span class="hero-tag">Mindful Movement</span>')

# Marquee
change("Online &amp; In-Studio", "Online Sessions Across India", 2)
change("Hatha \u00b7 Pranayama \u00b7 Therapeutic",
       "Hatha | Pranayama | Mindful Movement", 2)

# Statistics
change('<div class="stat-num">10+</div><div class="stat-label">Therapeutic Conditions</div>',
       '<div class="stat-num">India</div><div class="stat-label">Online Class Availability</div>')

# Services
change("Specialized therapeutic programs designed around your health conditions and goals.",
       "Explore yoga practices designed around your experience, interests and personal wellness goals.")
change("Targeted asana sequences with pranayama to boost metabolism, tone the body, and achieve sustainable weight management.",
       "Explore energizing yoga sequences, mindful movement and breathing practices as part of an active lifestyle.")
change("PCOD &amp; PCOS Yoga", "Gentle Yoga &amp; Mindful Movement")
change("Specialized therapeutic sequences to regulate hormones, reduce symptoms, and restore hormonal balance naturally.",
       "Explore gentle movement, mindful breathing and approachable yoga practices suited to your comfort and experience.")
change("Therapeutic \u00b7 Hormonal", "Gentle | Mindful")
change("Back Pain Yoga", "Flexibility &amp; Mobility")
change("Evidence-based asanas for cervical, lumbar, and spinal conditions. Safe sequences with contraindication awareness.",
       "Build a yoga practice focused on comfortable movement, flexibility, posture and body awareness.")
change("Safe \u00b7 Therapeutic", "Movement | Flexibility")
change("Calming pranayama, restorative poses, and mindfulness practices to reduce anxiety, depression, and mental fatigue.",
       "Explore calming breathing exercises, gentle yoga and mindfulness practices to encourage relaxation and everyday balance.")

# Philosophy
change("Most studios teach a fixed sequence. We start from your body: your conditions, your injuries, your goals",
       "Yoga is not one-size-fits-all. We begin with your experience, comfort and personal goals")
change("One-on-one health profiling before you begin",
       "A personal introduction before you begin")
change("Hybrid support \u2014 online, in-studio, or both",
       "Currently offering online sessions across India")

# How it works
change("From registration to your personalized practice \u2014 simple, smart, and therapeutic.",
       "From registration to your personalized yoga practice - simple and supportive.")
change("Register &amp; share your health",
       "Register &amp; share your goals")
change("Fill our detailed health profiling form \u2014 conditions, injuries, goals, lifestyle. Takes 10 minutes. Completely private.",
       "Complete the registration form and share your yoga experience, preferences and wellness goals.")
change("Your instructor carefully designs a personalized asana sequence \u2014 safe for your conditions, aligned with your goals.",
       "Your instructor prepares a yoga practice suited to your experience, comfort and goals.")

# Wellness goals
change("We Specialize In", "Explore Your Practice")
change("Therapeutic conditions", "Your wellness goals")
change("Safe, evidence-informed yoga for a wide range of health conditions.",
       "Discover different ways yoga can support your everyday wellness journey.")

labels = {
    "PCOS / PCOD": "Gentle Movement",
    "Weight Loss": "Active Lifestyle",
    "Back Pain": "Mobility",
    "Stress &amp; Anxiety": "Relaxation",
    "Diabetes": "Everyday Wellness",
    "High BP": "Mindful Breathing"
}
for old, new in labels.items():
    change(f'<span class="dot"></span><span>{old}</span>',
           f'<span class="dot"></span><span>{new}</span>')

# FAQ
change("Can I switch between online and in-studio sessions?",
       "Are classes currently available online?")
change('<button class="faq-q" onclick="toggleFaq(this)">Are classes currently available online?</button>',
       '<button class="faq-q" onclick="toggleFaq(this)">Are classes currently available online? <span class="plus"></span></button>\n'
       '      <div class="faq-a"><p>Yes. Navira Yoga Studio currently offers online yoga sessions across India. In-person classes are not available at this time.</p></div>')
change("Is this suitable for managing conditions like PCOS or back pain?",
       "What if I have a health concern?")
change("Yes \u2014 our therapeutic sequences are designed with contraindication awareness for conditions like PCOS/PCOD, back pain, thyroid issues, and more, always with your specific case in mind.",
       "Please tell your instructor about any relevant health concerns before beginning. Yoga is not a substitute for medical care, so seek guidance from a qualified healthcare professional when appropriate.")

# CTA
change("Ready to begin your<br/><em>healing journey?</em>",
       "Ready to begin your<br/><em>yoga journey?</em>")
change("Join Navira Yoga Studio and experience the power of personalized therapeutic yoga. First consultation is free!",
       "Begin your yoga journey with Navira Yoga Studio. Explore personalized practice, mindful movement and pranayama. First consultation is free!")

# Footer
change("Guntur, Andhra Pradesh, India",
       "Hyderabad, Telangana, India")
change("<h2>Studio Hours</h2>", "<h2>Session Hours</h2>")

# Final validation
for term in ["therapeutic", "Guntur", "Andhra Pradesh", "in-studio"]:
    if term.lower() in html.lower():
        raise ValueError(f"Outdated text remains: {term}")

backup = Path("index.before-remaining-updates.html")
if backup.exists():
    raise ValueError("Backup already exists; no changes saved.")

shutil.copy2(path, backup)
path.write_text(html, encoding="utf-8")

print("SUCCESS: Website content updated.")
print("Backup:", backup)
