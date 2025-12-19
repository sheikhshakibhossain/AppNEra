#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# Template defaults (AppNEra should replace these when generating an app)
APP_NAME="WebApp"
APP_ID="webapp"
APP_URL="https://example.com"

APP_DIR="$HOME/.local/$APP_NAME"
APP_DESKTOP_DIR="$HOME/.local/share/applications"
APP_ICON_DIR="$HOME/.local/share/icons"

mkdir -p "$APP_DIR" "$APP_DESKTOP_DIR" "$APP_ICON_DIR"

echo "Installing '$APP_NAME' into $APP_DIR"

# Copy app runtime
cp "$SCRIPT_DIR/app.py" "$APP_DIR/app.py"
cp "$SCRIPT_DIR/icon.png" "$APP_DIR/icon.png"
cp "$SCRIPT_DIR/uninstall.sh" "$APP_DIR/uninstall.sh"
chmod +x "$APP_DIR/uninstall.sh"

# Create isolated virtual environment
python3 -m venv "$APP_DIR/venv"

# Create launcher
cat > "$APP_DIR/run.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail

export APPNERA_APP_NAME="$APP_NAME"
export APPNERA_APP_ID="$APP_ID"
export APPNERA_URL="$APP_URL"

exec "$APP_DIR/venv/bin/python" "$APP_DIR/app.py"
EOF
chmod +x "$APP_DIR/run.sh"

# Create .desktop entry inside the app directory (self-contained)
cat > "$APP_DIR/$APP_ID.desktop" <<EOF
[Desktop Entry]
Name=$APP_NAME
Comment=$APP_NAME
Exec=$APP_DIR/run.sh
Icon=$APP_DIR/icon.png
Terminal=false
Type=Application
Categories=Network;WebBrowser;
EOF

# Link desktop entry + icon into standard user locations
ln -sf "$APP_DIR/$APP_ID.desktop" "$APP_DESKTOP_DIR/$APP_ID.desktop"
ln -sf "$APP_DIR/icon.png" "$APP_ICON_DIR/$APP_ID.png"

echo "Installation complete. Look for '$APP_NAME' in your app launcher."