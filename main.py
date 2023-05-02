from run_file_parser import RunFile
from color_text import make_color
from sys import argv

# filename = 'run_files/3_166_out.run'
filename = argv[1]
rf = RunFile(filename)

print(make_color('File loaded', 'cyan'))
cmd = ''
while cmd != 'exit':
    cmd = input('>>')
    if cmd == 'exit':
        break
    if (cmd == 'restore') | (cmd == 're'):
        rf.restore()
        rf.save_file()
    if cmd == 'print':
        rf.print()
    if cmd.find('set ') != -1:
        cmd = cmd[4:len(cmd)]
        try:
            value = int(cmd)
            rf.select_only(int(cmd))
            rf.save_file()
        except ValueError:
            print(make_color('Wrong argument:', 'red'), '<', cmd, '>')


print('EXIT')