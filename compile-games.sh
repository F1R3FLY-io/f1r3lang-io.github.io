#!/bin/bash
# compile-games.sh — Pre-compile JSX to plain JS, remove Babel standalone dependency
# This fixes blank pages on iOS Safari caused by runtime Babel transpilation
# Run from: /Users/hannahadams/git-repos/f1r3fly-review/

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
GAMES=("f1r3pix" "f1r3beat-panels" "f1r3ink" "f1r3skein" "f1r3sidechat")
NPX="/opt/homebrew/bin/npx"

echo "=== F1R3Games JSX Compiler ==="
echo "Removing Babel standalone dependency from all games"
echo ""

for game in "${GAMES[@]}"; do
  HTML="$REPO_DIR/$game/index.html"
  if [ ! -f "$HTML" ]; then
    echo "SKIP: $HTML not found"
    continue
  fi

  echo "--- $game ---"

  # Back up original
  cp "$HTML" "$HTML.babel-backup"

  # Extract the JSX block (everything between <script type="text/babel"> and </script>)
  python3 -c "
import re, sys
with open('$HTML', 'r') as f:
    html = f.read()
m = re.search(r'<script\s+type=\"text/babel\">(.*?)</script>', html, re.DOTALL)
if not m:
    print('ERROR: No babel script found')
    sys.exit(1)
with open('$HTML.jsx', 'w') as f:
    f.write(m.group(1))
print(f'  Extracted {len(m.group(1))} chars of JSX')
"

  # Compile JSX to plain JS using Babel
  /opt/homebrew/bin/babel --presets @babel/preset-react "$HTML.jsx" -o "$HTML.compiled.js" 2>&1
  echo "  Compiled to $(wc -c < "$HTML.compiled.js" | tr -d ' ') bytes"

  # Reassemble: remove babel-standalone script tag, replace script type="text/babel" with compiled JS
  python3 -c "
import re
with open('$HTML', 'r') as f:
    html = f.read()
# Remove babel-standalone script
html = re.sub(r'<script\s+src=\"https://cdnjs\.cloudflare\.com/ajax/libs/babel-standalone/[^\"]*\">\s*</script>\n?', '', html)
# Replace <script type=\"text/babel\">...</script> with <script>compiled</script>
with open('$HTML.compiled.js', 'r') as f:
    compiled = f.read()
pattern = r'<script\s+type=\"text/babel\">.*?</script>'
html = re.sub(pattern, '<script>\n' + compiled.replace('\\\\', '\\\\\\\\') + '</script>', html, flags=re.DOTALL)
with open('$HTML', 'w') as f:
    f.write(html)
print(f'  Written {len(html)} chars')
"

  # Clean up temp files
  rm -f "$HTML.jsx" "$HTML.compiled.js"

  # Verify
  babel_count=$(grep -c 'babel' "$HTML" 2>/dev/null || echo 0)
  createElement_count=$(grep -c 'React.createElement' "$HTML" 2>/dev/null || echo 0)
  echo "  Babel references: $babel_count (should be 0)"
  echo "  React.createElement calls: $createElement_count (should be >0)"
  echo "  Backup: $HTML.babel-backup"
  echo ""
done

echo "=== Done. Test on iPhone Safari, then push: ==="
echo "cd $REPO_DIR"
echo "git add -A && git commit -m 'Pre-compile JSX: remove Babel standalone for iOS Safari compatibility' && git push"
