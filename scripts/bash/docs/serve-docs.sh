#!/usr/bin/env bash
# Serve GitHub Pages documentation locally

set -euo pipefail

# Error handler
trap 'echo "✗ Error on line $LINENO. Exit code: $?" >&2' ERR

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "========================================="
echo "  GitHub Pages - Local Server"
echo "========================================="
echo ""

# Check if Ruby is installed
if ! command -v ruby &> /dev/null; then
    echo "❌ Ruby is not installed!"
    echo "Please install Ruby: https://www.ruby-lang.org/en/downloads/"
    exit 1
fi

# Check if Bundler is installed
if ! command -v bundle &> /dev/null; then
    echo "Installing Bundler..."
    gem install bundler
fi

# Install dependencies
echo "Installing Jekyll dependencies..."
bundle install

# Serve the site
echo ""
echo "Starting Jekyll server..."
echo "Site will be available at: http://localhost:4000"
echo "Press Ctrl+C to stop the server"
echo ""

bundle exec jekyll serve --host 0.0.0.0 --port 4000 --livereload
