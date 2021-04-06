# Find lib #


import concurrent.futures


def match(element, tags):
    # find if tags match element keywords or not
    matches = 0

    for tag in tags:
        if tag in element["Keywords"]:
            matches += 1
    
    if matches >= len(tags): return element

    return None


def search(array, tags):
    # returns all the element found in the database
    # based on tags
    found = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for item in array:
            futures.append(executor.submit(match, element=item, tags=tags))
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                found.append(future.result())

    return found

