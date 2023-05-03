import platform

from application import app

if __name__ == "__main__":
    if platform.system() == "Darwin":
        # enable debug mode if it's mac
        app.debug = True
        app.run()
    else:
        app.debug = False
        app.run()
