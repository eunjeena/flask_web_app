from flask import Flask, render_template, url_for
app = Flask(__name__)

posts=[
    {
        'author': 'gina na',
        'title':'Blog post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'koji okayasu',
        'title':'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home") #multi urls work same
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')
# to avoid these env settings:
# export FLASK_APP=<this file name>
# export FLASK_DEBUG=1
if __name__ == '__main__':
    app.run(debug=True)
