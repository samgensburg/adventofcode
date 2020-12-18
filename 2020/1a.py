def main():
        with open('1a.dat', 'r') as file:
                found = set()
                for line in file:
                        num = int(line)
                        if num in found:
                                return num * (2020 - num)
                        found.add(2020 - num)
print(main())
