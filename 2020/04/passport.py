import unittest

class Passport:
    def __init__(self, f):
        self.f = {}
        for e in f:
            (k, v) = e.split(':')
            self.f[k] = v

    def valid(self):
        for f in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']:
            if f not in self.f:
                return False
        return True

    def correct(self):
        if not self.valid():
            return False

        byr = self.f['byr']
        for c in byr:
            if c not in '0123456789':
                return False
        if int(byr) < 1920 or int(byr) > 2002:
            return False

        iyr = self.f['iyr']
        for c in iyr:
            if c not in '0123456789':
                return False
        if int(iyr) < 2010 or int(iyr) > 2020:
            return False

        eyr = self.f['eyr']
        for c in eyr:
            if c not in '0123456789':
                return False
        if int(eyr) < 2020 or int(eyr) > 2030:
            return False

        hgt = self.f['hgt']
        hgtd = hgt[-2:]
        if hgtd not in ['cm', 'in']:
            return False
        hgt = hgt[:-2]
        try:
            hgt2 = str(int(hgt))
            if hgt2 != hgt:
                return False
        except:
            return False
        hgtv = int(hgt)
        if hgtd == 'cm':
            if hgtv < 150 or hgtv > 193:
                return False
        if hgtd == 'in':
            if hgtv < 59 or hgtv > 76:
                return False

        hcl = self.f['hcl']
        if hcl[0] != '#':
            return False
        if len(hcl) != 7:
            return False
        for c in hcl[1:]:
            if c not in '0123456789abcdef':
                return False

        ecl = self.f['ecl']
        if ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return False

        pid = self.f['pid']
        if len(pid) != 9:
            return False
        for c in pid:
            if c not in '0123456789':
                return False

        return True


class TestPassport(unittest.TestCase):
    def test_valid(self):
        p = Passport(['ecl:gry', 'pid:860033327', 'eyr:2020', 'hcl:#fffffd', 'byr:1937', 'iyr:2017', 'cid:147', 'hgt:183cm'])
        self.assertTrue(p.valid())
        p = Passport(['iyr:2013', 'ecl:amb', 'cid:350', 'eyr:2023', 'pid:028048884', 'hcl:#cfa07d', 'byr:1929'])
        self.assertFalse(p.valid())
        p = Passport(['hcl:#ae17e1', 'iyr:2013', 'eyr:2024', 'ecl:brn', 'pid:760753108', 'byr:1931', 'hgt:179cm'])
        self.assertTrue(p.valid())
        p = Passport(['hcl:#cfa07d', 'eyr:2025', 'pid:166559648', 'iyr:2011', 'ecl:brn', 'hgt:59in'])
        self.assertFalse(p.valid())

    def test_correct(self):
        inc = [
            'eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926',
            'iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946',
            'hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277',
            'hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007',
        ]
        for s in inc:
            p = Passport(s.split(' '))
            self.assertFalse(p.correct())

        cor = [
            'pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f',
            'eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm',
            'hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022',
            'iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719',
        ]
        for s in cor:
            p = Passport(s.split(' '))
            self.assertTrue(p.correct())


#unittest.main()

l = []
while True:
    c = ''
    try:
        while True:
            s = input()
            if s == '':
                break
            c += ' ' + s
    except:
        break
    finally:
        l.append(c[1:])

ans = 0
for x in l:
    p = Passport(x.split(' '))
    if p.correct():
        ans += 1
print(ans)
