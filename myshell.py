# Provided by Nicolas Zimmermann, ID:18103286

import sys
import os
import Commands
import Env


class MyShell:
    # Initialization of members variables
    def __init__(self):
        self.commands = {
            "cd": Commands.cd,
            "clr": Commands.clr,
            "dir": Commands.dir,
            "environ": Commands.environ,
            "echo": Commands.echo,
            "display": Commands.echo,
            "help": Commands.displayHelp,
            "pause": Commands.pause,
            "quit": Commands.quitShell,
        }
        self.env = Env.Env(os.path.abspath(os.path.dirname(sys.argv[0])))

    # Print my prompt, which is the actual path followed by " > "
    @staticmethod
    def printPrompt():
        print(os.getcwd() + " > ", end="", flush=True)

    # Parse line before processing
    def parseLine(self, line):
        lineArgs = line.replace('\t', ' ').split()
        if lineArgs:
            cmd = lineArgs[0]
            if len(lineArgs) >= 2:
                args = lineArgs[1:]
            else:
                args = []
            return self.process(cmd, args)

    # Manage redirection just before processing commands
    @staticmethod
    def manageRedirection(args):
        if ">>" in args:
            try:
                index = args.index(">>")
                fileName = args[index + 1]
                args = args[:-2]
                sys.stdout = open(fileName, "a+")
            except IOError:
                sys.stderr.write("File: {} cannot be created.".format(fileName))
        elif ">" in args:
            try:
                index = args.index(">")
                fileName = args[index + 1]
                args = args[:-2]
                sys.stdout = open(fileName, "w+")
            except IOError:
                sys.stderr.write("File: {} cannot be created.".format(fileName))

    # Process the commands
    def process(self, cmd, args):
        self.manageRedirection(args)
        if cmd in self.commands:
            return self.commands[cmd](args, self.env)
        else:
            return Commands.execute(cmd, args)


    # Main loop when the shell is executed with a file as argument
    def execFile(self, fileName):
        b = True
        try:
            file = open(fileName, "r")
            for line in file.readlines():
                self.parseLine(line)
        except IOError:
            b = False
            sys.stderr.write("File: {} not found.".format(fileName))
        finally:
            if b:
                file.close()

    # Main loop for normal user usage
    def mainLoop(self):
        self.printPrompt()
        for line in sys.stdin:
            defaultOut = sys.stdout
            b = self.parseLine(line)
            sys.stdout = defaultOut
            if not b:
                return
            else:
                self.printPrompt()


# Launch the shell
shell = MyShell()
if len(sys.argv) > 1:
    shell.execFile(sys.argv[1])
else:
    shell.mainLoop()
