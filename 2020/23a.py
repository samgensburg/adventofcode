SIZE = 9

def main():
	deck = [5, 8, 3, 9, 7, 6, 2, 4, 1]
	import pdb; pdb.set_trace()
	for i in range(100):
		print(deck)
		removed = deck[1:4]
		new_deck = deck[:1]
		new_deck.extend(deck[4:])
		insertion_number = deck[0] - 1
		while insertion_number == 0 or insertion_number in removed:
			if insertion_number == 0:
				insertion_number += SIZE
			else:
				insertion_number -= 1
		for i in range(len(new_deck)):
			if new_deck[i] == insertion_number:
				insertion_index = i
		new_new_deck = new_deck[:insertion_index + 1]
		new_new_deck.extend(removed)
		new_new_deck.extend(new_deck[insertion_index + 1:])
		new_new_new_deck = new_new_deck[1:]
		new_new_new_deck.append(new_new_deck[0])
		deck = new_new_new_deck

	return deck

print(main())
