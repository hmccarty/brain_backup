export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export DATABASE_URI=./mydb.db

flask add-post ./brainbank/static/journal/2020-06-30-FirstPost.md