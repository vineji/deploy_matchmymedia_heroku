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
mkdir -p templates

# Copy frontend build files to static directory
echo "Copying frontend build files to static directory..."
cp -r frontend/dist/* static/

# Copy index.html to templates directory 
echo "Copying index.html to templates directory..."
cp frontend/dist/index.html templates/

echo "Build completed successfully!" 