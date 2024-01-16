from collections import defaultdict
from pathlib import Path
from queue import Queue
import re

DATA_FILE = Path(__file__).stem + '.dat'

class Path():
	def __init__(self, valve, path=None):
		self.current_valve = valve
		if path == None:
			self.pressure = 0
			self.current_rate = 0
			self.path = [valve.name]
			self.depth = 0
		else:
			time_elapsed = path.current_valve.travel_times[valve.name] + 1
			self.depth = path.depth + time_elapsed
			self.pressure = path.pressure + path.current_rate * time_elapsed
			self.current_rate = path.current_rate + valve.flow

			self.path = path.path.copy()
			self.path.append(valve.name)
	
	def generate_actions(self):
		out = []
		assert self.depth <= 30
		for destination in self.current_valve.travel_times:
			travel_time = self.current_valve.travel_times[destination] + 1
			if self.depth + travel_time > 30:
				continue
			if destination in self.path:
				continue
			out.append(destination)
		return out
	
	def __repr__(self):
		out = ', '.join(self.path)
		return out


class Valve():
	def __init__(self, text):
		match = re.match(r'Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (\w\w)((, \w\w)*)', text)
		assert match
		self.name = match.group(1)
		self.flow = int(match.group(2))
		self.destinations = [match.group(3)]
		further_destinations = match.group(4)
		while further_destinations:
			assert len(further_destinations) % 4 == 0
			self.destinations.append(further_destinations[2:4])
			further_destinations = further_destinations[4:]

	def generate_targets_from_destination_names(self, map):
		self.targets = [map[destination] for destination in self.destinations]

	def generate_distances(self, key_targets):
		self.travel_times = {}
		visited = set()
		visit_queue = Queue()
		visit_queue.put((self, 0))
		while not visit_queue.empty():
			loc, distance = visit_queue.get()
			if loc.name in visited:
				continue
			
			visited.add(loc.name)
			if loc.name in key_targets and loc.name != self.name:
				self.travel_times[loc.name] = distance
			
			for target in loc.targets:
				visit_queue.put((target, distance + 1))


def process_input(lines):
	valves = [Valve(line) for line in lines]
	map = {}
	for valve in valves:
		map[valve.name] = valve

	for valve in valves:
		valve.generate_targets_from_destination_names(map)
	
	key_targets = [valve.name for valve in valves if valve.flow > 0]
	for valve in valves:
		if valve.flow > 0:
			valve.generate_distances(key_targets)
	map['AA'].generate_distances(key_targets)

	return map

def solve_a(map):
	start = Path(map['AA'])
	best = 0
	path_queue = Queue()
	path_queue.put(start)
	while not path_queue.empty():
		path = path_queue.get()
		if path.depth == 30:
			best = max(best, path.pressure)
			continue

		for action in path.generate_actions():
			new_path = Path(map[action], path)
			path_queue.put(new_path)

		sit_value = path.pressure + path.current_rate * (30 - path.depth)
		best = max(best, sit_value)

	return best

def solve_b(map):
	start = Path(map['AA'])
	start.depth = 4
	path_queue = Queue()
	path_queue.put(start)
	best_pressures = {}
	path_queue_2 = Queue()
	while not path_queue.empty():
		path = path_queue.get()
		for action in path.generate_actions():
			new_path = Path(map[action], path)
			path_queue.put(new_path)

		sit_value = path.pressure + path.current_rate * (30 - path.depth)
		save_path = path.path.copy()[1:]
		key = ''.join(sorted(save_path))
		if key in best_pressures:
			best_pressures[key] = (max(sit_value, best_pressures[key][0]), save_path)
		else:
			best_pressures[key] = (sit_value, save_path)

	best = 0
	for key in best_pressures:
		pressure, save_path = best_pressures[key]
		s = set(save_path)
		for key2 in best_pressures:
			pressure2, save_path2 = best_pressures[key2]
			s2 = set(save_path2)
			if len(s.intersection(s2)) == 0:
				best = max(best, pressure + pressure2)

	return best



def main():
	with open(DATA_FILE, 'r') as file:
		lines = file.read().strip().split('\n')

	map = process_input(lines)
	return solve_a(map), solve_b(map)


print(main())
