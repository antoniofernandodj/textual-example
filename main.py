# main.py
from pathlib import Path
from widgets.postman_app import PostmanApp


if __name__ == "__main__":
    app = PostmanApp(css_path=Path(__file__).parent / 'style.tcss')
    app.run()
