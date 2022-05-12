from flask_frozen import Freezer
from app import setup_app

app = setup_app()

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
