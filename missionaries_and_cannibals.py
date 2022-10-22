
import queue


class stateSpaceInfo():
    def __init__(self, startNode, goalNode):
        print ("=======Start stateSpace=======")

        self.startNode = startNode
        self.goalNode = goalNode

        self.stateSpaceGraph = self.generateStateGraph()
        # print(self.stateSpaceGraph)

        self.nodeGraph = self.generateNodes()

    # node ={cannibolsRight, missonariesRight, boatRight, cannibolsLeft, missonariesLeft, boatLeft}
    def generateNodes(self):
        nodeDefs = {'S' : [3,3,1,0,0,0], 'A' : [1,3,0,2,0,1], 'B': [2,3,0,1,0,1], 'C': [2,2,0,1,1,1],
                    'D': [2,3,1,1,0,0], 'E': [0,3,0,3,0,1], 'F': [1,3,1,2,0,0], 'G': [1,1,0,2,2,1],
                    'H': [2,2,1,1,1,0], 'I': [2,0,0,1,3,0], 'J': [3,0,1,0,3,0], 'K': [1,0,0,2,3,1],
                    'L': [1,1,1,2,2,0], 'M': [2,0,1,1,3,0], 'Z': [0,0,0,3,3,1]}
        return nodeDefs

    def generateStateGraph(self):
        stateSpaceGraph = {'S' : ['A','B','C'], 'A' : ['S', 'D'], 'B' : ['S'], 'C':['S', 'D'],
                           'D' : ['A','C', 'E'], 'E' : ['D', 'F'], 'F' : ['E', 'G'], 'G' : ['F', 'H'],
                           'H' : ['G', 'I'], 'I' : ['H', 'J'], 'J' : ['H', 'K'], 'K' : ['J', 'L', 'M'],
                           'L' : ['K', 'Z'], 'M' : ['K', 'Z'], 'Z' : [] }
        return stateSpaceGraph


    def calculateHeuristicVal(self, node, heuristic):

        heuristicVal = 0
        nodeValues = self.nodeGraph[node]

        # h1(n) = (cannibolsRight + missonariesRight) - 1 
        if heuristic == 1:
            heuristicVal = (nodeValues[0]+nodeValues[1])/2

        # h2(n) = (cannibolsRight + missonariesRight) / boat 
        if heuristic == 2:
            heuristicVal = (nodeValues[0]+nodeValues[1])/2

        # print ('Heuricstic : Node', node, 'Value ', heuristicVal)
        return heuristicVal


    def getNeighbors(self, node):
        return self.stateSpaceGraph[node]    




class searchAlgorithems():
    def __init__(self, runAlgo, startNode, goalNode, heuristic=0):
            print ("=======Start searchAlgorithems=======")

            self.algo = runAlgo
            self.stateSpace = stateSpaceInfo(startNode, goalNode)
            self.runAlgorithem(self.algo, self.stateSpace, heuristic)


    def runAlgorithem (self, algoName, stateSpace, heuristic):
       
        print ("=======Start runAlgorithem=======")

        results = []

        if algoName == 'bfs':
            results = self.breathFirstSearch(stateSpace)

        elif algoName == 'dfs':    
            totResults = self.depthFirstSearch(stateSpace)
            print('Run Algo ', "dfs", "Final List", totResults) 
            index = totResults.index(self.stateSpace.goalNode) 
            results = totResults[0:index+1]
 
        elif algoName == 'greedybfs':   
            results = self.greedyBestFirstSearch(stateSpace)

        elif algoName == 'astar':   
            results = self.aStarAlgorithem(stateSpace, heuristic)

        else:
            print("Error - Unkown algo") 

        print('Run Algo : ', algoName, "Solution :", results)
        print('Number of steps to reach the goal :',  len(results) )      



    def breathFirstSearch(self, stateSpace):
        print ("=======Start breathFirstSearch=======")   

        visitedList = []
        queueList = []
        resultList = []

        visitedList.append(stateSpace.startNode) 
        queueList.append(stateSpace.startNode)

        # print("Visited", visitedList)
        # print("Queued", queueList)

        while queueList:
            node = queueList.pop(0)
            resultList.append(node)

            if (node == stateSpace.goalNode):
                break

            for adj in stateSpace.stateSpaceGraph[node]:
                if adj not in visitedList:
                    visitedList.append(adj)
                    queueList.append(adj)
        return resultList            


    def depthFirstSearch(self, stateSpace):
        print ("=======Start deapthFirstSearch=======")  

        visitedList = set()
        resultList = []

        def DFS(graph, visitedList, currentNode):

            if currentNode not in visitedList:
                resultList.append(currentNode)
                visitedList.add(currentNode)

                for adj in graph[currentNode]:
                    # print("adj", adj)  
                    DFS(graph, visitedList, adj)

        DFS(stateSpace.stateSpaceGraph, visitedList, stateSpace.startNode) 
        return resultList           

    
    def aStarAlgorithem (self, stateSpace, heuristic):
        print ("=======Start aStarAlgorithem=======")

        openList = set([stateSpace.startNode])
        closedList = set([])

        distance = {}
        distance[stateSpace.startNode] = 0

        parents = {}
        parents[stateSpace.startNode] = stateSpace.startNode

        while len(openList) > 0:
            n = None

            for v in openList:
                if n == None or distance[v] + stateSpace.calculateHeuristicVal(v, heuristic) < distance[n] + stateSpace.calculateHeuristicVal(n, heuristic):
                    n = v;

            if n == None:
                print('quit - a path do not exist')
                return None


            if n == stateSpace.goalNode:
                reconstPath = []

                while parents[n] != n:
                    reconstPath.append(n)
                    n = parents[n]

                reconstPath.append(stateSpace.startNode)

                reconstPath.reverse()

                print('Successful - Path found')
                return reconstPath

            
            for m in stateSpace.getNeighbors(n):
                if m not in openList and m not in closedList:
                    openList.add(m)
                    parents[m] = n
                    distance[m] = distance[n] + 1

                else:
                    if distance[m] > distance[n] + 1:
                        distance[m] = distance[n] + 1
                        parents[m] = n

                        if m in closedList:
                            closedList.remove(m)
                            openList.add(m)

            openList.remove(n)
            closedList.add(n)

        print('quit - a path do not exist')
        return None


    def greedyBestFirstSearch (self, stateSpace):
        print ("=======Start greedyBestFirstSearch=======")

        openList = set([stateSpace.startNode])
        closedList = set([])

        distance = {}
        distance[stateSpace.startNode] = 0

        parents = {}
        parents[stateSpace.startNode] = stateSpace.startNode

        while len(openList) > 0:
            n = None

            for v in openList:
                if n == None or distance[v]  < distance[n] :
                    n = v;

            if n == None:
                print('quit - a path do not exist')
                return None


            if n == stateSpace.goalNode:
                reconstPath = []

                while parents[n] != n:
                    reconstPath.append(n)
                    n = parents[n]

                reconstPath.append(stateSpace.startNode)

                reconstPath.reverse()

                print('Successful - Path found')
                return reconstPath

            
            for m in stateSpace.getNeighbors(n):
                if m not in openList and m not in closedList:
                    openList.add(m)
                    parents[m] = n
                    distance[m] = distance[n] + 1

                else:
                    if distance[m] > distance[n] + 1:
                        distance[m] = distance[n] + 1
                        parents[m] = n

                        if m in closedList:
                            closedList.remove(m)
                            openList.add(m)

            openList.remove(n)
            closedList.add(n)

        print('quit - a path do not exist')
        return None



        


if __name__ == "__main__":
    # Part 2
    # searchAlgorithems('bfs', 'S', 'Z')
    # searchAlgorithems('dfs', 'S', 'Z')

    # Part 3
    # searchAlgorithems('astar', 'S', 'Z', 1)
    # searchAlgorithems('astar', 'S', 'Z', 2)
    searchAlgorithems('greedybfs', 'S', 'Z')
