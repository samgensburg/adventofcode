def main():
        with open('1a.dat', 'r') as file:
                found1 = []
                found2 = dict()
                for line in file:
                        num = int(line)
                        if num in found2:
                                return num * found2[num][0] * found2[num][1]
                        for num2 in found1:
                                subtotal = num + num2
                                if subtotal >= 2020:
                                        continue
                                if subtotal in found2:
                                        continue
                                found2[2020 - subtotal] = (num, num2)
                        found1.append(num)
print(main())
