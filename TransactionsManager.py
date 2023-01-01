from collections import defaultdict
delimiter = " -> "

class Graph:
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed

    def addEdge(self, frm, to):
        self.graph[frm - 1].append(to - 1)

        if self.directed is False:
            self.graph[to - 1].append(frm - 1)
        else:
            self.graph[to - 1] = self.graph[to - 1]

    def topoSortvisit(self, s, visited, sortlist):
        visited[s] = True

        for i in self.graph[s]:
            if not visited[i]:
                self.topoSortvisit(i, visited, sortlist)

        sortlist.insert(0, s)

    def topoSort(self):
        visited = {i: False for i in self.graph}

        sortlist = []

        for v in self.graph:
            if not visited[v]:
                self.topoSortvisit(v, visited, sortlist)

        for i in range(0, len(sortlist)):
            print("T", sortlist[i] + 1, sep="", end='')
            if not i == len(sortlist) - 1:
                print(delimiter, end='')

    def isCyclicUtil(self, v, visited, recStack):
        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic
        for neighbour in self.graph[v]:
            if not visited[neighbour]:
                if self.isCyclicUtil(neighbour, visited, recStack):
                    return True
            elif recStack[neighbour]:
                return True

        # The node needs to be poped from
        # recursion stack before function ends
        recStack[v] = False
        return False

    # Returns true if graph is cyclic else false
    def isCyclic(self, numOfVertices):
        visited = [False] * numOfVertices
        recStack = [False] * numOfVertices
        for node in range(numOfVertices):
            if not visited[node]:
                if self.isCyclicUtil(node, visited, recStack):
                    return True
        return False


def transactionsStringToList(transactionInput):
    transactionInput = transactionInput.replace(' ', "")
    if transactionInput.endswith(';'):
        transactionInput = transactionInput[:len(transactionInput) - 1]

    return transactionInput.split(';')


def addPrecedenceInTransactionListToGraph(transactionList, precedenceGraph):
    # compring every Transaction to every transaction after it
    for i in range(0, len(transactionList)):
        currentTransaction = transactionList[i]
        currentTransaction = currentTransaction.replace('(', "").replace(')', "")  # remove "(value)"

        transactionName = currentTransaction[0]
        transactionTreeNumber = int(currentTransaction[1])
        transactionValue = currentTransaction[2]

        for j in range(i + 1, len(transactionList)):
            comparedTransaction = transactionList[j]
            comparedTransaction = comparedTransaction.replace('(', "").replace(')', "")  # remove "(value)"

            comparedTransactionName = comparedTransaction[0]
            comparedTransactionTreeNumber = int(comparedTransaction[1])
            comparedTransactionValue = comparedTransaction[2]

            if transactionValue is comparedTransactionValue and comparedTransactionName is not transactionName:
                if transactionTreeNumber + 1 == comparedTransactionTreeNumber or comparedTransactionTreeNumber + 1 == transactionTreeNumber:

                    precedenceGraph.addEdge(transactionTreeNumber, comparedTransactionTreeNumber)


def main():
    transactionInput = input("Please enter query: ")
    transactionList = transactionsStringToList(transactionInput)
    precedenceGraph = Graph(directed=True)
    addPrecedenceInTransactionListToGraph(transactionList, precedenceGraph)

    if precedenceGraph.isCyclic(len(precedenceGraph.graph)):
        print("NO.")
    else:
        precedenceGraph.topoSort()


if __name__ == '__main__':
    main()
