# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders wefre primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from operator import truediv
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    # declare the froniter list with start state and path
    _frontier = [[problem.getStartState(), []]]

    # declare the explored set as a list
    _explored_set = []

    while _frontier:
        # pop the last element in the frontier 
        vertex, path = _frontier.pop()

        # if the vertex in explored set, ignore the vertex
        if vertex in _explored_set:
            continue
        
        _explored_set.append(vertex)

        # if the vertex is the goal state then return the path
        if problem.isGoalState(vertex):
            return path

        # get the successors for the vertex
        successors = problem.getSuccessors(vertex)

        # modeify the successor list to only contain the nodes and actions  
        successors = list(map(lambda x : [x[0],path+[x[1]]], successors))

        # add the successor list the frontier list
        _frontier.extend(successors)

    return path

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # declare the froniter list with start state and path
    _frontier = [[problem.getStartState(), []]]

    # declare the explored set as a list
    _explored_set = []

    while _frontier:
        # pop the last element in the frontier 
        vertex, path = _frontier.pop(0)

        # if the vertex in explored set, ignore the vertex
        if vertex in _explored_set:
            continue
        
        _explored_set.append(vertex)

        # if the vertex is the goal state then return the path
        if problem.isGoalState(vertex):
            return path

        # get the successors for the vertex
        successors = problem.getSuccessors(vertex)

        # modeify the successor list to only contain the nodes and actions  
        successors = list(map(lambda x : [x[0],path+[x[1]]], successors))

        # add the successor list the frontier list
        _frontier.extend(successors)

    return path


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    # initialise the frontier as a priority queue
    _frontier = util.PriorityQueue()
    
    # get the start state of the problem
    start_state = problem.getStartState()

    # add the start state to the frontier along with a path list
    _frontier.push([start_state, []], 0)

    # declare the explored set list
    explored_set = []

    import heapq

    def pq_update(pq, item, priority):
        '''
            Method to update the elements in the priority queue

        PARAMS:
            pq      : priority queue object
            item    : item to be updated
            priority    : new priority value

        RETURNS:
            None
        '''

        for index, (p, c, i) in enumerate(pq.heap):

            # if vertex is found
            if i[0] == item[0]:
                if p <= priority:
                    break

                del pq.heap[index]

                # add the updated entity to the priority queue
                pq.heap.append((priority, c, item))
                heapq.heapify(pq.heap)
                break
        else:
            pq.push(item, priority)



    while _frontier:
        # pop the last element in the frontier 
        vertex, path = _frontier.pop()
        
        # if the vertex in explored set, ignore the vertex
        if vertex in explored_set:
            continue

        explored_set.append(vertex)

        # if the vertex is the goal state then return the path
        if problem.isGoalState(vertex):
            return path

        # get the successors for the vertex     
        successors = problem.getSuccessors(vertex)

        # add the successors to the frontier, if a shorter path found -> update the priority
        for i in successors:
            pq_update(_frontier, [i[0], path + [i[1]]], problem.getCostOfActions(path + [i[1]]))

    return path

    util.raiseNotDefined()

def nullHeuristic(state, problem=None): 
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0        

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # initialise the frontier as a priority queue
    _frontier = util.PriorityQueue()
    
    # get the start state of the problem
    start_state = problem.getStartState()

    # add the start state to the frontier along with a path list
    _frontier.push([start_state, []],0)

    # declare the explored set list 
    explored_set = []

    import heapq

    def pq_update(pq, item, priority):
        '''
            Method to update the elements in the priority queue

        PARAMS:
            pq      : priority queue object
            item    : item to be updated
            priority    : new priority value

        RETURNS:
            None
        '''
        for index, (p, c, i) in enumerate(pq.heap):

            # if vertex is found
            if i[0] == item[0]:
                if p <= priority:
                    break

                del pq.heap[index]

                # add the updated entity to the priority queue
                pq.heap.append((priority, c, item))
                heapq.heapify(pq.heap)
                break
        else:
            pq.push(item, priority)


    while _frontier:        

        # pop the last element in the frontier     
        vertex, path = _frontier.pop()
        
        # if the vertex in explored set, ignore the vertex
        if vertex in explored_set:
            continue

        explored_set.append(vertex)
        
        # if the vertex is the goal state then return the path
        if problem.isGoalState(vertex):
            return path

        # get the successors for the vertex     
        successors = problem.getSuccessors(vertex)

        # add the successors to the frontier, if a shorter path found -> update the priority
        for i in successors:    
            pq_update(_frontier, [i[0], path + [i[1]]],  heuristic(i[0],problem) + problem.getCostOfActions(path + [i[1]]))

    return path    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
