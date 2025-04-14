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

## 7. Make sure bin/post_compile is executable
```
chmod +x bin/post_compile
```

## 8. Deploy to Heroku
```
git add .
git commit -m "Ready for Heroku deployment with lightweight ML"
git push heroku main
```
Note: If your branch is not 'main', use: `git push heroku your-branch-name:main`

If you're having issues with the Apple Git version, try:
```
/usr/local/bin/git push heroku main
```
Or install Git via Homebrew and ensure it's in your PATH:
```
brew install git
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 9. Run migrations
```
heroku run python manage.py migrate
```

## 10. Create superuser (optional)
```
heroku run python manage.py createsuperuser
```

## 11. Open your application
```
heroku open
```

## Troubleshooting

### View logs
```
heroku logs --tail
```

### Check dyno status
```
heroku ps
```

### Restart app if needed
```
heroku restart
```

### Scale dynos if needed
```
heroku ps:scale web=1
``` 