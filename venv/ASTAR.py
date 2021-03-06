import sys
graph = {
    'Oradea': ['zeriland', 'sibiu'],
    'zeriland': ['Oradea', 'Arad'],
    'Arad': ['zeriland', 'sibiu', 'Timisoara'],
    'sibiu': ['Oradea', 'Arad', 'fagaras', 'Rimnicu'],
    'fagaras': ['sibiu', 'Bucharest'],
    'Timisoara': ['Arad', 'Logoj'],
    'Rimnicu': ['sibiu', 'Pitesti', 'Craiova'],
    'Logoj': ['Timisoara', 'Mehadia'],
    'Pitesti': ['Rimnicu', 'Craiova', 'Bucharest'],
    'Mehadia': ['Logoj', 'Dobreta'],
    'Dobreta': ['Mehadia', 'Craiova'],
    'Craiova': ['Dobreta', 'Rimnicu', 'Pitesti'],
    'Bucharest': ['fagaras', 'Pitesti', 'Giurgiu', 'Urziceni'],
    'Giurgiu': ['Bucharest'],
    'Urziceni': ['Bucharest', 'Hirsova', 'Vaslui'],
    'Hirsova': ['Urziceni', 'Eforie'],
    'Eforie': ['Hirsova'],
    'Vaslui': ['Urziceni', 'Lasi'],
    'Lasi': ['Vaslui', 'Neamt'],
    'Neamt': ['Lasi']
}
heuristic = {
    'Oradea': [380],
    'zeriland': [374],
    'Arad': [366],
    'sibiu': [253],
    'fagaras': [178],
    'Timisoara': [329],
    'Rimnicu': [193],
    'Logoj': [244],
    'Pitesti': [98],
    'Mehadia': [241],
    'Dobreta': [242],
    'Craiova': [160],
    'Bucharest': [0],
    'Giurgiu': [77],
    'Urziceni': [80],
    'Hirsova': [151],
    'Eforie': [161],
    'Vaslui': [199],
    'Lasi': [226],
    'Neamt': [234]
}
price = {
    'Oradea': [71, 151],
    'zeriland': [71, 75],
    'Arad': [75, 140, 118],
    'sibiu': [151, 140, 99, 80],
    'fagaras': [99, 211],
    'Timisoara': [118, 111],
    'Rimnicu': [80, 97, 146],
    'Logoj': [111, 70],
    'Pitesti': [97, 138, 101],
    'Mehadia': [70, 75],
    'Dobreta': [75, 120],
    'Craiova': [120, 146, 138],
    'Bucharest': [211, 101, 90, 85],
    'Giurgiu': [90],
    'Urziceni': [85, 98, 142],
    'Hirsova': [98, 86],
    'Eforie': [86],
    'Vaslui': [142, 92],
    'Lasi': [92, 87],
    'Neamt': [87]
}


# I used the heap sort that was here https://www.geeksforgeeks.org/heap-sort/ but i changed it much
def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and is
    # greater than root
    if l < n:
        pathi, costi, ti = arr[i]
        pathl, costl, tl = arr[l]
        if costi < costl:
            largest = l
    # See if right child of root exists and is
    # greater than root
    if r < n:
        pathLarge, costLarge, tLarge = arr[largest]
        pathr, costr, tr = arr[r]
        if costLarge < costr:
            largest = r

        # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap

        # Heapify the root.
        heapify(arr, n, largest)

    # The main function to sort an array of given size


def heapSort(arr):
    n = len(arr)
    # Build a maxheap.
    for i in range(n, -1, -1):
        heapify(arr, n, i)

        # One by one extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)


def aStarSearchTree(graph, heuristic, price, start, end):
    # maintain a queue of paths
    queue = []
    totalCost = 0
    # push the first path into the queue using it's own heuristic
    heuFullNode = heuristic.get(start, [])
    heuStart = heuFullNode[0]
    queue.append(([start], heuStart, totalCost))
    # here i measure the real size of each algorithm in bytes
    storage = sys.getsizeof(queue)
    # initialize the visited number of nodes and extended number on nodes*
    visitSize = 1
    extendSize = 0
    while queue:
        # get the first path from the queue
        heapSort(queue)
        path, cost, total = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        extendSize += 1
        if sys.getsizeof(queue) > storage:
            storage = sys.getsizeof(queue)
        # path found
        if node == end:
            return path, extendSize, visitSize, totalCost, storage
        i = 0
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            heuFullNode = heuristic.get(adjacent, [])
            heuNode = heuFullNode[0]
            costFullNode = price.get(node, [])
            costNode = costFullNode[i]
            costPlusHeu = costNode + heuNode
            totalCost = total + costNode
            i += 1
            visitSize += 1
            new_path = list(path)
            new_path.append(adjacent)
            queue.append((new_path, costPlusHeu, totalCost))


def aStarSearchGraph(graph, heuristic, price, start, end):
    # maintain a queue of paths
    queue = []
    totalCost = 0
    # make close list for check if one node was visited before or not and push the root
    closeList = []
    # push the first path into the queue using it's own heuristic
    heuFullNode = heuristic.get(start, [])
    heuStart = heuFullNode[0]
    queue.append(([start], heuStart, totalCost))
    # here i measure the real size of each algorithm in bytes
    storage = sys.getsizeof(queue)
    # initialize the visited number of nodes and extended number on nodes*
    visitSize = 1
    extendSize = 0

    while queue:
        # get the first path from the queue
        heapSort(queue)
        path, cost, total = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node in closeList:
            continue
        extendSize += 1
        closeList.append(node)
        if sys.getsizeof(queue) + sys.getsizeof(closeList) > storage:
            storage = sys.getsizeof(queue) + sys.getsizeof(closeList)
        # path found
        if node == end:
            return path, extendSize, visitSize, totalCost, storage
        i = 0
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            if adjacent in closeList:
                i += 1
                continue
            heuFullNode = heuristic.get(adjacent, [])
            heuNode = heuFullNode[0]
            costFullNode = price.get(node, [])
            costNode = costFullNode[i]
            costPlusHeu = costNode + heuNode
            totalCost = total + costNode
            i += 1
            visitSize += 1
            new_path = list(path)
            new_path.append(adjacent)
            queue.append((new_path, costPlusHeu, totalCost))


if __name__ == "__main__":
    path, extend, visit, total, storage = aStarSearchTree(graph, heuristic, price, 'Arad', 'Bucharest')
    print("Path : ", path, " Cost : ", total, " Extended : ", extend, " Visited : ", visit, " Storage : ",
          storage)
