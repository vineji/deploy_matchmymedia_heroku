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

# Copy index.html to templates with Django template tags
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
        <script defer="defer" src="{% static 'js/chunk-vendors.js' %}"></script>
        <script defer="defer" src="{% static 'js/app.js' %}"></script>
        <link href="{% static 'css/app.css' %}" rel="stylesheet">
    </head>
    <body>
        <noscript>
            <strong>We're sorry but MatchMyMedia doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
        </noscript>
        <div id="app"></div>
    </body>
</html>
EOL

# Copy all static assets
echo "Copying static assets..."
cp frontend/dist/favicon.ico static/
cp frontend/dist/js/chunk-vendors.* static/js/chunk-vendors.js
cp frontend/dist/js/app.* static/js/app.js
cp frontend/dist/css/app.* static/css/app.css

echo "Done! Now commit these files and deploy to Heroku."
echo "git add api/templates/ static/ -f"
echo "git commit -m \"Add built files for Heroku\""
echo "git push heroku main" 