#!/usr/bin/env bash

set -euo pipefail

# Template defaults (AppNEra should replace these when generating an app)
APP_NAME="WebApp"
APP_ID="webapp"

APP_DIR="$HOME/.local/$APP_NAME"
APP_DESKTOP_DIR="$HOME/.local/share/applications"
APP_ICON_DIR="$HOME/.local/share/icons"

echo "Uninstalling '$APP_NAME' from $APP_DIR"

rm -f "$APP_DESKTOP_DIR/$APP_ID.desktop" || true
rm -f "$APP_ICON_DIR/$APP_ID.png" || true

rm -rf "$APP_DIR"

echo "Uninstallation complete."