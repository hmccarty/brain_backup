import cms

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    post = cms.get()

    return render_template('home.html',
                           posts=[post])

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/quotes')
def quotes():
    return render_template('quotes.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

if __name__ == '__main__':
    app.run()