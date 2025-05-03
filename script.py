#!/usr/bin/env python3
"""
inject_welcome_banner.py
—————————
Adds a full-width “WELCOME TO SPOT-ON!” banner that fades away after 5 s.

• Makes timestamped backup of index.html
• Skips if #welcome-banner already exists
• Injects one inline <script id="welcome-banner-script"> to handle fade-out
"""

import sys, pathlib, datetime as dt
from bs4 import BeautifulSoup

# ---------- configurable bits ------------------------------------------------
INDEX = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("index.html")

BANNER_HTML = """
<div id="welcome-banner" style="
     background:linear-gradient(135deg,#ff8a00,#e52e71);
     color:#fff;font-family:system-ui,sans-serif;text-align:center;
     font-size:clamp(2rem,5vw,4rem);padding:2.5rem 1rem;margin:0;
     opacity:1;transition:opacity 1s ease-in-out;">
  🎶 WELCOME TO SPOT-ON! 🌍
</div>
"""

FADE_SCRIPT = """
<script id="welcome-banner-script">
  (()=>{const b=document.getElementById('welcome-banner');
        if(!b) return;
        setTimeout(()=>{b.style.opacity='0';
          b.addEventListener('transitionend',()=>b.remove());
        },5000);
  })();
</script>
"""
# ---------------------------------------------------------------------------

if not INDEX.exists():
    sys.exit(f"✖ {INDEX} not found")

html = INDEX.read_text("utf-8")
soup = BeautifulSoup(html, "html.parser")

if soup.find(id="welcome-banner"):
    print("✔ Banner already present – nothing to do.")
    sys.exit(0)

# backup
stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
backup = INDEX.with_suffix(INDEX.suffix + f".{stamp}.bak")
backup.write_text(html)
print(f"🗄  Backup saved → {backup}")

# inject banner + script
body = soup.body
if body is None:
    sys.exit("✖ <body> tag not found; aborting.")
body.insert(0, BeautifulSoup(BANNER_HTML, "html.parser"))

# insert script *once* (after banner so DOM element already exists)
if not soup.find(id="welcome-banner-script"):
    body.insert(1, BeautifulSoup(FADE_SCRIPT, "html.parser"))

INDEX.write_text(str(soup))
print(f"✅ Welcome banner with 5-second fade injected into {INDEX}")
