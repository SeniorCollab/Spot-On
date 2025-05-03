
from pathlib import Path
import sys
import textwrap


SNIPPET = textwrap.dedent("""\
    <!-- BEGIN welcome-overlay -->
    <style>
      #welcome-overlay{position:fixed;inset:0;background:rgba(0,0,0,.88);color:#fff;
        display:flex;align-items:center;justify-content:center;text-align:center;
        font-family:sans-serif;font-size:3rem;z-index:9999;transition:opacity .6s;}
    </style>
    <div id="welcome-overlay">Welcome&nbsp;to&nbsp;Pinfinity</div>
    <script>
      document.addEventListener('DOMContentLoaded',function(){
        setTimeout(function(){
          var el=document.getElementById('welcome-overlay');
          el.style.opacity='0';
          setTimeout(function(){el.remove();},600);
        },5000);
      });
    </script>
    <!-- END welcome-overlay -->
""")

# ----------------------------------------------------------------------
# 2. Locate the file we need to patch
# ----------------------------------------------------------------------
CANDIDATES = [
    Path("index.html"),
]

target = next((p for p in CANDIDATES if p.exists()), None)
if not target:
    sys.exit(
        "❌  No index.html or pages/_document.js found -- nothing to patch.\n"
        "    Add your HTML entry point first or tweak the CANDIDATES list."
    )

text = target.read_text(encoding="utf-8")
if "BEGIN welcome-overlay" in text:
    print("✅  Overlay already present – nothing to do.")
    sys.exit(0)


lower = text.lower()

def inject_before(body_close_tag: str):
    idx = lower.rfind(body_close_tag)
    if idx == -1:
        return text + "\n" + SNIPPET + "\n"
    return text[:idx] + SNIPPET + text[idx:]

if target.suffix == ".html":
    patched = inject_before("</body>")
else:  # Next.js _document.js
    # crude but effective – find the first "<body" inside the template string
    body_start = lower.find("<body")
    if body_start == -1:
        # create a very small _document.js wrapper if user didn’t have one
        patched = text + textwrap.dedent(f"""
            import {{ Html, Head, Main, NextScript }} from 'next/document';
            import {{ Fragment }} from 'react';
            export default function Document() {{
              return (
                <Html>
                  <Head />
                  <body>
                    {SNIPPET}
                    <Main />
                    <NextScript />
                  </body>
                </Html>
              );
            }}
        """)
    else:
        patched = inject_before("</body>")

target.write_text(patched, encoding="utf-8")
print(f"✨  Overlay injected into {target}")
