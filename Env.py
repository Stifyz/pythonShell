# Provided by Nicolas Zimmermann, ID:18103286

import os


class Env:
    def __init__(self, path):
        self.setEnv("SHELL", path + "/myshell.py")

    @staticmethod
    def setEnv(key, value):
        os.environ[key] = value

    @staticmethod
    def getEnv(key):
        if key in os.environ:
            return os.environ[key]
        else:
            return "Environment variable {} not found.".format(key)

    @staticmethod
    def getEnvFull():
        return ('{}={}'.format(key, value) for key, value in os.environ.items())
