#!/bin/bash

# Build Vue.js frontend
echo "Building Vue.js frontend..."
cd frontend
npm install
npm run build
cd ..

# Create directories
echo "Setting up directories..."
mkdir -p static
mkdir -p api/templates

# Copy frontend build files to static directory
echo "Copying frontend build files to static directory..."
cp -r frontend/dist/* static/

# Create a proper Django template
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

echo "Build completed successfully!" 