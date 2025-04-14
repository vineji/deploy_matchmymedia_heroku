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

## Final Steps to Fix Static Files

1. Disable automatic static file collection on Heroku:
```
heroku config:set DISABLE_COLLECTSTATIC=1
```

2. Set DEBUG to true temporarily:
```
heroku config:set DEBUG=True
```

3. Rebuild your frontend with the updated configuration:
```
./build.sh
```

4. Add the new files and commit:
```
git add static/ api/templates/ frontend/vue.config.js -f
git commit -m "Update static files with non-hashed filenames and move template to api/templates/"
```

5. Push to Heroku:
```
git push heroku main
```

6. Manually collect static files:
```
heroku run python manage.py collectstatic --no-input
```

7. Restart your app:
```
heroku restart
```

8. Open your app:
```
heroku open
```

9. Once everything is working, set DEBUG back to false:
```
heroku config:set DEBUG=False
```

## Troubleshooting

### View logs
```
heroku logs --tail
```

### Check static files
```
heroku run ls staticfiles/
heroku run ls staticfiles/js/
heroku run ls staticfiles/css/
```

### Run a shell on Heroku
```
heroku run bash
```
Then you can explore the file system.

### Restart the app
```
heroku restart
``` 