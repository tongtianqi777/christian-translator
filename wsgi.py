import platform

from app import app

if __name__ == "__main__":
    if platform.system() == "Darwin":
        # enable debug mode if it's mac
        app.debug = True
        app.run(port=8000)
    else:
        app.debug = False
        app.run(host='0.0.0.0', port=8000)
