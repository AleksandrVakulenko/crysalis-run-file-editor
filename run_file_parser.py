from color_text import printc
from color_text import make_color

run_sec_bias = 530
run_size = 88  # bytes


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
            print('Wrong run_n in set_frames_done')
            return
        if frames > self.get_frames_in_run(run_n):
            print('Wrong frame_n in set_frames_done')
            return
        bias = run_sec_bias + run_size * (run_n - 1) + 74
        self._int32_to_bytes(bias, frames)

    def _int32_to_bytes(self, bias, value):
        self._fileContent[bias + 3] = value // (256 * 256 * 256)
        value = value % (256 * 256 * 256)
        self._fileContent[bias + 2] = value // (256 * 256)
        value = value % (256 * 256)
        self._fileContent[bias + 1] = value // (256)
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


