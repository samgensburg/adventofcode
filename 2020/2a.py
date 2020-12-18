import re

def main():
        with open('2.dat', 'r') as file:
                count = 0
                for line in file:
                        match = re.match(r'^(\d+)-(\d+) (\w): (.+)$', line)
                        assert match
                        low = int(match.group(1))
                        high = int(match.group(2))
                        char = match.group(3)
                        password = match.group(4)
                        found = 0
                        
                        for c in password:
                                if c == char:
                                        found += 1
                        if found >= low and found <= high:
                                count += 1
                return count

print(main())
