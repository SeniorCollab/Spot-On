from pathlib import Path

html_path = Path("index.html")
src = html_path.read_text(encoding="utf-8")

# Skip if already present
if "BEGIN welcome-overlay" in src:
    print("Overlay already injected ✔")
    raise SystemExit

snippet = """
<!-- BEGIN welcome-overlay -->
<style>
  #welcome-overlay {position:fixed;inset:0;background:rgba(0,0,0,.88);color:#fff;
  font-family:sans-serif;font-size:3rem;display:flex;align-items:center;
  justify-content:center;text-align:center;z-index:9999;}
</style>
<div id="welcome-overlay" aria-live="polite">Welcome&nbsp;to&nbsp;Pinfinity</div>
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script>
  $(function () {
    setTimeout(() => {
      $("#welcome-overlay").fadeOut(600, function () { $(this).remove(); });
    }, 5000);
  });
</script>
<!-- END welcome-overlay -->
"""

marker_lower = src.lower().rfind("</body>")
new_src = (
    src[:marker_lower] + snippet + src[marker_lower:]
    if marker_lower != -1
    else src + snippet
)

html_path.write_text(new_src, encoding="utf-8")
print("✅ 5-second welcome overlay injected into index.html")
