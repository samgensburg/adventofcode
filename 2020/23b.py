SIZE = 1000000

class Node:
	def __init__(self, data, next=None):
		self.data = data
		self.next = next

def main():
	input = [5, 8, 3, 9, 7, 6, 2, 4, 1]
	deck = None
	iterator = None
	lookup = {}
	for n in input:
		if deck is None:
			deck = Node(n)
			iterator = deck
		else:
			iterator.next = Node(n)
			iterator = iterator.next
		lookup[n] = iterator

	for n in range(1000001):
		if n < 10:
			continue
		iterator.next = Node(n)
		iterator = iterator.next
		lookup[n] = iterator
	iterator.next = deck

	for n in range(10000000):
		if n % 100000 == 0:
			print(n)
		removed = deck.next
		deck.next = removed.next.next.next

		insertion_number = deck.data - 1
		removed_values = [removed.data, removed.next.data, removed.next.next.data]
		while insertion_number == 0 or insertion_number in removed_values:
			if insertion_number == 0:
				insertion_number += SIZE
			else:
				insertion_number -= 1

		insertion_point = lookup[insertion_number]
		post_insertion_point = insertion_point.next
		insertion_point.next = removed
		removed.next.next.next = post_insertion_point

		deck = deck.next

	return lookup[1].next.data * lookup[1].next.next.data

print(main())
