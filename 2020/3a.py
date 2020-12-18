import re

def main():
        with open('3.dat', 'r') as file:
                y = 0
                count = 0
                for line in file:
                        line = line.strip()
                        width = len(line)
                        if line[y] == '#':
                                count += 1
                        
                        y = (y + 3) % width
                return count

print(main())
