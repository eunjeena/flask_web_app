# app variable should exists in __init__.py of that package
from flaskblog import app

# to avoid these env settings:
# export FLASK_APP=<this file name>
# export FLASK_DEBUG=1
if __name__ == '__main__':
    app.run(debug=True)
