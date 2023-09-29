from cmd import Cmd


class Shell(Cmd):
    intro = 'Shell intro\r\n'
    use_rawinput = False
    prompt = 'My Shell> '

    def __init__(self, stdin=None, stdout=None):
        super(Shell, self).__init__(completekey='tab', stdin=stdin, stdout=stdout)

    def print(self, value):
        # make sure stdout is set and not closed
        if self.stdout and not self.stdout.closed:
            self.stdout.write(value)
            self.stdout.flush()

    def printline(self, value):
        self.print(value + '\r\n')

    def emptyline(self):
        self.print('\r\n')

    def do_greet(self, arg):
        if arg:
            self.printline('Hey {0}! Nice to see you!'.format(arg))
        else:
            self.printline('Hello there!')

    def do_bye(self, arg):
        self.printline('See you later!')
        return True
