import platform

from application import application

if __name__ == "__main__":
    if platform.system() == "Darwin":
        # enable debug mode if it's mac
        application.debug = True
        application.run()
    else:
        application.debug = False
        application.run()
