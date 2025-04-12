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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        #远离鬼 + 减少食物 + 减少与食物的最短距离
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition() #pacman移动之后的位置
        newFood = successorGameState.getFood() #剩余的食物
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] #示每个幽灵（Ghost）在 Pacman 吃下能量豆（Power Pellet）后，仍然处于“害怕状态”（Scared）的剩余步数
        
        score=0
        # Food estimation
        Food=newFood.asList()

        min_dist=999
        for food in Food:
            dist=util.manhattanDistance(newPos,food)
            if dist < min_dist:
                score+=1/(dist+1)  #距离最近的食物越近越好

        #Ghost_estimation
        for index, GhostState in enumerate(newGhostStates):
             ghostPos=GhostState.getPosition()
             distance = util.manhattanDistance(newPos,ghostPos) 
             if newScaredTimes[index]>0:
                 score+=2/(distance+1)
             else:
                 if distance<4: #保证不死 （一个很大的penalty）
                    score-=500
                 else:
                     score-=2/(distance+1)
                 
        
        score+=successorGameState.getScore()

        return score

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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
    def minimax(self,state,depth,agentIndex):
        if depth==0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state),None
        legal_action=state.getLegalActions(agentIndex)

        if not legal_action:
            return self.evaluationFunction(state),None
        
        nextAgent=(agentIndex+1)%state.getNumAgents()
        if nextAgent==0:
            nextDepth=depth-1
        else:
            nextDepth=depth
        #pacman:
        if agentIndex==0:
            bestvalue=-999
            bestaction=None
            for action in legal_action:
                successor=state.generateSuccessor(agentIndex,action)
                value,_=self.minimax(successor,nextDepth,nextAgent)
                if value>bestvalue:
                    bestvalue=value
                    bestaction=action
            return bestvalue,bestaction
        else: # ghost
            worstvalue=1000
            worstaction=None
            for action in legal_action:
                successor=state.generateSuccessor(agentIndex,action)
                value,_=self.minimax(successor,nextDepth,nextAgent)
                
                if value<worstvalue:
                    worstvalue=value
                    worstaction=action
            return worstvalue,worstaction
                
    def getAction(self, gameState: GameState):
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

        _,action=self.minimax(gameState,self.depth,0)
        return action
        
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
      
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def max_value(state,a,b,agentIndex,depth):
         v=-9999
         best_action=None
         legal_action=state.getLegalActions(agentIndex)
         agent=(agentIndex+1)%state.getNumAgents()
         if agent==0:
             nextDepth=depth-1
         else:
            nextDepth=depth
         for action in legal_action:
            v=max(v,value(state.generateSuccessor(agentIndex,action),a,b,agent,nextDepth))
            if v>=b:
                return v #pruning
            a=max(a,v)
         return v
        
        def min_value(state,a,b,agentIndex,depth):
         v=9999
         legal_action=state.getLegalActions(agentIndex)
         agent=(agentIndex+1)%state.getNumAgents()
         if agent==0:
            nextDepth=depth-1
         else:
            nextDepth=depth
         for action in legal_action:
            v=min(v,value(state.generateSuccessor(agentIndex,action),a,b,agent,nextDepth))
            if v<=a: #min节点的value只会越来越小，如果当下已经小于max的最好值了，就可以直接返回出栈了
                return v,  #pruning
            b=min(b,v) 
         return v 

        def value(state,a,b,agent,depth):
            if state.isWin() or state.isLose() or depth-1==0:
                return self.evaluationFunction(state)
            elif agent==0:
                return max_value(state,a,b,agent,depth)
            else:
                return min_value(state,a,b,agent,depth)
        
        legalActions=gameState.getLegalActions(0)
        a=-9990
        b=9999
        bs=-1000
        ba=None
        for action in legalActions:
            score=value(gameState.generateSuccessor(0,action),a,b,1,self.depth)
            if score>bs:
                bs=score
                ba=action

            a=max(a,bs)
        return ba

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
