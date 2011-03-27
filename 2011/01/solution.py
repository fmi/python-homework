def make_multiset(objects):
    result = {}
    for obj in objects:
        result[obj] = result.get(obj, 0) + 1
    return result

def ordered_dict(dictionary):
    return sorted(dictionary.items())

def reversed_dict(dictionary):
    return dict(map(reversed, dictionary.items()))

def unique_objects(objects):
    return len(set(map(id, objects)))
