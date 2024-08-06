
import json

def parse_menu(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    menu = {}
    current_category = None
    current_item = None

    for i, line in enumerate(lines):
        # Determine the indentation level
        indent_level = len(line) - len(line.lstrip())

        # Skip empty lines
        if not line.strip():
            continue

        # Check if line is a category (no indentation)
        if indent_level == 0:
            current_category = line[:-1]
            if current_category == 'Sides:':
                 print('hithere')
            menu[current_category] = {}
            current_item = None
            continue

        # Check if line is an item (4 spaces of indentation)
        if indent_level == 4:
            # Check if the previous line was an item
            if current_item:
                # If we had a previous item and it had details, ensure they are appended properly
                if not menu[current_category][current_item]:
                    menu[current_category][current_item] = []
            current_item = line.strip()
            if current_category not in menu:
                menu[current_category] = {}
            menu[current_category][current_item] = []
            continue

        # Check if line is a detail (8 spaces of indentation)
        if indent_level == 8 and current_item:
            menu[current_category][current_item].append(line.strip())

        # Handle edge case for last line as an item without details
        if indent_level == 4 and i == len(lines) - 1:
            if current_item:
                if not menu[current_category][current_item]:
                    menu[current_category][current_item] = []

    return menu

# File paths
input_file_path = 'pizza_menu.txt'
output_file_path = 'pizza_menu.json'

# Parse and convert to JSON
parsed_menu = parse_menu(input_file_path)

# Convert to JSON with indentation for readability
json_output = json.dumps(parsed_menu, indent=4)

# Write JSON to a file


print("Conversion complete! Check burger_menu.json for the result.")
#xxxxxxxxxxxxxxxxxxx
def fix_empty_lists(menu):
    for category in menu:
        items = list(menu[category].keys())
        new_menu = {}
        combined_items = []

        for item in items:
            if menu[category][item] == []:
                combined_items.append(item)
            else:
                if combined_items:
                    new_menu[category] = combined_items
                    combined_items = []
                new_menu[item] = menu[category][item]

        # Handle any remaining combined items
        if combined_items:
            new_menu[category] = combined_items

        menu[category] = new_menu

    return menu

# Example usage
#parsed_menu = parse_menu(file_path)
t = fix_empty_lists(parsed_menu)
json_output = json.dumps(t, indent=4)

with open(output_file_path, 'w') as json_file:
    json_file.write(json_output)

