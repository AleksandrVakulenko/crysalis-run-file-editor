from run_file_parser import RunFile
from color_text import make_color
from sys import argv
from parse import findall
from parse import search
import os
import re


def clear_cmd():
    os.system('cls' if os.name == 'nt' else 'clear')


def cmd_parser(cmd):
    if (cmd == 'restore') | (cmd == 're') | (cmd == 'r'):
        return 'restore',
    if (cmd == 'exit') | (cmd == 'e') | (cmd == 'quit') | (cmd == 'q'):
        return 'exit',
    if (cmd == 'print') | (cmd == 'p') | (cmd == 'pr'):
        return 'print',
    if (cmd == 'help') | (cmd == 'h'):
        return 'help',
    if (cmd == 'clc') | (cmd == 'clear'):
        return 'clc',
    if (cmd.find('set ') != -1) & (cmd.find('.') == -1) & (cmd.find(',') == -1):
        set_list = []
        for r in findall('{:d}', cmd):
            set_list.append(r[0])
        return 'set', set_list
    print(make_color('cmd ignored', 'red'))


help_msg = '\n' \
           'restore | re | r     : restore full file\n' \
           'exit | e | quit | q  : exit program\n' \
           'print | p | pr       : print file state\n' \
           'help | h             : help message\n' \
           'clear | clc          : clear screen\n' \
           'set %i %i ...%i      : set selected runs\n'


def try_to_find_run_file():
    list_of_files = os.listdir('./')
    valid_names = []
    for name in list_of_files:
        if re.search('.*.run', name) is not None:
            valid_names.append(name)
    if len(valid_names) > 1:
        print(make_color('More than one *.run file in this folder:', 'red'))
        print(valid_names)
        return ''
    if len(valid_names) == 0:
        print(make_color('No one *.run file found', 'red'))
        return ''
    return valid_names[0]


# filename = 'run_files/3_166_out.run'


try:
    filename = argv[1]
except IndexError:
    print(make_color('Non argument provided, trying to find *.run file in \\.', 'yellow'))
    filename = try_to_find_run_file()
    if filename == '':
        print('exit\n')
        exit(-1)
    else:
        print(make_color('File found: ', 'yellow'), end='')
        print(filename)

rf = RunFile(filename)


print(make_color('File loaded', 'cyan'))


parsed_cmd = '',
while parsed_cmd[0] != 'exit':
    parsed_cmd = cmd_parser(input('>>'))
    if not parsed_cmd:
        parsed_cmd = 'none',
    if parsed_cmd[0] == 'exit':
        break
    if parsed_cmd[0] == 'restore':
        rf.restore()
        rf.save_file()
    if parsed_cmd[0] == 'print':
        rf.print()
    if parsed_cmd[0] == 'set':
        rf.select_list(parsed_cmd[1])
        rf.save_file()
    if parsed_cmd[0] == 'clc':
        clear_cmd()
    if parsed_cmd[0] == 'help':
        print(help_msg)

# print(make_color('Wrong argument:', 'red'), cmd)

print('EXIT')
