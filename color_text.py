import os
os.system('color')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


def make_color(string, color):
    if color == 'none':
        string = bcolors.ENDC + string + bcolors.ENDC
    elif color == 'yellow':
        string = bcolors.WARNING + string + bcolors.ENDC
    elif color == 'pink':
        string = bcolors.HEADER + string + bcolors.ENDC
    elif color == 'blue':
        string = bcolors.OKBLUE + string + bcolors.ENDC
    elif color == 'cyan':
        string = bcolors.OKCYAN + string + bcolors.ENDC
    elif color == 'green':
        string = bcolors.OKGREEN + string + bcolors.ENDC
    elif color == 'red':
        string = bcolors.FAIL + string + bcolors.ENDC
    elif color == '6':
        string = bcolors.BOLD + string + bcolors.ENDC
    elif color == 'underline':
        string = bcolors.UNDERLINE + string + bcolors.ENDC
    return string


def printc(args):
    # print(bcolors.WARNING)
    # print(args)
    # print(bcolors.ENDC)
    # print(bcolors.WARNING + args + bcolors.ENDC)
    print(bcolors.WARNING + args + bcolors.ENDC)


