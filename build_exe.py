from setup_main import run as packageCli
import os


def run():
    packageCli()
    os.system("pyinstaller -F build_pyd/server.py")


if __name__ == "__main__":
    run()
