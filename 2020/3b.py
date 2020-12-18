import re

def main(right, down):
        with open('3.dat', 'r') as file:
                y = 0
                count = 0
                fall = down - 1
                for line in file:
                        fall += 1
                        if fall == down:
                                fall = 0
                        else:
                                continue

                        line = line.strip()
                        width = len(line)
                        if line[y] == '#':
                                count += 1
                        
                        y = (y + right) % width
                return count

print(main(1, 1))
print(main(3, 1))
print(main(5, 1))
print(main(7, 1))
print(main(1, 2))
