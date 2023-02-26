import queue

from matplotlib import pyplot as plt


# getting heuristics from file
def getHeuristics():
    heuristics = {}
    file = open("heuristics")
    for i in file.readlines():
        node_val = i.split()
        heuristics[node_val[0]] = int(node_val[1])

    return heuristics


# getting cities location from file
def getCity():
    cities = {}
    citiesIndex = {}
    file = open("cities")
    j = 0
    for i in file.readlines():
        node_val = i.split()
        cities[node_val[0]] = [int(node_val[1]), int(node_val[2])]

        citiesIndex[j] = node_val[0]
        j += 1

    return cities, citiesIndex


# creating cities graph from file
def createGraph():
    graph = {}
    file = open("citiesGraph")
    for i in file.readlines():
        node_val = i.split()

        if node_val[0] in graph and node_val[1] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[2], node_val[1]])
            graph.update({node_val[0]: c})

            c = graph.get(node_val[1])
            c.append([node_val[2], node_val[0]])
            graph.update({node_val[1]: c})

        elif node_val[0] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[2], node_val[1]])
            graph.update({node_val[0]: c})

            graph[node_val[1]] = [[node_val[2], node_val[0]]]

        elif node_val[1] in graph:
            c = graph.get(node_val[1])
            c.append([node_val[2], node_val[0]])
            graph.update({node_val[1]: c})

            graph[node_val[0]] = [[node_val[2], node_val[1]]]

        else:
            graph[node_val[0]] = [[node_val[2], node_val[1]]]
            graph[node_val[1]] = [[node_val[2], node_val[0]]]

    return graph


def drawMap(graph, cities, choice, algorithmResult):
    if choice == 1:
        algorithmName = "Best First Search"
    elif choice == 2:
        algorithmName = "Breadth First Search"
    elif choice == 3:
        algorithmName = "Depth First Search"
    elif choice == 4:
        algorithmName = "Greedy Best First Search"
    else:
        algorithmName = "A Star"

    plt.figure(algorithmName)

    for i, j in cities.items():
        plt.plot(j[0], j[1], "ro")
        plt.annotate(i, (j[0] + 1, j[1] + 2))

        for k in graph[i]:
            n = cities[k[1]]
            plt.plot([j[0], n[0]], [j[1], n[1]], "gray")

    for i in range(len(algorithmResult) - 1):
        try:
            first = cities[algorithmResult[i]]
            second = cities[algorithmResult[i + 1]]

            plt.plot([first[0], second[0]], [first[1], second[1]], "blue")
        except:
            exit(1)

    plt.errorbar(1, 1, label=algorithmName, color="blue")
    plt.legend(loc="lower left")

    plt.show()


# Best First Search Algorithm
def BestFirstSearch(graph, startCity, goalCity):
    frontier = queue.PriorityQueue()
    reached = {}

    if startCity == goalCity:
        solution = TraceBackForWeightedAlgorithm(reached, startCity, goalCity)
        return solution

    frontier.put((0, startCity, ''))
    reached[startCity] = [0, '']

    while not frontier.empty():
        node = frontier.get()

        if node[1] == goalCity:
            solution = TraceBackForWeightedAlgorithm(reached, startCity, goalCity)
            return solution

        for child in graph[node[1]]:
            if child[1] not in reached or (int(child[0]) + node[0]) < reached[child[1]][0]:
                child[0] = int(child[0]) + node[0]
                child = [child[0], child[1], node[1]]
                reached[child[1]] = [child[0], child[2]]
                frontier.put(child)

    return "Failure"


def TraceBackForWeightedAlgorithm(reached, startCity, goalCity):
    path = [goalCity]
    current = goalCity
    while current != startCity:
        parentNode = reached[current][1]
        current = parentNode
        path.insert(0, parentNode)
    return path


# Breadth First Search Algorithm
def BreadthFirstSearch(graph, startCity, goalCity):
    frontier = queue.Queue()  # FIFO
    reached = {}

    if startCity == goalCity:
        solution = TraceBackForNoWeightedAlgorithm(reached, startCity, goalCity)
        return solution

    frontier.put((startCity, ''))
    reached[startCity] = ''

    while not frontier.empty():
        node = frontier.get()

        for child in graph[node[0]]:
            if child[1] == goalCity:
                child = [child[1], node[0]]
                reached[child[0]] = child[1]
                solution = TraceBackForNoWeightedAlgorithm(reached, startCity, goalCity)
                return solution
            if child[1] not in reached:
                child = [child[1], node[0]]
                reached[child[0]] = child[1]
                frontier.put(child)

    return "Failure"


def TraceBackForNoWeightedAlgorithm(reached, startCity, goalCity):
    path = [goalCity]
    current = goalCity
    while current != startCity:
        parentNode = reached[current]
        current = parentNode
        path.insert(0, parentNode)
    return path


# Depth First Search Algorithm
def DepthFirstSearch(graph, startCity, goalCity):
    frontier = queue.LifoQueue()
    explored = set()
    reached = {}

    if startCity == goalCity:
        solution = TraceBackForNoWeightedAlgorithm(reached, startCity, goalCity)
        return solution

    frontier.put((startCity, ''))
    reached[startCity] = ''

    while not frontier.empty():
        state = frontier.get()
        explored.add(state[0])
        if state[0] == goalCity:
            solution = TraceBackForNoWeightedAlgorithm(reached, startCity, goalCity)
            return solution

        for neighbor in graph[state[0]]:
            if neighbor[1] not in explored:
                neighbor = [neighbor[1], state[0]]
                frontier.put(neighbor)
                reached[neighbor[0]] = neighbor[1]

    return "Failure"


# Greedy Best First Search Algorithm
def GreedyBestFS(graph, heuristics, startCity, goalCity):
    frontier = queue.PriorityQueue()
    reached = {}

    if startCity == goalCity:
        solution = TraceBackForWeightedAlgorithm(reached, startCity, goalCity)
        return solution

    frontier.put((heuristics[startCity], startCity, ''))
    reached[startCity] = [heuristics[startCity], '']

    while not frontier.empty():
        node = frontier.get()

        if node[1] == goalCity:
            solution = TraceBackForWeightedAlgorithm(reached, startCity, goalCity)
            return solution

        for child in graph[node[1]]:
            childHeuristic = heuristics[child[1]]
            if child[1] not in reached or childHeuristic < reached[child[1]][0]:
                child = [childHeuristic, child[1], node[1]]
                reached[child[1]] = [child[0], child[2]]
                frontier.put(child)

    return "Failure"


# A* Algorithm
def AStar(graph, heuristics, startCity, goalCity):
    initialCost = 0
    frontier = queue.PriorityQueue()
    frontier.put((initialCost + heuristics[startCity], startCity, '', initialCost))
    reached = {startCity: [initialCost + heuristics[startCity], '']}

    if startCity == goalCity:
        solution = TraceBackForWeightedAlgorithm(reached, startCity, goalCity)
        return solution

    while not frontier.empty():
        node = frontier.get()

        if node[1] == goalCity:
            solution = TraceBackForWeightedAlgorithm(reached, startCity, goalCity)
            return solution

        for child in graph[node[1]]:
            childHeuristic = heuristics[child[1]]
            childPathCost = int(child[0]) + node[3] + childHeuristic
            if child[1] not in reached or childPathCost < reached[child[1]][0]:
                child = [childPathCost, child[1], node[1], int(child[0])]
                reached[child[1]] = [child[0], child[2]]
                frontier.put(child)

    return "Failure"


# running the program
def main():
    graph = createGraph()
    heuristics = getHeuristics()
    cities, citiesIndex = getCity()

    for i, j in citiesIndex.items():
        print(i + 1, j)

    while True:
        start = int(input("Enter start city's number (0 for exit): "))
        if start == 0:
            exit(0)

        goal = int(input("Enter goal city's number (0 for exit): "))
        if goal == 0:
            exit(0)

        startCity = citiesIndex[start - 1]
        goalCity = citiesIndex[goal - 1]
        algorithm = ['Best First Search', 'Breadth First Search', 'Depth First Search', 'Greedy Best First Search',
                     'A Star']
        i = 1
        for x in algorithm:
            print(i, x)
            i += 1
        choice = int(input("Enter algorithm's number (0 to exit): "))
        if choice == 0:
            exit(0)
        if choice == 1:
            bestFS = BestFirstSearch(graph, startCity, goalCity)
            print("BestFS => ", bestFS)
            drawMap(graph, cities, choice, bestFS)
        elif choice == 2:
            breadthFS = BreadthFirstSearch(graph, startCity, goalCity)
            print("BreadthFS => ", breadthFS)
            drawMap(graph, cities, choice, breadthFS)
        elif choice == 3:
            depthFS = DepthFirstSearch(graph, startCity, goalCity)
            print("DepthFS => ", depthFS)
            drawMap(graph, cities, choice, depthFS)
        elif choice == 4:
            greedyBestFS = GreedyBestFS(graph, heuristics, startCity, goalCity)
            print("GreedyBestFS => ", greedyBestFS)
            drawMap(graph, cities, choice, greedyBestFS)
        elif choice == 5:
            astar = AStar(graph, heuristics, startCity, goalCity)
            print("AStar => ", astar)
            drawMap(graph, cities, choice, astar)
        else:
            exit(0)


main()
