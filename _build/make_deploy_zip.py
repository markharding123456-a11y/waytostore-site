"""Build the upload package for cPanel. Run from the site root:   python _build/make_deploy_zip.py
Re-stamps the pages, then writes _deploy/waytostore-site-YYYY-MM-DD.zip containing ONLY what belongs in public_html.
Upload the zip to public_html in cPanel File Manager, Extract, delete the zip."""
import datetime
import pathlib
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", ".claude", "_build", "_deploy", "__pycache__"}
EXCLUDE_FILES = {"CLAUDE.md", "SEO-PLAN.md", "profile-text.md", ".gitignore", ".cpanel.yml",
                 "brand-options.html", "options-preview.html", "og-image.svg"}

subprocess.run([sys.executable, str(ROOT / "_build" / "patch_pages.py")], check=True, cwd=ROOT, stdout=subprocess.DEVNULL)

out_dir = ROOT / "_deploy"
out_dir.mkdir(exist_ok=True)
stamp = datetime.date.today().isoformat()
zpath = out_dir / ("waytostore-site-%s.zip" % stamp)
files = []
for p in sorted(ROOT.rglob("*")):
    rel = p.relative_to(ROOT)
    if p.is_dir() or any(part in EXCLUDE_DIRS for part in rel.parts) or rel.name in EXCLUDE_FILES:
        continue
    files.append(rel)

with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for rel in files:
        z.write(ROOT / rel, rel.as_posix())

print("wrote", zpath, "(%d files, %d KB)" % (len(files), zpath.stat().st_size // 1024))
for rel in files:
    print("  ", rel.as_posix())
must = ["index.html", ".htaccess", "styles.css", "robots.txt", "sitemap.xml", "404.html", "favicon.ico",
        "heated-storage-grand-forks.html", "rv-boat-trailer-storage-grand-forks.html", "privacy.html",
        "blog/index.html", "fonts/sora-normal-1.woff2", "og-image.png", "logo.svg"]
missing = [m for m in must if pathlib.PurePosixPath(m) not in [pathlib.PurePosixPath(f.as_posix()) for f in files]]
print("MISSING:" if missing else "all required files present", missing or "")
