#!/usr/bin/env python3
"""
Adds a “WELCOME TO SPOT-ON!” banner (fades out after 5 s) to guide.html.
• If #welcome-banner already exists, does nothing.
• Writes guide.html.YYYYMMDD-HHMMSS.bak before modifying the file.
Requires: beautifulsoup4 (auto-installed by Vercel via requirements.txt).
"""

import sys, pathlib, datetime as dt
from bs4 import BeautifulSoup

HTML_FILE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("guide.html")

BANNER_HTML = """
<div id="welcome-banner" style="
 background:linear-gradient(135deg,#ff8a00,#e52e71);
 color:#fff;font-family:system-ui,sans-serif;text-align:center;
 font-size:clamp(2rem,5vw,4rem);padding:2.5rem 1rem;margin:0;
 opacity:1;transition:opacity 1s ease-in-out;">
  🎶 WELCOME&nbsp;TO&nbsp;SPOT-ON! 🌍
</div>
<script id="welcome-banner-script">
 (()=>{const b=document.getElementById('welcome-banner');
       if(!b) return;
       setTimeout(()=>{b.style.opacity='0';
         b.addEventListener('transitionend',()=>b.remove());
       },5000);
 })();
</script>
"""

# ----------------------------------------------------------------------------------
if not HTML_FILE.exists():
    sys.exit(f"✖ {HTML_FILE} not found")

html = HTML_FILE.read_text("utf-8")
if 'id="welcome-banner"' in html:
    print("✔ Banner already present – nothing to do."); sys.exit(0)

# backup
stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
backup = HTML_FILE.with_suffix(HTML_FILE.suffix + f".{stamp}.bak")
backup.write_text(html); print(f"🗄  Backup saved → {backup}")

# inject right after the opening <body> tag
lower = html.lower()
body_pos = lower.find("<body")
if body_pos == -1: sys.exit("✖ <body> tag not found")
body_end = html.find(">", body_pos)
new_html = html[:body_end+1] + BANNER_HTML + html[body_end+1:]
HTML_FILE.write_text(new_html); print(f"✅ Banner injected into {HTML_FILE}")
