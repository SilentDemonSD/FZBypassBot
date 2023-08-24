if [ -d "/app/.heroku/" ]; then
  python3 -m FZBypass
else
  python3 update.py && python3 -m FZBypass
fi
