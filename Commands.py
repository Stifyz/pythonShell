# Provided by Nicolas Zimmermann, ID:18103286

import os
import sys


# Execute cmd with the arguments in args. Manage the background execution
def execute(cmd, args):
    childPid = os.fork()
    b = True
    if len(args) > 0 and args[-1] == "&":
        b = False
        args = args[-1:]
    if childPid == 0:
        os.system(cmd + ' ' + ' '.join(args))
    elif b:
        os.wait()
    return True


# Move to directory args[0]
def cd(args, env):
    path = os.getcwd()
    if not args:
        print(path)
    else:
        directory = args[0]
        try:
            os.chdir(directory)
        except OSError:
            sys.stderr.write("Cannot found directory {} from path {}.\n".format(directory, path))
        finally:
            env.setEnv("PWD", os.getcwd())
    return True


# Clear the screen
def clr(args, env):
    print("\033c", end="")
    return True


# List the files in the given directory
def dir(args, env):
    if not args:
        directory = "."
    else:
        directory = args[0]
    if os.path.isdir(directory):
        print(*os.listdir(directory), sep="\n")
    else:
        sys.stderr.write("{} is not a valid directory.\n".format(directory))
    return True


# List the environment strings separated by new-lines
def environ(args, env):
    if not args:
        print(*env.getEnvFull(), sep="\n")
    else:
        print(env.getEnv(args[0]))
    return True


# Display the words in args separated by spaces
def echo(args, env):
    print(*args, sep=' ')
    return True


# Display the readme file
def displayHelp(args, env):
    path = env.getEnv("SHELL")[:-len("myshell.py")]
    childPid = os.fork()
    if childPid == 0:
        os.system("cat " +  path + "readme | more")
    else:
        os.wait()
    return True


# Pause the shell, until the user press enter
def pause(args, env):
    input()
    return True


# Exit the shell properly
def quitShell(args, env):
    print("quit")
    return False
