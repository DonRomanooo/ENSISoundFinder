# Find lib #


import concurrent.futures
import multiprocessing


def match(element, tags):
    # find if tags match element keywords or not
    matches = 0

    tags_set = set(tags)

    for tag in tags_set:
        if tag in element["Keywords"]:
            matches += 1
    
    if matches >= len(tags): return element

    return None


def search(array, tags):
    # returns all the element found in the database
    # based on tags
    found = []

    cpus = multiprocessing.cpu_count()

    with concurrent.futures.ThreadPoolExecutor(cpus) as executor:
        futures = []
        for item in array:
            futures.append(executor.submit(match, element=item, tags=tags))
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                found.append(future.result())

    return found

