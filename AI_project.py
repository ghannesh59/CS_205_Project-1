#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import copy  #importing copy library for using deepcopy
import time  #importing time library for claculating time


# In[108]:


def main():
    print("welcome to 8x8 puzzle\n ")
    
    row1=list(input("Enter the row1 without any space seperating the numbers: "))#Taking 1st row as input
    row2=list(input("Enter the row2 without any space seperating the numbers: "))#Taking 2nd row as input
    row3=list(input("Enter the row3 without any space seperating the numbers: "))#Taking 3rd row as input
    row1=[int(i) for i in row1]
    row2=[int(i) for i in row2]
    row3=[int(i) for i in row3]
    puzzle=[row1,row2,row3]
    
    print(puzzle)
     
    algorithm = input('choose the algorithm \n 1. Uniform Cost Search '
                 '\n 2. A* with Misplaced Tile heuristic. \n 3. A* with Manhattan distance heuristic\n')#choosing the algorithm.
    
    queueing_function = int(algorithm)

    print(search(puzzle, queueing_function))#Passing the puzzle and queueing_function as input for search function.
    
    
#node data structure.The node has total of 8 attributes,four attributes for directions based on zero tile,three attributes for calculating cost    
class node:
    def __init__(self,puzzle):
        self.puzzle=puzzle
        self.depth=0
        self.hcost=0
        self.fcost=0
        self.move_up=None
        self.move_down=None
        self.move_left=None
        self.move_right=None
    
# Main driver Program
def search(problem,queueing_function):

    # storing the start time
    start_time = time.time()
    queue=[]
    nodes_count = 0  #keeps count of expanded nodes
    visited= []      #keeps track of visited nodes
    size_of_queue = 0 
    max_queue = 0    #The maximum no.of nodes in queue at once.

    if queueing_function == 1: #performs uniform cost search
        h_cost= 0              #h(n)=0 for uniform cost search.
        
    if queueing_function == 2: #performs A* with Heuristic as misplaced tiles
        h_cost = misplaced_tiles(problem) #h(n) is calculated from misplaced tiles heuristic function.
        
    if queueing_function == 3: #performs A* with Heuristic as manhattan distance
        h_cost = manhattan_distance(problem) #h(n) is calculated from manhattan heuristic function.
        
    
    current_node= node(problem)       #This is the starting node i.e initial state of problem.
    current_node.depth = 0            #Depth of current node i.e g(n)
    current_node.hcost = h_cost        #heuristic cost of current node
    current_node.fcost=current_node.depth+current_node.hcost    #f(n) value of current node.
    queue.append(current_node)          #adding current_node to queue
    visited.append(current_node.puzzle) #adding the puzzle to visited list
    size_of_queue=size_of_queue+1       #increasing size of queue

    #we will run this loop until queue length is not zero.
    while queue:
        #sorting based on f(n) i.e g(n)+h(n)
        if queueing_function != 1:   #we don't need to sort for uniform search because h(n)=0
            #sorting based on the f(n) cost and depth,I used key parameter for fast sorting here 
            queue = sorted(queue, key=lambda curr_node: (curr_node.fcost, curr_node.depth))
            
        out_node = queue.pop(0) #removing the node from queue
        nodes_count = nodes_count+1
        size_of_queue = size_of_queue-1

        #checking whether out_node is goal_node or not.
        if goal(out_node.puzzle):
            return ( "Goal state is reached \n Total no.of nodes expanded is: {} \n maximum number of nodes in the queue at once is: {}.\n The depth of the goal node is: {} \nCPU Time:{}".format(nodes_count,max_queue,out_node.depth,(time.time()-start_time)))

        if goal(out_node.puzzle)==False:
            print("The best node to expand with a g(n) = {}  and h(n) = {} and f(n)= {} is \n {} \n".format(out_node.depth,out_node.hcost,out_node.fcost,out_node.puzzle))
            
            
        #expanding node that is popped off from queue
        expanded_node = expand(out_node,visited)
        #The popped off node is given as input to the expand function to get its possible children.
        #we store all the children nodes of the popped off node in this array
        children_nodes= [expanded_node.move_up, expanded_node.move_down, expanded_node.move_left, expanded_node.move_right]

        for children in children_nodes:
            if children != None:           #If children is not none we will find the f(n) cost for children node based on the queueing_function
                if queueing_function == 1:
                    children.depth = out_node.depth + 1
                    children.hcost = 0
                elif queueing_function == 2:
                    children.depth = out_node.depth + 1
                    children.hcost = misplaced_tiles(children.puzzle)
                elif queueing_function == 3:
                    children.depth = out_node.depth + 1
                    children.hcost = manhattan_distance(children.puzzle)
                children.fcost=children.hcost+children.depth #calculating fcost of children

                
                queue.append(children) #adding children to the queue
                visited.append(children.puzzle)
                size_of_queue=size_of_queue+1 #incrementing the size of queue

        
        if size_of_queue >max_queue:
            max_queue=size_of_queue #updating the max_queue
            
            
def expand(out_node,visited): #Giving popped node from queue and visited list of nodes as input. 
    row = 0
    column = 0
    # finding the indexes of 0 in the puzzle.
    for i in range(len(out_node.puzzle)):
        for j in range(len(out_node.puzzle)):
            if out_node.puzzle[i][j] == 0:
                row = i
                column = j
#If zero block is either in row1 or row2 then we can move the zero block upwards
    if row > 0:
        up = copy.deepcopy(out_node.puzzle)
        zero_value = up[row][column]
        up[row][column] = up[row - 1][column]     #interchanging the tiles
        up[row - 1][column] = zero_value
        if up not in visited:                     #checking whether the puzzle node is visited or not.
            out_node.move_up = node(up)           #adding up child to the parent node
            
    # If zero block is either in row0 or row1 then we can move the zero block downwards
    if row < 2:
        down = copy.deepcopy(out_node.puzzle)
        zero_value = down[row][column]
        down[row][column] = down[row + 1][column]   #interchanging the tiles
        down[row + 1][column] = zero_value
        if down not in visited:                    #checking whether the puzzle node is visited or not.
            out_node.move_down = node(down)        #adding down child to the parent node
            
    # If zero block is either in column1 or column2 then we can move zero block leftwards
    if column > 0:
        left = copy.deepcopy(out_node.puzzle)
        zero_value = left[row][column]
        left[row][column] = left[row][column - 1]   #interchanging the tiles
        left[row][column - 1] = zero_value
        if left not in visited:                   #checking whether the puzzle node is visited or not.
            out_node.move_left = node(left)       #adding left child to the parent node
            
     # If zero block is either in column0 or column1 then we can move zero block rightwards
    if column < 2:
        right = copy.deepcopy(out_node.puzzle)
        zero_value = right[row][column]
        right[row][column] = right[row][column+1]  #interchanging the tiles
        right[row][column+1] = zero_value
        if right not in visited:                  #checking whether the puzzle node is visited or not.
            out_node.move_right = node(right)     #adding right child to the parent node
            
    return out_node  #returning the parent node
            
goal_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
#function for calculating heuristic using misplaced_tiles
def misplaced_tiles(puzzle):
    h_cost = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] != goal_puzzle[i][j] and puzzle[i][j]!= 0:
                h_cost += 1
    return h_cost

#function for calculating heuristic using manhattan_distance
def manhattan_distance(puzzle):
    h_cost= 0
    num=1
    while(num<9):
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                if puzzle[i][j] == num:
                    row = i
                    column = j
                if goal_puzzle[i][j] == num:
                    goal_row = i
                    goal_column = j
        h_cost += abs(goal_row-row) + abs(goal_column-column)
        num=num+1
    return h_cost
#function for checking whether the node is goal state or not
def goal(puzzle):
    if puzzle == goal_puzzle:
        return True
    return False

if __name__ == "__main__":
    main()

