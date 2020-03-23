# app variable should exists in __init__.py of that package
from flaskblog import create_app

app = create_app()

# to avoid these env settings:
# export FLASK_APP=<this file name>
# export FLASK_DEBUG=1
if __name__ == '__main__':
    app.run(debug=True)
