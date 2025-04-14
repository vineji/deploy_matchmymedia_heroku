#!/bin/bash

echo "=== Preparing files for Heroku deployment ==="

# Build the Vue.js frontend
echo "Building Vue.js frontend..."
cd frontend
npm install
npm run build
cd ..

# Create necessary directories
echo "Creating directories..."
mkdir -p static/css
mkdir -p static/js
mkdir -p api/templates

# Find the actual filenames with hashes
CHUNK_VENDORS_FILE=$(find frontend/dist/js -name "chunk-vendors*.js" | xargs basename)
APP_JS_FILE=$(find frontend/dist/js -name "app*.js" | xargs basename)
APP_CSS_FILE=$(find frontend/dist/css -name "app*.css" | xargs basename)

echo "Found these files:"
echo "- JS: $CHUNK_VENDORS_FILE"
echo "- JS: $APP_JS_FILE"
echo "- CSS: $APP_CSS_FILE"

# Copy index.html to templates with the exact filenames
echo "Creating Django template..."
cat > api/templates/index.html << EOL
{% load static %}
<!doctype html>
<html lang="">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <link rel="icon" href="{% static 'favicon.ico' %}">
        <title>MatchMyMedia</title>
        <script defer="defer" src="{% static 'js/$CHUNK_VENDORS_FILE' %}"></script>
        <script defer="defer" src="{% static 'js/$APP_JS_FILE' %}"></script>
        <link href="{% static 'css/$APP_CSS_FILE' %}" rel="stylesheet">
    </head>
    <body>
        <noscript>
            <strong>We're sorry but MatchMyMedia doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
        </noscript>
        <div id="app"></div>
    </body>
</html>
EOL

# Copy all static assets with original filenames
echo "Copying static assets..."
cp frontend/dist/favicon.ico static/
cp frontend/dist/js/$CHUNK_VENDORS_FILE static/js/
cp frontend/dist/js/$APP_JS_FILE static/js/
cp frontend/dist/css/$APP_CSS_FILE static/css/

# For debugging purposes, create a list of copied files
ls -la static/js/ > static/copied-files.txt
ls -la static/css/ >> static/copied-files.txt

echo "Done! Now commit these files and deploy to Heroku."
echo "git add api/templates/ static/ -f"
echo "git commit -m \"Add built files for Heroku with correct hashed filenames\""
echo "git push heroku main" 