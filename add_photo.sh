export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export DATABASE_URI=./mydb.db

python3 -m flask add-photo mario ./brainbank/static/gallery/1.png