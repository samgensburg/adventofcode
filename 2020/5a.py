def main():
        with open('5.dat', 'r') as file:
                high = 0
                for line in file:
                        line = line.strip()
                        row, col, seat_id = stats_for_seat(line)
                        if seat_id > high:
                                high = seat_id

                return high

def stats_for_seat(seat):
        low = 0
        high = 128
        for c in seat[:7]:
                if c == 'B':
                        low = (low + high) / 2
                else:
                        high = (low + high) / 2
        row = low

        low = 0
        high = 8
        for c in seat[7:]:
                if c == 'R':
                        low = (low + high) / 2
                else:
                        high = (low + high) / 2
        col = low
        seat_id = row * 8 + col
        return (row, col, seat_id)
        
print(main())
