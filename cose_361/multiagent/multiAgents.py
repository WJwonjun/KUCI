# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newfood=newFood.asList()
        ghoPos = [(ghost.getPosition()[0], ghost.getPosition()[1]) for ghost in newGhostStates]
        scared =newScaredTimes[0]>0

        if not scared and (newPos in ghoPos):
            return -1
        
        if newPos in currentGameState.getFood().asList():
            return 1
        
        closeFood = sorted(newfood, key = lambda fdis:util.manhattanDistance(fdis,newPos))    
        closeGho = sorted(ghoPos, key=lambda gDist: util.manhattanDistance(gDist, newPos))

        fd = lambda fDis: util.manhattanDistance(fDis, newPos)

        gd = lambda gDis: util.manhattanDistance(gDis, newPos)

        return 1/fd(closeFood[0]) - 1/gd(closeGho[0])


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        numGho = [i for i in range(1,gameState.getNumAgents())]
        
        def ret(state,d):
            return state.isWin() or state.isLose() or d == self.depth
        
        def minval(state,d,ghost):
            if ret(state,d):
                return self.evaluationFunction(state)
            
            v = 1e9
            for action in state.getLegalActions(ghost):
                if ghost == numGho[-1]: 
                    v = min(v, maxval(state.generateSuccessor(ghost,action),d+1))
                else: 
                    v = min(v, minval(state.generateSuccessor(ghost,action),d,ghost+1))
            return v

        def maxval(state,d):
            if ret(state,d):
                return self.evaluationFunction(state)
            
            v= -1e9
            for action in state.getLegalActions(0):
                v = max(v, minval(state.generateSuccessor(0,action),d,1))
            return v
        
        actions = [(action, minval(gameState.generateSuccessor(0,action),0,1)) for action in gameState.getLegalActions(0)]

        actions.sort(key = lambda x: x[1])
        return actions[-1][0]

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a = -1e9
        b = 1e9
        c_v = -1e9
        npacaction = Directions.STOP
        la = gameState.getLegalActions(0).copy()
        for next_action in la:
            nextState = gameState.generateSuccessor(0,next_action)
            nextValue = self.get_nodevalue(nextState,0,1,a,b)
            if nextValue > c_v:
                c_v, npacaction = nextValue, next_action
            a = max(a, c_v)
        return npacaction 
     
        util.raiseNotDefined()

    def get_nodevalue(self,gameState,depth,agentindex,a,b):

        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        elif agentindex == 0 :          
            return self.asearch(gameState,depth,agentindex,a,b)
        else:
            return self.bsearch(gameState,depth,agentindex,a,b)
    
    def asearch(self,gameState,depth,agentindex,a,b):
        v = -1e9
        for index, action in enumerate(gameState.getLegalActions(agentindex)):
            v = max(v, self.get_nodevalue(gameState.generateSuccessor(agentindex,action),depth,agentindex+1,a,b))
            if v > b : 
                return v
            a = max(a,v)
        return v

    def bsearch(self,gameState,depth,agentindex,a,b):
        v = 1e9
        for index, action in enumerate(gameState.getLegalActions(agentindex)):
            if agentindex == gameState.getNumAgents() -1:
                v = min(v,self.get_nodevalue(gameState.generateSuccessor(agentindex,action),depth+1,0,a,b)) 
                if v< a:
                    return v   
            else : 
                v = min(v, self.get_nodevalue(gameState.generateSuccessor(agentindex,action),depth,agentindex+1,a,b))
                if v< a:
                    return v
            
            b = min(b,v)
        return v  
           

        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
