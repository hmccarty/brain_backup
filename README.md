# Brain Bank
The human brain is somewhat fragile, so I figured I might as well upload
relevant information to the cloud. In the event that I am dead, please use
this site to restore to a latest, working version.

## Testing
You first need to set a few environment variables:
```bash
export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export DATABASE_URI=./mydb.db
```

To run locally:
```bash
python3 -m flask run
```
