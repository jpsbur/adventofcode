import unittest

class Code:
    def __init__(self, lines):
        self.lines = []
        for l in lines:
            x, y = l.split()
            self.lines.append((x, int(y)))

    def detect_loop(self):
        pos = 0
        done = {}
        acc = 0
        while pos not in done:
            if pos == len(self.lines):
                return False, acc
            done[pos] = True
            i, o = self.lines[pos]
            if i == 'nop':
                pos += 1
            elif i == 'acc':
                acc += o
                pos += 1
            elif i == 'jmp':
                pos += o
        return True, acc

    def fix(self):
        for j in range(len(self.lines)):
            i, o = self.lines[j]
            if i == 'jmp':
                self.lines[j] = ('nop', o)
            elif i == 'nop':
                self.lines[j] = ('jmp', o)
            has_loop, acc = self.detect_loop()
            if not has_loop:
                return acc
            self.lines[j] = i, o


class TestCode(unittest.TestCase):
    def test_detect_loop(self):
        c = Code([
            'nop +0',
            'acc +1',
            'jmp +4',
            'acc +3',
            'jmp -3',
            'acc -99',
            'acc +1',
            'jmp -4',
            'acc +6',
        ])
        self.assertEqual(c.detect_loop(), (True, 5))

    def test_fix(self):
        c = Code([
            'nop +0',
            'acc +1',
            'jmp +4',
            'acc +3',
            'jmp -3',
            'acc -99',
            'acc +1',
            'jmp -4',
            'acc +6',
        ])
        self.assertEqual(c.fix(), 8)


#unittest.main()

lines = []
while True:
    try:
        l = input()
    except:
        break
    lines.append(l)
c = Code(lines)
print(c.detect_loop())
print(c.fix())
