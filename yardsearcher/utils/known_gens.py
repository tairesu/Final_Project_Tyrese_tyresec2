import json

def file_to_groups(filename):
    all_groups = []
    with open(filename, 'r+') as file:
        all_groups = json.load(file)
        file.close()
    return all_groups

def parse_groups(all_groups: list):
    assert isinstance(all_groups, list) and len(all_groups) > 0
    output = set()
    for group in all_groups:
        makes = group.get('makes', [])
        for make in makes:
            models = make.get('models', [])
            for model in models:
                generations = model.get('generations', [])
                for generation in generations:
                    output.add((generation['name'], make['name'], model['name'], generation['yearStart'], generation['yearEnd']))

    return output
                    
def handle(filename):
    all_groups = file_to_groups(filename)
    return parse_groups(all_groups)

def print_output(output):
    for gen in output:
        print(gen)

        
if __name__ == '__main__':
    all_groups = file_to_groups('all.json')
    output = parse_groups(all_groups)
    print_output(output)