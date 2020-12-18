import re

def main():
        with open('4.dat', 'r') as file:
                count = 0
                passport = dict()
                for line in file:
                        line = line.strip()
                        if len(line) == 0:
                                if is_valid_passport(passport):
                                        count += 1
                                passport = dict()
                        else:
                                parts = line.split()
                                for part in parts:
                                        pair = part.split(':')
                                        passport[pair[0]] = pair[1]
                        


                if is_valid_passport(passport):
                        count += 1
                return count

def is_valid_passport(passport):
        required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
        for field in required_fields:
                if field not in passport:
                        print(len(passport))
                        return False

        if not check_year(passport['byr'], 1920, 2002):
                return False
        if not check_year(passport['iyr'], 2010, 2020):
                return False
        if not check_year(passport['eyr'], 2020, 2030):
                return False
        if not check_height(passport['hgt']):
                return False
        if not check_hair_color(passport['hcl']):
                return False
        if not check_eye_color(passport['ecl']):
                return False
        if not check_passport_id(passport['pid']):
                return False
        return True
        
def check_year(year, low, high):
        match = re.match(r'\d\d\d\d', year)
        if not match:
                return False
        year = int(year)
        if year < low or year > high:
               return False
        return True

def check_height(height):
        unit = height[-2:]
        value = height[:-2]
        try:
                value = int(value)
        except:
                return False
        if unit == 'cm':
                return value >= 150 and value <= 193
        elif unit == 'in':
                return value >= 59 and value <= 76
        return False
        
def check_hair_color(color):
        match = re.match(r'^#[0-9a-fA-F]{6}$', color)
        return match is not None

def check_eye_color(color):
        return color in set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])

def check_passport_id(passport_id):
        match = re.match(r'^\d{9}$', passport_id)
        return match is not None

print(main())
