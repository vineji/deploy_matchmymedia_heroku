# Heroku Deployment Instructions for MatchMyMedia

## 1. Install Heroku CLI
If you haven't already:
```
brew install heroku/brew/heroku
```

## 2. Login to Heroku
```
heroku login
```

## 3. Create a new Heroku app
```
heroku create matchmymedia
```

## 4. Add buildpack
```
heroku buildpacks:set heroku/python
```

## 5. Configure environment variables
```
heroku config:set SECRET_KEY='your-secret-key-here'
heroku config:set DEBUG=False
heroku config:set GOOGLE_BOOKS_API_KEY='your-google-books-api-key'
heroku config:set TMBD_API_KEY='your-tmdb-api-key'
```

## 6. Add Redis add-on
```
heroku addons:create heroku-redis:mini
```

## 7. Build the frontend locally
Make sure you've built the Vue.js frontend first:
```
chmod +x build.sh
./build.sh
```

## 8. Make the post_compile script executable
```
chmod +x bin/post_compile
```

## 9. Commit the built static files
The build.sh script created static files that need to be committed:
```
git add static/ templates/ -f
git commit -m "Add built frontend files"
```

## 10. Deploy to Heroku
```
git push heroku main
```
Note: If your branch is not 'main', use: `git push heroku your-branch-name:main`

If you're having issues with the Apple Git version, try:
```
/usr/local/bin/git push heroku main
```

## 11. Run migrations
```
heroku run python manage.py migrate
```

## 12. Create superuser (optional)
```
heroku run python manage.py createsuperuser
```

## 13. Open your application
```
heroku open
```

## Troubleshooting

### Rebuild and redeploy frontend
If your frontend still doesn't display correctly:
```
# Run the build script again
./build.sh

# Commit and push the changes
git add static/ templates/ -f
git commit -m "Rebuild frontend"
git push heroku main
```

### View logs
```
heroku logs --tail
```

### Check static files
```
heroku run ls -la staticfiles/
```

### Restart the app
```
heroku restart
``` 