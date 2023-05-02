from sys import argv
from parse import findall
from parse import search
import os
import re

os.system('color')
run_sec_bias = 530
run_size = 88  # bytes

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



def bytes_to_int32(file_content, bias):
    result = 0
    for i in range(bias + 3, bias - 1, -1):
        result = result * 256 + file_content[i]
    return result


def bytes_to_int16(file_content, bias):
    return 256 * file_content[bias + 1] + file_content[bias]


def frames_done(file_content, run_n):
    return bytes_to_int32(file_content, run_sec_bias + run_size * (run_n - 1) + 74)


def frames_in_run(file_content, run_n):
    return bytes_to_int32(file_content, run_sec_bias + run_size * (run_n - 1) + 70)


class RunFile:
    _filename = ''
    _fileContent = []
    _run_number = 0

    def __init__(self, in_filename):
        self._filename = in_filename
        # print(filename)
        with open(self._filename, mode='rb') as file:  # b is important -> binary
            self._fileContent = bytearray(file.read())
        self._run_number = self._find_run_number()  # number of runs

    def _find_run_number(self):
        k = 0
        current_run_n = bytes_to_int16(self._fileContent, run_sec_bias + run_size * k + 86)
        while current_run_n != 0:
            k = k + 1
            current_run_n = bytes_to_int16(self._fileContent, run_sec_bias + run_size * k + 86)
        return k + 1

    def get_run_number(self):
        return self._run_number

    def get_frames_in_run(self, run_n):
        if run_n > self._run_number:
            return -1
        return frames_in_run(self._fileContent, run_n)

    def get_frames_done(self, run_n):
        if run_n > self._run_number:
            return -1
        return frames_done(self._fileContent, run_n)

    def set_frames_done(self, run_n, frames):
        if run_n > self._run_number:
            print(make_color('Wrong run_n in set_frames_done', 'red'))
            return
        if frames > self.get_frames_in_run(run_n):
            print(make_color('Wrong frame_n in set_frames_done', 'red'))
            return
        bias = run_sec_bias + run_size * (run_n - 1) + 74
        self._int32_to_bytes(bias, frames)

    def _int32_to_bytes(self, bias, value):
        self._fileContent[bias + 3] = value // (256 * 256 * 256)
        value = value % (256 * 256 * 256)
        self._fileContent[bias + 2] = value // (256 * 256)
        value = value % (256 * 256)
        self._fileContent[bias + 1] = value // 256
        value = value % 256
        self._fileContent[bias + 0] = value

    def restore(self):
        for run_n in range(1, self._run_number + 1):
            self.set_frames_done(run_n, self.get_frames_in_run(run_n))

    def select_only(self, run_2_set):
        for run_n in range(1, self._run_number + 1):
            if run_n == run_2_set:
                self.set_frames_done(run_n, self.get_frames_in_run(run_n))
            else:
                self.set_frames_done(run_n, 0)

    def select_list(self, in_list):
        for run_n in range(1, self._run_number + 1):
            self.set_frames_done(run_n, 0)
        for run_n in in_list:
            self.set_frames_done(run_n, self.get_frames_in_run(run_n))

    def print(self):
        s = ''
        width = 8
        for k in range(1, self.get_run_number() + 1):
            new_part = '{:03d}|'.format(k) +\
                '{:03d}/{:03d} '.format(self.get_frames_done(k), self.get_frames_in_run(k))
            if self.get_frames_done(k) > 0:
                new_part = make_color(new_part, 'yellow')
            s = s + new_part
            if (k-1) % width == (width-1):
                print(s)
                s = ''
        print(s)
        # print('')

    def save_file(self):
        with open(self._filename, mode='wb') as file:  # b is important -> binary
            file.write(self._fileContent)
            print(make_color('File updated!', 'green'))


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
