import copy
import sys

class block:
    
    def __init__(self, block_id, property_name = None, value_string = None):                             
        self.block_id = block_id
        self.property_name = property_name
        self.value_string = value_string
        self.on_top_of = None
        self.side_by_side = []
        self.below_of = None
        
    def __lt__(self, other):
         return self.block_id < other.block_id
        
    def __eq__(self, other):
        if(other == "table" or other == None):
            return False
        else:
            return self.block_id == other.block_id and ((self.on_top_of.block_id if self.on_top_of != None else None) == \
            (other.on_top_of.block_id if other.on_top_of != None else None)) and \
            [x.block_id for x in self.side_by_side] == [x.block_id for x in other.side_by_side]
        
    def __ne__(self, other):
        if(other == "table" or other == None):
            return True
        else:
            return self.block_id != other.block_id and ((self.on_top_of.block_id if self.on_top_of != None else None) !=  \
            (other.on_top_of.block_id if other.on_top_of != None else None)) and \
            [x.block_id for x in self.side_by_side] != [x.block_id for x in other.side_by_side]
    
    def set_on_top_of(self, block_one):
        if(self.on_top_of == None):
            self.on_top_of = block_one
            block_one.below_of = self
        else:
            print("Only one block can be placed on top of a block")
            
    def set_side_by_side(self, block_one):
        if(block_one in self.side_by_side):
            print(block_one.block_id + " is already side by side with " + self.block_id)
        else:
            self.side_by_side.append(block_one)
            self.side_by_side = sorted(self.side_by_side)
            
    def remove_on_top_of(self):
        self.on_top_of.below_of = None
        self.on_top_of = None
        
    def remove_side_by_side(self):
        for w in self.side_by_side:
            w.side_by_side.remove(self)
        self.side_by_side = []
        
    def __repr__(self):
        return "{" + self.block_id + ", (" + ("None", self.property_name)[self.property_name != None] + ": " + \
        ("None", self.value_string)[self.value_string != None] + "), (on-top-of: " + \
        ("None" if self.on_top_of == None else self.on_top_of.block_id) + "), (side-by-side: " + \
        str([x.block_id for x in self.side_by_side]) + ")}\n"
        
    def __str__(self):
        return "{" + self.block_id + ", (" + ("None", self.property_name)[self.property_name != None] + ": " + \
        ("None", self.value_string)[self.value_string != None] + "), (on-top-of: " + \
        ("None" if self.on_top_of == None else self.on_top_of.block_id) + "), (side-by-side: " + \
        str([x.block_id for x in self.side_by_side]) + ")}\n"
    
    
def slide_to(block_one, block_two, command = True):
    if(slide_to_check(block_one, block_two, command, True)):
        z = block_one
        if(command):block_one.remove_side_by_side()
        while(z.on_top_of != None and command):
            z = z.on_top_of
            z.remove_side_by_side()
        block_one.set_side_by_side(block_two)
        block_two.set_side_by_side(block_one)
        x = block_one
        y = block_two
        
        while(x.on_top_of != None and y.on_top_of != None):
            x = x.on_top_of
            y = y.on_top_of
            x.set_side_by_side(y)
            y.set_side_by_side(x)

            
def slide_to_check(block_one, block_two, command = True, verbose = False):
    if((block_one.below_of != None) and command):
        if(verbose): print(block_one.block_id + " height is not zero")
        return False
    elif((block_two.below_of != None) and command):
        if(verbose): print(block_two.block_id + " height is not zero")
        return False
    elif(len(block_two.side_by_side) >= 4):
        if(verbose): print(block_one.block_id + " already has four block side-by-side with it")
        return False
    elif(block_one in block_two.side_by_side):
        if(verbose): print(block_one.block_id + " is already side by side with " + block_two.block_id)
        return False
    else:
        return True

    
def stack(block_one, block_two, command = True):
    if(block_one.on_top_of != None and command):
        print(block_one.block_id + " already has a block on top of it")
    elif(block_two == "table" or block_two == None):
        block_one.remove_side_by_side()
        if(block_one.below_of != None): block_one.below_of.on_top_of = None
        block_one.below_of = None
        a = block_one
    elif(block_two.on_top_of != None and command):
        print(block_two.block_id + " already has a block on top of it")
    else:
        if(block_one.below_of != None): block_one.below_of.on_top_of = None
        block_one.remove_side_by_side()
        block_one.below_of = block_two
        block_two.on_top_of = block_one
        if(len(block_two.side_by_side) > 0):
            for z in block_two.side_by_side:
                x = z
                y = block_two
                while(x.on_top_of != None and y.on_top_of != None):
                    x = x.on_top_of
                    y = y.on_top_of
                    x.set_side_by_side(y)
                    y.set_side_by_side(x)
                    
def actions(state):
    actions = []
    slides = []
    stacks = []
    for indz, z in enumerate(state):
        if(z.on_top_of == None and (len(z.side_by_side) != 0 or z.below_of != None)):
            
            actions.append(("stack", (indz, z.block_id), None))
    for indx, x in enumerate(state):
        for indy, y in enumerate(state):
            if(x.block_id != y.block_id):
                if(slide_to_check(x, y) == True and (len(x.side_by_side) > 0 or len(y.side_by_side) > 0)):
                    slides.append(("slide-to", (indx, x.block_id), (indy, y.block_id)))
                if(slide_to_check(x, y) == True and (len(x.side_by_side) == 0 and len(y.side_by_side) == 0) and x < y):
                    slides.append(("slide-to", (indx, x.block_id), (indy, y.block_id)))
                if(x.on_top_of == None and y.on_top_of == None):
                    stacks.append(("stack", (indx, x.block_id), (indy, y.block_id)))
    
    return actions + slides + stacks


def take_action(state, action):
    newState = copy.deepcopy(state)
    if(action[0] == "slide-to"):
        slide_to(newState[action[1][0]], newState[action[2][0]])
    if(action[0] == "stack"):
        stack(newState[action[1][0]], newState[action[2][0]] if action[2] != None else None)
    return newState


def read_startState(file_name):
    f = list(open(file_name, "r"))
    state = []
    for x in f:
        if(len(x.split()) == 4):
            ary = x.replace("(", "").replace(")", "").split()
            if(ary[0] == "has"):
                new_block = block(ary[1], ary[2], ary[3])
                state.append(new_block)
    for y in f:
        if(len(y.split()) == 4):
            ary = y.replace("(", "").replace(")", "").split()
            if(ary[0] == "is"):
                list_one = [a for a in state if a.block_id == ary[1]]
                if(len(list_one) > 0):
                    block_one = list_one[0]
                else:
                    block_one = block(ary[1])
                    state.append(block_one)
                if(ary[2] == "table"):
                    block_two = None
                else:
                    list_two = [b for b in state if b.block_id == ary[2]]
                    if(len(list_two) > 0):
                        block_two = list_two[0]
                    else:
                        block_two = block(ary[2])
                        state.append(block_two)
                if(ary[3] == "on-top-of"):
                    stack(block_one, block_two, command = False)
                elif(ary[3] == "side-by-side"):
                    slide_to(block_one, block_two, command = False)
    return sorted(state)

def read_goalState(file_name):
    return list(open(file_name, "r"))

def check(state, goalState):
    for x in goalState:
        if(len(x.split()) == 4):
            ary = x.replace("(", "").replace(")", "").split()
            state_block_ids = [y.block_id for y in state]
            if(ary[0] == "has"):
                if(ary[1] not in state_block_ids):
                    return False
            if(ary[0] == "is"):
                if(ary[3] == "on-top-of"):
                    if(ary[2] == 'table' and (ary[1] not in state_block_ids)):
                        print("Block in goal isn't in state")
                        return False
                    elif((ary[2] not in state_block_ids) or (ary[1] not in state_block_ids)):
                        print("Block in goal isn't in state")
                        return False
                    if(ary[2] == 'table'):
                        for w in state:
                            if(w.block_id == ary[1] and w.below_of != None):
                                return False
                    else:
                        for z in state:
                            if(z.block_id == ary[2] and (z.on_top_of.block_id if z.on_top_of != None else None) != ary[1]):
                                return False

                if(ary[3] == "side-by-side"):
                    if((ary[2] not in state_block_ids) or (ary[1] not in state_block_ids)):
                        print("Block in goal isn't in state")
                        return False
                    for z in state:
                        if(z.block_id == ary[2] and (ary[1] not in [w.block_id for w in z.side_by_side])):
                            return False
    return True

def h_9(state, goal):
    cost = 0
    dic = {} 
    dic2 = {}
    for x in goalState:
        ary = x.replace("(", "").replace(")", "").split()
        if(len(x.split()) == 4):
            if(ary[0] == "is"):
                if(ary[3] == "on-top-of"):
                    block_one = next((g for g in state if g.block_id == ary[1]), None)
                    block_two = next((f for f in state if f.block_id == ary[2]), None)
                    if(dic2.get((ary[1], ary[2]), 0) == 0 and (block_one.below_of.block_id if block_one.below_of != None else None) != (ary[2] if ary[2] != 'table' else None)):
                        cost = cost + 1
                        dic2[(ary[1], block_one.below_of.block_id if block_one.below_of != None else None)] = 1
                        while(block_one.on_top_of != None and dic2.get((block_one.on_top_of.block_id, block_one.block_id), 0) == 0):
                            cost = cost + 1
                            dic2[(block_one.on_top_of.block_id, block_one.block_id)] = 1
                            block_one = block_one.on_top_of
                        while(block_two.on_top_of != None and dic2.get((block_two.on_top_of.block_id, block_two.block_id), 0) == 0):
                            cost = cost + 1
                            dic2[(block_two.on_top_of.block_id, block_two.block_id)] = 1
                            block_two = block_two.on_top_of
                        
    for x in goalState:
        ary = x.replace("(", "").replace(")", "").split()
        if(len(x.split()) == 4):
            if(ary[0] == "is"):
                if(ary[3] == "side-by-side"):
                    block_one = next((g for g in state if g.block_id == ary[1]), None)
                    block_two = next((f for f in state if f.block_id == ary[2]), None)
                    if(block_one.block_id not in [c.block_id for c in block_two.side_by_side]):
                        one = copy.deepcopy(block_one)
                        one_height = 0
                        two = copy.deepcopy(block_two)
                        two_height = 0
                        while(one.below_of != None):
                            one = one.below_of
                            one_height = one_height + 1
                        while(two.below_of != None):
                            two = two.below_of
                            two_height = two_height + 1
                        if(one_height != two_height):
                            cost = cost + 1
                            if(block_one.below_of != None and len(block_one.below_of.side_by_side) > 0):
                                cost = cost + 1
                            elif(block_two.below_of != None and len(block_two.below_of.side_by_side) > 0):
                                cost = cost + 1
                            one = copy.deepcopy(block_one)
                            two = copy.deepcopy(block_two)
                            while(one.on_top_of != None and two.on_top_of != None and dic2.get((one.on_top_of.block_id, one.block_id), 0) == 0 and dic2.get((two.on_top_of.block_id, two.block_id), 0) == 0):
                                cost = cost + 1
                                dic2[(one.on_top_of.block_id, one.block_id)] = 1
                                dic2[(two.on_top_of.block_id, two.block_id)] = 1
                                one = one.on_top_of
                                two = two.on_top_of
                        elif(dic.get((ary[1], ary[2]), 0) == 0 and dic.get((ary[2], ary[1]), 0) == 0):
                            cost = cost + 1
                            dic[(ary[1], ary[2])] = 1
                            a = copy.deepcopy(block_one)
                            b = copy.deepcopy(block_two)
                            while(a.on_top_of != None and b.on_top_of != None):
                                a = a.on_top_of
                                b = b.on_top_of
                                dic[(a.block_id, b.block_id)] = 1 
                            a = copy.deepcopy(block_one)
                            b = copy.deepcopy(block_two)
                            while(a.below_of != None and b.below_of != None):
                                a = a.below_of
                                b = b.below_of
                                dic[(a.block_id, b.block_id)] = 1
    for x in goalState:
        count = 0
        ary = x.replace("(", "").replace(")", "").split()
        if(len(x.split()) == 4):
            if(ary[0] == "is"):
                if(ary[3] == "side-by-side"):
                    for y in goalState:
                        ary2 = y.replace("(", "").replace(")", "").split()
                        if(len(y.split()) == 4):
                            if(ary2[0] == "is"):
                                if(ary2[3] == "on-top-of"):
                                    if(ary[1] == ary2[1] and ary[2] != ary2[1]):
                                        count = count + 1
                                        block_one = next((g for g in state if g.block_id == ary[2]), None)
                                    if(ary[1] != ary2[1] and ary[2] == ary2[1]):
                                        count = count + 1
                                        block_one = next((g for g in state if g.block_id == ary[1]), None)
                                    
                    if(count == 1 and (block_one.below_of == None)):
                        cost = cost + 1
                        while(block_one.on_top_of != None and dic2.get((block_one.on_top_of.block_id, block_one.block_id), 0) == 0):
                            cost = cost + 1
                            dic2[(block_one.on_top_of.block_id, block_one.block_id)] = 1
                            block_one = block_one.on_top_of
                    
                            
    return cost

class Node:
    def __init__(self, state, action, h=0, g=0 ,f=0):
        self.state = state
        self.action = action
        self.h = h
        self.g = g
        self.f = f
    def __repr__(self):
        return "Node(" + repr(self.state) + ", action=" + repr(self.action) + ", f=" + repr(self.f) + \
               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"
    def __str__(self):
        return "Node(" + repr(self.state) + ", action=" + repr(self.action) + ", f=" + repr(self.f) + \
               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"
    
def aStar(parentNode, goalState, actionsF, take_actionF, hF, fmax):
    if(check(parentNode.state, goalState)):
        return([parentNode.action], parentNode.g)
    actions = actionsF(parentNode.state)
    if not actions:
        return("no more moves", float("inf"))
    children = []
    for action in actions:
        childState = take_actionF(parentNode.state, action)
        h = hF(childState, goalState)
        g = parentNode.g + 1
        f = max(h+g, parentNode.f)
        childNode = Node(state=childState, action = action, h=h, g=g, f=f)
        children.append(childNode)
    while True:
        minChild = min(children, key = lambda x: x.f)
        if minChild.f > fmax:
            return ("max steps exceded", minChild.f)
        alternativef = minChild.f if len(children) > 1 else float('inf')
        print("depth " + str(minChild.g))
        print("heuristic " + str(minChild.h))
        result, minChild.f = aStar(minChild, goalState, actionsF, take_actionF, hF, min(fmax,alternativef))
        if result is not "no more moves" and result is not "max steps exceded":         
            result.insert(0, parentNode.action) 
            return (result, minChild.f) 
        
def aStarSearch(startState, goalState, actionsF, take_actionF, hF, fmax):
    return aStar(Node(state=startState, action=None, f=0, g=0, h=0), goalState, actionsF, take_actionF, hF, fmax) 

startState = read_startState(sys.argv[1]) #Input File
goalState = read_goalState(sys.argv[2]) #Output File
print(startState)
print()
answer = aStarSearch(startState, goalState, actions, take_action, h_9, 100)
if((answer[0] ==  "max steps exceded") or (answer[0] == "no more moves")):
    print(answer)
else:
    for a in answer[0][1::]:
        print("(" + str(a[0]) + ", " + str(a[1][1]) + ", " + (str(a[2][1]) if a[2] != None else "table") + ")")
    print(answer[1])