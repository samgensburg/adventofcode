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
        return True

print(main())
