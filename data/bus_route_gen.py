import re
from collections import defaultdict

# Paths
INPUT_FILE = 'data/new_bus_route_data.txt'
OUTPUT_FILE = 'data/new_bus_routes.md'

# Regex patterns
TYPE_RE = re.compile(r"Type:\s*(.*)", re.IGNORECASE)
TIME_RE = re.compile(r"Time:\s*(.*)", re.IGNORECASE)

SEPARATOR_PATTERN = r"→|->|➡|–|—|−|~|\-|⇄|\\|/|<->|\|"


def parse_bus_blocks(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    buses = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect a route line
        if 'Route:' in line:
            # Determine bus name
            # Case A: previous line is native name in parentheses
            if i >= 2 and lines[i-1].startswith('(') and ')' in lines[i-1]:
                english = lines[i-2]
                native = lines[i-1]
                bus_name = f"{english} {native}"
            # Case B: route and native on same line: '(native) Route:...'
            elif line.startswith('(') and ')' in line.split('Route:')[0]:
                english = lines[i-1]
                native = line.split('Route:')[0].strip()
                bus_name = f"{english} {native}"
            else:
                # No native info
                english = lines[i-1] if i >= 1 else 'Unknown'
                bus_name = english
            # Extract stops
            route_part = line.split('Route:')[1]
            stops = [s.strip() for s in re.split(SEPARATOR_PATTERN, route_part) if s.strip()]
            # Initialize type/time
            bus_type = ''
            bus_time = ''
            # Look ahead for Type/Time
            j = i + 1
            while j < len(lines) and 'Route:' not in lines[j] and not re.match(r'^.+\(.+\)$', lines[j]):
                t = lines[j]
                m1 = TYPE_RE.match(t)
                if m1:
                    bus_type = m1.group(1).strip()
                m2 = TIME_RE.match(t)
                if m2:
                    bus_time = m2.group(1).strip()
                j += 1
            buses.append({'name': bus_name, 'stops': stops, 'type': bus_type, 'time': bus_time})
            i = j
        else:
            i += 1
    return buses


def build_stop_map(buses):
    stop_map = defaultdict(set)
    for bus in buses:
        for stop in bus['stops']:
            stop_map[stop].add(bus['name'])
    return {stop: sorted(names) for stop, names in stop_map.items()}


def build_adjacent_stops(buses):
    adj_map = defaultdict(list)
    for bus in buses:
        stops = bus['stops']
        for idx, stop in enumerate(stops):
            neighbors = []
            # two before
            for j in range(idx-2, idx):
                if 0 <= j < len(stops): neighbors.append(stops[j])
            # two after
            for j in range(idx+1, idx+3):
                if 0 <= j < len(stops): neighbors.append(stops[j])
            # pad if <4
            offset = 3
            while len(neighbors) < 4:
                back = idx - offset
                fwd = idx + offset
                if back >= 0:
                    neighbors.insert(0, stops[back])
                elif fwd < len(stops):
                    neighbors.append(stops[fwd])
                else:
                    break
                offset += 1
            # unique
            for n in neighbors:
                if n != stop and n not in adj_map[stop]:
                    adj_map[stop].append(n)
    return adj_map


def generate_markdown(buses, stop_map, adj_map):
    md = []
    # Segment 1
    md.append("## Segment 1: Bus Details\n")
    for bus in buses:
        md.append(f"### Route: {bus['name']}")
        md.append(f"- **Stops (Forward)**: {' → '.join(bus['stops'])}")
        md.append(f"- **Stops (Reverse)**: {' → '.join(reversed(bus['stops']))}")
        md.append(f"- **Service Time**: {bus['time'] or 'N/A'}")
        md.append(f"- **Service Type**: {bus['type'] or 'N/A'}")
        md.append("")
    # Segment 2
    md.append("## Segment 2: Stops to Buses Map\n")
    for stop in sorted(stop_map):
        md.append(f"- **{stop} Stop**: {', '.join(stop_map[stop])}")
    md.append("")
    # Segment 3
    md.append("## Segment 3: Adjacent Stops (4 Neighbors Each)\n")
    for stop in sorted(adj_map):
        md.append(f"- **{stop}**: {', '.join(adj_map[stop])}")
    return '\n'.join(md)


def main():
    text = open(INPUT_FILE, encoding='utf-8').read()
    buses = parse_bus_blocks(text)
    stop_map = build_stop_map(buses)
    adj_map = build_adjacent_stops(buses)
    markdown = generate_markdown(buses, stop_map, adj_map)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(markdown)
    print(f"Generated {OUTPUT_FILE} with {len(buses)} buses and {len(stop_map)} stops.")


if __name__ == '__main__':
    main()
