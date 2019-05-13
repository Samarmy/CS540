import copy
import sys

class block:
    
    def __init__(self, block_id, x, y, z, color = None):                             
        self.block_id = block_id
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.color = color
        self.top = None
        self.below = None
        self.sides = []
        self.grabbed = False
        
    def __lt__(self, other):
         return int(self.block_id[5:]) < int(other.block_id[5:])
        
    def __eq__(self, other):
        if(other == "table" or other == None):
            return False
        else:
            return self.block_id == other.block_id
        
    def __ne__(self, other):
        if(other == "table" or other == None):
            return True
        else:
            return self.block_id != other.block_id
        
    def set_top(self, block_one):
        if(self != block_one.top):
            if(self.below != None): self.below.top = None
            self.below = block_one
            block_one.top = self
    
    def remove_bottom(self):
        if(self.below != None): self.below.top = None
        self.below = None
    
    def add_side(self, block_one):
        if(self not in block_one.sides):
            self.sides.append(block_one)
            block_one.sides.append(self)
        
    def remove_sides(self):
        for s in self.sides:
            s.sides.remove(self)
        self.sides = []
        
    def __repr__(self):
        return "{" + self.block_id +", ("+str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "), (" + \
        "color: " + ("None", self.color)[self.color != None] + "), (on-top-of: " + \
        ("None" if self.top == None else self.top.block_id) + "), (side-by-side: " + \
        str([x.block_id for x in self.sides]) + ")}\n"
        
    def __str__(self):
        return "{" + self.block_id +", ("+str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "), (" + \
        "color: " + ("None", self.color)[self.color != None] + "), (on-top-of: " + \
        ("None" if self.top == None else self.top.block_id) + "), (side-by-side: " + \
        str([x.block_id for x in self.sides]) + ")}\n"
    
def grabbed(state):
    if(True in [x.grabbed for x in state]):
        return True
    return False

def find(x, y, z, state):
    return next((a for a in state if (a.x == int(x) and a.y == int(y) and a.z == int(z))), None)

def find2(block_id, state):
    return next((a for a in state if (a.block_id == block_id)), None)

def grab(block_one, state):
    if(grabbed(state)):
        print("Cannot grab! A block is already grabbed")
    elif(block_one.top != None):
        print("Cannot grab! " + block_one.block_id + " has a block on top of it")
    else:
        block_one.grabbed = True
        
def get_grabbed(state):
    for inds, s in enumerate(state):
        if(s.grabbed == True):
            return (inds, s)
    return (-1, None)

def release(block_one, state):
    if(block_one.grabbed == False):
        print("Cannot release! " + block_one.block_id + " is not currently grabbed")
    elif(block_one.z > 0 and (find(block_one.x, block_one.y, block_one.z - 1, state) == None)):
        print("Cannot release! There is no block underneath that spot")
    else:
        block_one.grabbed = False
        
def carry(block_one, deltax, deltay, deltaz, state):
    if(block_one.grabbed == False):
        print("Cannot carry! " + block_one.block_id + " is not currently grabbed")
    elif(find(block_one.x + deltax, block_one.y + deltay, block_one.z + deltaz, state) != None):
        print("Cannot carry " + block_one.block_id + "! There is already a block in spot " + str((block_one.x + deltax, block_one.y + deltay, block_one.z + deltaz)))
    else:
        block_one.x = block_one.x + deltax
        block_one.y = block_one.y + deltay
        block_one.z = block_one.z + deltaz
        block_one.remove_bottom()
        block_one.remove_sides()
        zdown = find(block_one.x, block_one.y, block_one.z - 1, state)
        xup = find(block_one.x + 1, block_one.y, block_one.z, state)
        xdown = find(block_one.x - 1, block_one.y, block_one.z, state)
        yup = find(block_one.x, block_one.y + 1, block_one.z, state)
        ydown = find(block_one.x, block_one.y - 1, block_one.z, state)
        if(zdown != None): block_one.set_top(zdown)
        if(xup != None): block_one.add_side(xup)
        if(xdown != None): block_one.add_side(xdown)
        if(yup != None): block_one.add_side(yup)
        if(ydown != None): block_one.add_side(ydown)
            
            
def slide(block_one, deltax, deltay, state):
    if(grabbed(state)):
        print("Cannot slide! A block is grabbed")
    elif(block_one.z != 0):
        print("Cannot slide! " + block_one.block_id + " is not at height 0")
    elif(find(block_one.x + deltax, block_one.y + deltay, block_one.z, state) != None):
        print("Cannot slide! There is already a block in spot " + str((block_one.x + deltax, block_one.y + deltay, block_one.z)))
    else:
        block_one.x = block_one.x + deltax
        block_one.y = block_one.y + deltay
        block_one.remove_sides()
        xup = find(block_one.x + 1, block_one.y, block_one.z, state)
        xdown = find(block_one.x - 1, block_one.y, block_one.z, state)
        yup = find(block_one.x, block_one.y + 1, block_one.z, state)
        ydown = find(block_one.x, block_one.y - 1, block_one.z, state)
        if(xup != None): block_one.add_side(xup)
        if(xdown != None): block_one.add_side(xdown)
        if(yup != None): block_one.add_side(yup)
        if(ydown != None): block_one.add_side(ydown)
        temp = block_one
        while(temp.top != None):
            temp = temp.top
            temp.x = temp.x + deltax
            temp.y = temp.y + deltay
            temp.remove_sides()
            xup = find(temp.x + 1, temp.y, temp.z, state)
            xdown = find(temp.x - 1, temp.y, temp.z, state)
            yup = find(temp.x, temp.y + 1, temp.z, state)
            ydown = find(temp.x, temp.y - 1, temp.z, state)
            if(xup != None): temp.add_side(xup)
            if(xdown != None): temp.add_side(xdown)
            if(yup != None): temp.add_side(yup)
            if(ydown != None): temp.add_side(ydown)
            
def actions_2(state):
    actions = []
    slides = [(-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0)]
    carries = [(-1,1,0), (0,1,0), (1,1,0), (1,0,0), (1,-1,0), (0,-1,0), (-1,-1,0), (-1,0,0), (-1,1,1), (0,1,1), (1,1,1), (1,0,1), (1,-1,1), (0,-1,1), (-1,-1,1), (-1,0,1), (0,0,1), (-1,1,-1), (0,1,-1), (1,1,-1), (1,0,-1), (1,-1,-1), (0,-1,-1), (-1,-1,-1), (-1,0,-1), (0,0,-1)]
    grabs = []
    if not(grabbed(state)):
        for inda, a in enumerate(state):
            if(a.z == 0):
                for s in slides:
                    if(9 >= a.x + s[0] >= 0 and 9 >= a.y + s[1] >= 0 and find(a.x + s[0], a.y + s[1], 0, state) == None):
                        actions.append(("slide", (inda, a.block_id), s))
        for inda, a in enumerate(state):
            if(a.top == None):
                grabs.append(("grab", (inda, a.block_id)))
    if(grabbed(state)):
        grabbed_block = get_grabbed(state)
        for c in carries:
                if(grabbed_block[1].z + c[2] >= 0 and 9 >= grabbed_block[1].x + c[0] >= 0 and 9 >= grabbed_block[1].y + c[1] >= 0 and find(grabbed_block[1].x + c[0], grabbed_block[1].y + c[1], grabbed_block[1].z + c[2], state) == None):
                    actions.append(("carry", (grabbed_block[0], grabbed_block[1].block_id), c))
        if(grabbed_block[1].z == 0 or grabbed_block[1].below != None):
            grabs.append(("release", (grabbed_block[0], grabbed_block[1].block_id)))
    return grabs + actions

def take_action_2(action, state):
    newState = copy.deepcopy(state)
    if(action[0] == "slide"):
        slide(newState[action[1][0]], action[2][0], action[2][1], newState)
    elif(action[0] == "release"):
        release(newState[action[1][0]], newState)
    elif(action[0] == "carry"):
        carry(newState[action[1][0]], action[2][0], action[2][1], action[2][2], newState)
    elif(action[0] == "grab"):
        grab(newState[action[1][0]], newState)
 
    return newState

def read_startState(file_name):
    f = list(open(file_name, "r"))
    state = []
    for x in f:
        if(len(x.split()) == 6):
            ary = x.replace("(", "").replace(")", "").split()
            if(ary[0] == "has"):
                new_block = block(ary[1], ary[3], ary[4], ary[5])
                state.append(new_block)
    for s in state:
        zup = find(s.x, s.y, s.z + 1, state)
        zdown = find(s.x, s.y, s.z - 1, state)
        xup = find(s.x + 1, s.y, s.z, state)
        xdown = find(s.x - 1, s.y, s.z, state)
        yup = find(s.x, s.y + 1, s.z, state)
        ydown = find(s.x, s.y - 1, s.z, state)
        if(zup != None): zup.set_top(s)
        if(zdown != None): s.set_top(zdown)
        if(xup != None): s.add_side(xup)
        if(xdown != None): s.add_side(xdown)
        if(yup != None): s.add_side(yup)
        if(ydown != None): s.add_side(ydown)
    for z in f:
        if(len(z.split()) == 4):
            ary = z.replace("(", "").replace(")", "").split()
            if(ary[0] == "has"):
                block_one = next((a for a in state if (a.block_id == ary[1])), None)
                block_one.color = ary[3]
                
    return sorted(state)

def read_goalState(file_name):
    return sorted(list(open(file_name, "r")))

def check(state, goalState):
    wildcards = {}
    for x in goalState:
        if(len(x.split()) == 4 or len(x.split()) == 6):
            ary = x.replace("(", "").replace(")", "").split()
            state_block_ids = [y.block_id for y in state]
            
            if(ary[0] == "has" and ary[1][:8] != "wildcard"):
                if(ary[1] not in state_block_ids):
                    print("Block in goal isn't in state")
                    return False
                if(len(x.split()) == 6):
                    temp = find(ary[3], ary[4], ary[5], state)
                    if(temp == None or temp.block_id != ary[1]):
                        return False
            if(ary[0] == "is" and ary[2][:8] != "wildcard" and ary[1][:8] != "wildcard"):
                if((ary[2] not in state_block_ids) or (ary[1] not in state_block_ids)):
                        print("Block in goal isn't in state")
                        return False
                if(ary[3] == "on-top-of"):
                        for z in state:
                            if(z.block_id == ary[2] and (z.top.block_id if z.top != None else None) != ary[1]):
                                return False

                if(ary[3] == "side-by-side"):
                    for z in state:
                        if(z.block_id == ary[2] and (ary[1] not in [w.block_id for w in z.sides])):
                            return False
                        
       
            if(ary[0] == "has" and ary[1][:8] == "wildcard"):
                if(len(x.split()) == 4):
                    no_color = True
                    for z in state:
                        if(z.color == ary[3]):
                            no_color = False
                            if(wildcards.get(ary[1], 0) == 0):
                                wildcards[ary[1]] = [z]
                            else:
                                wildcards[ary[1]].append(z)
                    if(no_color):
                        print("There is no block that is color " + ary[3])
                        return False
                if(len(x.split()) == 6):
                    temp = find(ary[3], ary[4], ary[5], state)
                    if(temp == None):
                        return False
                    elif(wildcards.get(ary[1], 0) == 0):
                        wildcards[ary[1]] = [temp]
                    else:
                        remove = []
                        for y in wildcards[ary[1]]:
                            if(y != temp):
                                remove = remove + [y]
                        for r in remove:
                            wildcards[ary[1]].remove(r)
                        if(wildcards.get(ary[1], 0) == 0 or len(wildcards[ary[1]]) == 0):
                            return False
            if(ary[0] == "is" and (ary[2][:8] == "wildcard" or ary[1][:8] == "wildcard")):
                if(ary[3] == "on-top-of" and ary[2][:8] != "wildcard"):
                    block_two = next((a for a in state if a.block_id == ary[2]), None)
                    if(block_two.top == None):
                        return False
                    elif(wildcards.get(ary[1], 0) == 0):
                        wildcards[ary[1]] = [block_two.top]
                    else:
                        remove = []
                        for w in wildcards[ary[1]]:
                            if(w.below != block_two):
                                remove = remove + [w]
                        for r in remove:
                            wildcards[ary[1]].remove(r)
                        if(wildcards.get(ary[1], 0) == 0 or len(wildcards[ary[1]]) == 0):
                            return False
                elif(ary[3] == "on-top-of" and ary[1][:8] != "wildcard"):
                    block_one = next((a for a in state if a.block_id == ary[1]), None)
                    if(block_one.below == None):
                        return False
                    elif(wildcards.get(ary[2], 0) == 0):
                        wildcards[ary[2]] = [block_one.below]
                    else:
                        remove = []
                        for w in wildcards[ary[2]]:
                            if(w.top != block_one):
                                remove = remove + [w]
                        for r in remove:
                            wildcards[ary[2]].remove(r)
                        if(wildcards.get(ary[2], 0) == 0 or len(wildcards[ary[2]]) == 0):
                            return False
                elif(ary[3] == "on-top-of"):
                    if(wildcards.get(ary[1], 0) == 0 and wildcards.get(ary[2], 0) == 0):
                        for v in state:
                            if(v.top != None):
                                if(wildcards.get(ary[1], 0) == 0): 
                                    wildcards[ary[1]] = [v.top]
                                else:
                                    wildcards[ary[1]].append(v.top)
                                if(wildcards.get(ary[2], 0) == 0): 
                                    wildcards[ary[2]] = [v]
                                else:
                                    wildcards[ary[2]].append(v)
                        if(wildcards.get(ary[1], 0) == 0 or wildcards.get(ary[2], 0) == 0 or len(wildcards[ary[2]]) == 0 or len(wildcards[ary[1]]) == 0):
                            return False
                    elif(wildcards.get(ary[2], 0) == 0):
                        remove = []
                        for w in wildcards[ary[1]]:
                            if(w.below == None):
                                remove = remove + [w]
                            else:
                                if(wildcards.get(ary[2], 0) == 0):
                                    wildcards[ary[2]] = [w.below]
                                else:
                                    wildcards[ary[2]].append(w.below)
                        for r in remove:
                            wildcards[ary[1]].remove(r)
                        if(wildcards.get(ary[1], 0) == 0 or wildcards.get(ary[2], 0) == 0 or len(wildcards[ary[2]]) == 0 or len(wildcards[ary[1]]) == 0):
                            return False
                    elif(wildcards.get(ary[1], 0) == 0):
                        remove = []
                        for w in wildcards[ary[2]]:
                            if(w.top == None):
                                remove = remove + [w]
                            else:
                                if(wildcards.get(ary[1], 0) == 0):
                                    wildcards[ary[1]] = [w.top]
                                else:
                                    wildcards[ary[1]].append(w.top)
                        for r in remove:
                            wildcards[ary[2]].remove(r)
                        if(wildcards.get(ary[1], 0) == 0 or wildcards.get(ary[2], 0) == 0 or len(wildcards[ary[2]]) == 0 or len(wildcards[ary[1]]) == 0):
                            return False  
                    else:
                        remove = []
                        for m in wildcards[ary[1]]:
                            not_related_1 = True
                            for n in wildcards[ary[2]]:
                                if(m.below == n):
                                    not_related_1 = False
                            if(not_related_1):
                                remove = remove + [m]
                        for r in  remove:
                            wildcards[ary[1]].remove(r)   
                            
                        remove = []
                        for m in wildcards[ary[2]]:
                            not_related_2 = True
                            for n in wildcards[ary[1]]:
                                if(m.top == n):
                                    not_related_2 = False
                            if(not_related_2):
                                remove = remove + [m]
                        for r in remove:
                            wildcards[ary[2]].remove(r)
                        if(wildcards.get(ary[1], 0) == 0 or wildcards.get(ary[2], 0) == 0 or len(wildcards[ary[2]]) == 0 or len(wildcards[ary[1]]) == 0):
                            return False



                elif(ary[3] == "side-by-side" and ary[2][:8] != "wildcard"):
                    block_two = next((a for a in state if a.block_id == ary[2]), None)
                    if(len(block_two.sides) == 0):
                        return False
                    elif(wildcards.get(ary[1], 0) == 0):
                        for j in block_two.sides:
                            if(wildcards.get(ary[1], 0) == 0):
                                wildcards[ary[1]] = [j]
                            else:
                                wildcards[ary[1]].append(j)
                        if(wildcards.get(ary[1], 0) == 0 or len(wildcards[ary[1]]) == 0):
                            return False
                    else:
                        remove = []
                        for w in wildcards[ary[1]]:
                            if(w not in block_two.sides):
                                remove = remove + [w]
                        for r in remove:
                            wildcards[ary[1]].remove(r)
                        if(wildcards.get(ary[1], 0) == 0 or len(wildcards[ary[1]]) == 0):
                            return False
                elif(ary[3] == "side-by-side" and ary[1][:8] != "wildcard"):
                    block_one = next((a for a in state if a.block_id == ary[1]), None)
                    if(len(block_one.sides) == 0):
                        return False
                    elif(wildcards.get(ary[2], 0) == 0):
                        for j in block_one.sides:
                            if(wildcards.get(ary[2], 0) == 0):
                                wildcards[ary[2]] = [j]
                            else:
                                wildcards[ary[2]].append(j)
                        if(wildcards.get(ary[2], 0) == 0 or len(wildcards[ary[2]]) == 0):
                                return False
                    else:
                        remove = []
                        for w in wildcards[ary[2]]:
                            if(w not in block_one.sides):
                                remove = remove + [w]
                        for r in remove:
                             wildcards[ary[2]].remove(2)
                        if(wildcards.get(ary[2], 0) == 0 or len(wildcards[ary[2]]) == 0):
                            return False
                elif(ary[3] == "side-by-side"):
                    if(wildcards.get(ary[1], 0) == 0 and wildcards.get(ary[2], 0) == 0):
                        for v in state:
                            if(len(v.sides) > 0):
                                if(wildcards.get(ary[1], 0) == 0): 
                                    wildcards[ary[1]] = [v]
                                else:
                                    wildcards[ary[1]].append(v)
                                for k in v.sides:
                                    if(wildcards.get(ary[2], 0) == 0): 
                                        wildcards[ary[2]] = [k]
                                    else:
                                        wildcards[ary[2]].append(k)
                        if(wildcards.get(ary[1], 0) == 0 or wildcards.get(ary[2], 0) == 0 or len(wildcards[ary[2]]) == 0 or len(wildcards[ary[1]]) == 0):
                            return False
                    elif(wildcards.get(ary[2], 0) == 0):
                        remove = []
                        for w in wildcards[ary[1]]:
                            if(len(w.sides) == 0):
                                remove = remove + [w] 
                            else:
                                for p in w.sides:
                                    if(wildcards.get(ary[2], 0) == 0):
                                        wildcards[ary[2]] = [p]
                                    else:
                                        wildcards[ary[2]].append(p)
                        for r in remove:
                            wildcards[ary[1]].remove(r)
                        if(wildcards.get(ary[1], 0) == 0 or wildcards.get(ary[2], 0) == 0 or len(wildcards[ary[2]]) == 0 or len(wildcards[ary[1]]) == 0):
                            return False
                    elif(wildcards.get(ary[1], 0) == 0):
                        remove = []
                        for w in wildcards[ary[2]]:
                            if(len(w.sides) == 0):
                                remove = remove + [w] 
                            else:
                                for p in w.sides:
                                    if(wildcards.get(ary[1], 0) == 0):
                                        wildcards[ary[1]] = [p]
                                    else:
                                        wildcards[ary[1]].append(p)
                        for r in remove:
                            wildcards[ary[2]].remove(r)
                        if(wildcards.get(ary[1], 0) == 0 or wildcards.get(ary[2], 0) == 0 or len(wildcards[ary[2]]) == 0 or len(wildcards[ary[1]]) == 0):
                            return False
                    else:
                        remove = []
                        for m in wildcards[ary[1]]:
                            not_related_1 = True
                            for n in wildcards[ary[2]]:
                                if(n in m.sides):
                                    not_related_1 = False
                            if(not_related_1):
                                remove = remove + [m]
                        for r in remove:
                            wildcards[ary[1]].remove(r)
                        remove = []
                        for m in wildcards[ary[2]]:
                            not_related_2 = True
                            for n in wildcards[ary[1]]:
                                if(n in m.sides):
                                    not_related_2 = False
                            if(not_related_2):
                                remove = remove + [m]
                        for r in remove:
                            wildcards[ary[2]].remove(r)
                        if(wildcards.get(ary[1], 0) == 0 or wildcards.get(ary[2], 0) == 0 or len(wildcards[ary[2]]) == 0 or len(wildcards[ary[1]]) == 0):
                            return False
    return True

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
    
class Node2:
    def __init__(self, state, action, moves, h=0, g=0 ,f=0):
        self.state = state
        self.action = action
        self.moves = moves
        self.h = h
        self.g = g
        self.f = f
    def __repr__(self):
        return "Node(" + repr(self.state) + ", action=" + repr(self.action) + ", moves" + repr(self.moves) + ", f=" + repr(self.f) + \
               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"
    def __str__(self):
        return "Node(" + repr(self.state) + ", action=" + repr(self.action) + ", moves" + repr(self.moves) + ", f=" + repr(self.f) + \
               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"
    
def aStarLow(parentNode, goalState, actionsF, take_actionF, hF, fmax):
    if(check(parentNode.state, goalState)):
        return([parentNode.action], parentNode.g, parentNode.state)
    actions = actionsF(parentNode.state)
    if not actions:
        return("no more moves", float("inf"))
    children = []
    for action in actions:
        childState = take_actionF(action, parentNode.state)
        h = hF(childState, goalState)
        g = parentNode.g + 1
        f = h+g
        childNode = Node(state=childState, action = action, h=h, g=g, f=f)
        children.append(childNode)
    while True:
        minChild = min(children, key = lambda x: x.f)
        if minChild.f > fmax:
            return ("max steps exceded", minChild.f,  parentNode.state)
        alternativef = minChild.f if len(children) > 1 else float('inf')
        result, minChild.f, parentState= aStarLow(minChild, goalState, actionsF, take_actionF, hF, min(fmax,alternativef))
        if result is not "no more moves" and result is not "max steps exceded":         
            result.insert(0, parentNode.action) 
            return (result, minChild.f, parentState) 
        
def aStarSearchLow(startState, goalState, actionsF, take_actionF, hF, fmax):
    answer = aStarLow(Node(state=startState, action=None, f=0, g=0, h=0), goalState, actionsF, take_actionF, hF, fmax)
    return answer

def h_5(startState, goalState):
    cost = 0
    wildcards = {}
    g = get_grabbed(startState)
    for x in goalState:
        if(len(x.split()) == 4 or len(x.split()) == 6):
            ary = x.replace("(", "").replace(")", "").split()
            if(ary[0] == "has" and ary[1][:8] == "wildcard"):
                if(len(x.split()) == 4):
                    for z in startState:
                        if(z.color == ary[3]):
                            if(wildcards.get(ary[1], 0) == 0):
                                wildcards[ary[1]] = [z]
                            else:
                                wildcards[ary[1]].append(z)
                
            if(ary[0] == "has" and ary[1][:8] != "wildcard" and len(x.split()) == 6):
                temp = copy.deepcopy(find2(ary[1], startState))
                blocker = find(ary[3], ary[4], ary[5], startState)
                cost = cost + max([abs(temp.x - int(ary[3])), abs(temp.y - int(ary[4])), abs(temp.z - int(ary[5]))])
                if(temp.z != int(ary[5])):
                    temp_1 = copy.deepcopy(temp)
                    while(temp_1.top != None):
                        temp_1 = temp_1.top
                        cost = cost + 1
                        if(temp_1 != g[1]):
                            cost = cost + 1
                    if(temp != blocker and g[1] != temp):
                            cost = cost + 1
                    if(blocker != None):
                        temp_2 = copy.deepcopy(blocker)
                        while(temp_2.top != None):
                            temp_2 = temp_2.top
                            cost = cost + 1
                            if(temp_2 != g[1]):
                                cost = cost + 1         
                        if(blocker != temp and g[1] != blocker):
                            cost = cost + 1
            if(ary[0] == "has" and ary[1][:8] == "wildcard" and len(x.split()) == 6):
                temp_2 = find(int(ary[3]), int(ary[4]), int(ary[5]), startState)
                if(wildcards.get(ary[1], 0) == 0):
                    for m in startState:
                        if(wildcards.get(ary[1], 0) == 0):
                            wildcards[ary[1]] = [m]
                        else:
                            wildcards[ary[1]].append(m)
                if(wildcards.get(ary[1], 0) != 0):
                    min_card = (None, 1000)
                    for w in wildcards[ary[1]]:
                        dif = max([abs(w.x - int(ary[3])), abs(w.y - int(ary[4])), abs(w.z - int(ary[5]))])
                        if(w.z != int(ary[5])):
                            temp = copy.deepcopy(w)
                            while(temp.top != None):
                                temp = temp.top
                                dif = dif + 1
                                if(temp != g[1]):
                                    dif = dif + 1
                            if(temp_2 != w and g[1] != w):
                                    dif = dif + 1
                            if(temp_2 != None):
                                temp2 = copy.deepcopy(temp_2)
                                while(temp2.top != None):
                                    temp2 = temp2.top
                                    dif = dif + 1
                                    if(temp2 != g[1]):
                                        dif = dif + 1         
                                if(temp_2 != w and g[1] != temp_2):
                                    dif = dif + 1
                        if(min_card[1] > dif):
                            min_card = (w, dif)
                    cost = cost + min_card[1]                                
            if(ary[0] == "is" and ary[1][:8] != "wildcard" and ary[2][:8] != "wildcard"):
                block_one = copy.deepcopy(find2(ary[1], startState))
                block_two = copy.deepcopy(find2(ary[2], startState))
                block_a = copy.deepcopy(find2(ary[1], startState))
                block_b = copy.deepcopy(find2(ary[2], startState))
                if(ary[3] == "on-top-of"):
                    dif = max([abs(block_one.x - block_two.x), abs(block_one.y - block_two.y), abs(block_one.z - 1 - block_two.z)])
                    if(block_two.top != block_one):
                        while(block_one.top != None):
                            block_one = block_one.top
                            dif = dif + 1
                            if(block_one != g[1]):
                                dif = dif + 1
                        while(block_two.top != None):
                            block_two = block_two.top
                            dif = dif + 1
                            if(block_two != g[1]):
                                dif = dif + 1
                    blocker = block_two.top
                    if(blocker != block_one and get_grabbed(startState)[1] != block_one and blocker != None):
                        dif = dif + 1
                            
                else:
                    dif1 = max([abs(block_one.x + 1 - block_two.x), abs(block_one.y - block_two.y), abs(block_one.z - block_two.z)])
                    dif2 = max([abs(block_one.x - 1 - block_two.x), abs(block_one.y - block_two.y), abs(block_one.z - block_two.z)])
                    dif3 = max([abs(block_one.x - block_two.x), abs(block_one.y + 1 - block_two.y), abs(block_one.z - block_two.z)])
                    dif4 = max([abs(block_one.x - block_two.x), abs(block_one.y - 1 - block_two.y), abs(block_one.z - block_two.z)])
                    dif = min([dif1, dif2, dif3, dif4])
                    if(block_one.z != block_two.z):
                        while(block_one.top != None and block_two.top != None):
                            block_one = block_one.top
                            block_two = block_two.top
                            dif = dif + 1
                            if(block_one != g[1] or block_two != g[1]):
                                dif = dif + 1
                    if(block_a.z != block_b.z and (g[1] != block_a or g[1] != block_b )):
                        dif = dif + 2
                cost = cost + dif                              
            if(ary[0] == "is" and ary[1][:8] == "wildcard" and ary[2][:8] != "wildcard"):
                block_two = find2(ary[2], startState)
                if(wildcards.get(ary[1], 0) == 0):
                    for m in startState:
                        if(m != block_two):
                            if(wildcards.get(ary[1], 0) == 0):
                                wildcards[ary[1]] = [m]
                            else:
                                wildcards[ary[1]].append(m)
                min_card = (None, 1000)
                for w in wildcards[ary[1]]:
                    if(ary[3] == "on-top-of"):
                        dif = max([abs(w.x - block_two.x), abs(w.y - block_two.y), abs(w.z - 1 - block_two.z)])
                        if(block_two.top != w):
                            temp_1 = copy.deepcopy(w)
                            temp_2 = copy.deepcopy(block_two)
                            while(temp_1.top != None):
                                temp_1 = temp_1.top
                                dif = dif + 1
                            while(temp_2.top != None):
                                temp_2 = temp_2.top
                                dif = dif + 1
                            blocker = block_two.top
                            if(blocker != w and get_grabbed(startState)[1] != w and blocker != None):
                                dif = dif + 1
                    else:
                        dif1 = max([abs(w.x + 1 - block_two.x), abs(w.y - block_two.y), abs(w.z - block_two.z)])
                        dif2 = max([abs(w.x - 1 - block_two.x), abs(w.y - block_two.y), abs(w.z - block_two.z)])
                        dif3 = max([abs(w.x - block_two.x), abs(w.y + 1 - block_two.y), abs(w.z - block_two.z)])
                        dif4 = max([abs(w.x - block_two.x), abs(w.y - 1 - block_two.y), abs(w.z - block_two.z)])
                        dif = min([dif1, dif2, dif3, dif4])
                        if(w.z != block_two.z):
                            temp_1 = copy.deepcopy(w)
                            temp_2 = copy.deepcopy(block_two)
                            while(temp_1.top != None and temp_2.top != None):
                                temp_1 = temp_1.top
                                temp_2 = temp_2.top
                                dif = dif + 1
                                if(temp_2 != g[1] or temp_1 != g[1]):
                                    dif = dif + 1
                    if(min_card[1] > dif):
                        min_card = (w, dif)

                cost = cost + min_card[1]                            
            if(ary[0] == "is" and ary[1][:8] != "wildcard" and ary[2][:8] == "wildcard"):
                block_one = find2(ary[1], startState)
                if(wildcards.get(ary[2], 0) == 0):
                    for m in startState:
                        if(m != block_one):
                            if(wildcards.get(ary[2], 0) == 0):
                                wildcards[ary[2]] = [m]
                            else:
                                wildcards[ary[2]].append(m)
                min_card = (None, 1000)
                for w in wildcards[ary[2]]:
                    if(w != block_one):
                        if(ary[3] == "on-top-of"):
                            dif = max([abs(block_one.x - w.x), abs(block_one.y - w.y), abs(block_one.z - 1 - w.z)])
                            if(block_one.below != w):
                                temp_1 = copy.deepcopy(block_one)
                                temp_2 = copy.deepcopy(w)
                                while(temp_1.top != None):
                                    temp_1 = temp_1.top
                                    dif = dif + 1
                                    if(temp_1 != g[1]):
                                        dif = dif + 1
                                while(temp_2.top != None):
                                    temp_2 = temp_2.top
                                    dif = dif + 1
                                    if(temp_2 != g[1]):
                                        dif = dif + 1
                                blocker = w.top
                                if(blocker != block_one and get_grabbed(startState)[1] != block_one and blocker != None):
                                    dif = dif + 1
                        else:
                            dif1 = max([abs(block_one.x + 1 - w.x), abs(block_one.y - w.y), abs(block_one.z - w.z)])
                            dif2 = max([abs(block_one.x - 1 - w.x), abs(block_one.y - w.y), abs(block_one.z - w.z)])
                            dif3 = max([abs(block_one.x - w.x), abs(block_one.y + 1 - w.y), abs(block_one.z - w.z)])
                            dif4 = max([abs(block_one.x - w.x), abs(block_one.y - 1 - w.y), abs(block_one.z - w.z)])
                            dif = min([dif1, dif2, dif3, dif4])
                            if(w.z != block_one.z):
                                temp_1 = copy.deepcopy(w)
                                temp_2 = copy.deepcopy(block_one)
                                while(temp_1.top != None and temp_2.top != None):
                                    temp_1 = temp_1.top
                                    temp_2 = temp_2.top
                                    dif = dif + 1
                                    if(temp_2 != g[1] or temp_1 != g[1]):
                                        dif = dif + 1
                        if(min_card[1] > dif):
                            min_card = (w, dif)
                cost = cost + min_card[1]
                            
            if(ary[0] == "is" and ary[1][:8] == "wildcard" and ary[2][:8] == "wildcard"):
                if(wildcards.get(ary[1], 0) == 0):
                    for m in startState:
                        if(wildcards.get(ary[1], 0) == 0):
                            wildcards[ary[1]] = [m]
                        else:
                            wildcards[ary[1]].append(m)
                if(wildcards.get(ary[2], 0) == 0):
                    for m in startState:
                        if(wildcards.get(ary[2], 0) == 0):
                            wildcards[ary[2]] = [m]
                        else:
                            wildcards[ary[2]].append(m)
                min_card = (None, None, 1000)
                for w in wildcards[ary[1]]:
                    for v in wildcards[ary[2]]:
                        if(v != w):
                            if(ary[3] == "on-top-of"):
                                dif = max([abs(w.x - v.x), abs(w.y - v.y), abs(w.z - 1 - v.z)])
                                if(v.top != w):
                                    temp_1 = copy.deepcopy(w)
                                    temp_2 = copy.deepcopy(v)
                                    while(temp_1.top != None):
                                        temp_1 = temp_1.top
                                        dif = dif + 1
                                        if(temp_1 != g[1]):
                                            dif = dif + 1
                                    while(temp_2.top != None):
                                        temp_2 = temp_2.top
                                        dif = dif + 1
                                        if(temp_2 != g[1]):
                                            dif = dif + 1
                                blocker = v.top
                                if(blocker != w and g[1] != w and blocker != None):
                                    dif = dif + 1
                            else:
                                dif1 = max([abs(w.x + 1 - v.x), abs(w.y - v.y), abs(w.z - v.z)])
                                dif2 = max([abs(w.x - 1 - v.x), abs(w.y - v.y), abs(w.z - v.z)])
                                dif3 = max([abs(w.x - v.x), abs(w.y + 1 - v.y), abs(w.z - v.z)])
                                dif4 = max([abs(w.x - v.x), abs(w.y - 1 - v.y), abs(w.z - v.z)])
                                dif = min([dif1, dif2, dif3, dif4])
                                if(w.z != v.z):
                                    temp_1 = copy.deepcopy(w)
                                    temp_2 = copy.deepcopy(v)
                                    while(temp_1.top != None and temp_2.top != None):
                                        temp_1 = temp_1.top
                                        temp_2 = temp_2.top
                                        dif = dif + 1
                                        if(temp_2 != g[1] or temp_1 != g[1]):
                                            dif = dif + 1
                            if(min_card[2] > dif):
                                min_card = (w, v, dif)
                
                cost = cost + min_card[2]
    return cost

def actions_H(startState, goalState):
    cost = 0
    colors = []
    actions = []
    dont = []
    sides = []
    wildcards = {}
    g = get_grabbed(startState)
    for x in goalState:
        if(len(x.split()) == 4 or len(x.split()) == 6):
            ary = x.replace("(", "").replace(")", "").split()
            if(ary[0] == "has" and ary[1][:8] == "wildcard"):
                if(len(x.split()) == 4):
                    colors.append(x)
                    for z in startState:
                        if(z.color == ary[3]):
                            if(wildcards.get(ary[1], 0) == 0):
                                wildcards[ary[1]] = [z]
                            else:
                                wildcards[ary[1]].append(z)
                                
                    
    for x in goalState:
        action = []
        cost = 0
        if(len(x.split()) == 4 or len(x.split()) == 6):
            ary = x.replace("(", "").replace(")", "").split()
            if(ary[0] == "has" and ary[1][:8] != "wildcard" and len(x.split()) == 6):
                temp_1 = find2(ary[1], startState)
                temp_2 = find(int(ary[3]), int(ary[4]), int(ary[5]), startState)
                dont.append(ary[1])
                if(temp_1 != temp_2):
                    if(temp_1.z != int(ary[5]) and temp_1.top != None):
                        action.append("move " + temp_1.block_id + " remove-top")
                    if(temp_2 != None and temp_2.below != None):
                        action.append("move " + temp_2.below.block_id + " remove-top")
                    action.append(x)
            if(ary[0] == "has" and ary[1][:8] == "wildcard" and len(x.split()) == 6):
                temp_2 = find(int(ary[3]), int(ary[4]), int(ary[5]), startState)
                if(wildcards.get(ary[1], 0) == 0):
                    for m in startState:
                        if(wildcards.get(ary[1], 0) == 0):
                            wildcards[ary[1]] = [m]
                        else:
                            wildcards[ary[1]].append(m)
                if(wildcards.get(ary[1], 0) != 0):
                    min_card = (None, 1000)
                    for w in wildcards[ary[1]]:
                        dif = max([abs(w.x - int(ary[3])), abs(w.y - int(ary[4])), abs(w.z - int(ary[5]))])
                        if(w.z != int(ary[5])):
                            temp = copy.deepcopy(w)
                            while(temp.top != None):
                                temp = temp.top
                                dif = dif + 1
                                if(temp != g[1]):
                                    dif = dif + 1
                            if(temp_2 != w and g[1] != w):
                                    dif = dif + 1
                            if(temp_2 != None):
                                temp2 = copy.deepcopy(temp_2)
                                while(temp2.top != None):
                                    temp2 = temp2.top
                                    dif = dif + 1
                                    if(temp2 != g[1]):
                                        dif = dif + 1         
                                if(temp_2 != w and g[1] != temp_2):
                                    dif = dif + 1                                     
                        if(min_card[1] > dif):
                            min_card = (w, dif)
                    dont.append(ary[1])
                    if(temp_2 != min_card[0]):
                        if(min_card[0].z != int(ary[5]) and min_card[0].top != None):
                            action.append("move " + min_card[0].block_id + " remove-top")
                        if(temp_2 != None and temp_2.below != None):
                            action.append("move " + temp_2.below.block_id + " remove-top")
                        action.append(x) 
            if(ary[0] == "is" and ary[1][:8] != "wildcard" and ary[2][:8] != "wildcard"):
                block_one = find2(ary[1], startState)
                block_two = find2(ary[2], startState)
                dont.append(block_one.block_id)
                dont.append(block_two.block_id)
                if(ary[3] == "side-by-side" and block_two not in block_one.sides):
                    if(block_two.z != block_one.z and block_one.top != None):
                        action.append("move " + block_one.block_id + " remove-top")
                    if(block_two.z != block_one.z and block_two.top != None):
                        action.append("move " + block_two.block_id + " remove-top")
                    if(block_two.z != block_one.z and block_two.below != None and len(block_two.below.sides) == 0 and block_one.below != None and len(block_one.below.sides) == 0):
                        if(block_two.z > block_one.z):
                            action.append("move " + block_one.block_id + " find-stack")
                        else:
                            action.append("move " + block_two.block_id + " find-stack")                            
                    action.append(x)


                if(ary[3] == "on-top-of" and block_one.below != block_two):
                    if(block_one.top != None):
                        action.append("move " + block_one.block_id + " remove-top")
                    if(block_two.top != None):
                        action.append("move " + block_two.block_id + " remove-top")
                    action.append(x)
                                            
            if(ary[0] == "is" and ary[1][:8] == "wildcard" and ary[2][:8] != "wildcard"):
                block_two = find2(ary[2], startState)
                if(wildcards.get(ary[1], 0) == 0):
                    for m in startState:
                        if(m != block_two):
                            if(wildcards.get(ary[1], 0) == 0):
                                wildcards[ary[1]] = [m]
                            else:
                                wildcards[ary[1]].append(m)
                min_card = (None, 1000)
                for w in wildcards[ary[1]]:
                    if(ary[3] == "on-top-of"):
                        dif = max([abs(w.x - block_two.x), abs(w.y - block_two.y), abs(w.z - 1 - block_two.z)])
                        if(block_two.top != w):
                            temp_1 = copy.deepcopy(w)
                            temp_2 = copy.deepcopy(block_two)
                            while(temp_1.top != None):
                                temp_1 = temp_1.top
                                dif = dif + 1
                            while(temp_2.top != None):
                                temp_2 = temp_2.top
                                dif = dif + 1
                            blocker = block_two.top
                            if(blocker != w and get_grabbed(startState)[1] != w and blocker != None):
                                dif = dif + 1
                    else:
                        dif1 = max([abs(w.x + 1 - block_two.x), abs(w.y - block_two.y), abs(w.z - block_two.z)])
                        dif2 = max([abs(w.x - 1 - block_two.x), abs(w.y - block_two.y), abs(w.z - block_two.z)])
                        dif3 = max([abs(w.x - block_two.x), abs(w.y + 1 - block_two.y), abs(w.z - block_two.z)])
                        dif4 = max([abs(w.x - block_two.x), abs(w.y - 1 - block_two.y), abs(w.z - block_two.z)])
                        dif = min([dif1, dif2, dif3, dif4])
                        if(w.z != block_two.z):
                            temp_1 = copy.deepcopy(w)
                            temp_2 = copy.deepcopy(block_two)
                            while(temp_1.top != None and temp_2.top != None):
                                temp_1 = temp_1.top
                                temp_2 = temp_2.top
                                dif = dif + 1
                                if(temp_2 != g[1] or temp_1 != g[1]):
                                    dif = dif + 1
                    if(min_card[1] > dif):
                        min_card = (w, dif)
                dont.append(min_card[0].block_id)
                dont.append(block_two.block_id)
                if(ary[3] == "side-by-side" and block_two not in min_card[0].sides):
                    if(block_two.z != min_card[0].z and min_card[0].top != None):
                        action.append("move " + min_card[0].block_id + " remove-top")
                    if(block_two.z != min_card[0].z and block_two.top != None):
                        action.append("move " + block_two.block_id + " remove-top")
                    if(block_two.z != min_card[0].z and block_two.below != None and len(block_two.below.sides) == 0 and min_card[0].below != None and len(min_card[0].below.sides) == 0):
                        if(block_two.z > min_card[0].z):
                            action.append("move " + min_card[0].block_id + " find-stack")
                        else:
                            action.append("move " + block_two.block_id + " find-stack")                            
                    action.append(ary[0] + " " + block_two.block_id + " " + min_card[0].block_id + " side-by-side")


                if(ary[3] == "on-top-of" and min_card[0].below != block_two):
                    if(min_card[0].top != None):
                        action.append("move " + min_card[0].block_id + " remove-top")
                    if(block_two.top != None):
                        action.append("move " + block_two.block_id + " remove-top")
                    action.append(ary[0] + " " + min_card[0].block_id + " " +  block_two.block_id + " on-top-of")
                                         
            if(ary[0] == "is" and ary[1][:8] != "wildcard" and ary[2][:8] == "wildcard"):
                block_one = find2(ary[1], startState)
                if(wildcards.get(ary[2], 0) == 0):
                    for m in startState:
                        if(m != block_one):
                            if(wildcards.get(ary[2], 0) == 0):
                                wildcards[ary[2]] = [m]
                            else:
                                wildcards[ary[2]].append(m)
                min_card = (None, 1000)
                for w in wildcards[ary[2]]:
                    if(w != block_one):
                        if(ary[3] == "on-top-of"):
                            dif = max([abs(block_one.x - w.x), abs(block_one.y - w.y), abs(block_one.z - 1 - w.z)])
                            if(block_one.below != w):
                                temp_1 = copy.deepcopy(block_one)
                                temp_2 = copy.deepcopy(w)
                                while(temp_1.top != None):
                                    temp_1 = temp_1.top
                                    dif = dif + 1
                                    if(temp_1 != g[1]):
                                        dif = dif + 1
                                while(temp_2.top != None):
                                    temp_2 = temp_2.top
                                    dif = dif + 1
                                    if(temp_2 != g[1]):
                                        dif = dif + 1
                                blocker = w.top
                                if(blocker != block_one and get_grabbed(startState)[1] != block_one and blocker != None):
                                    dif = dif + 1
                        else:
                            dif1 = max([abs(block_one.x + 1 - w.x), abs(block_one.y - w.y), abs(block_one.z - w.z)])
                            dif2 = max([abs(block_one.x - 1 - w.x), abs(block_one.y - w.y), abs(block_one.z - w.z)])
                            dif3 = max([abs(block_one.x - w.x), abs(block_one.y + 1 - w.y), abs(block_one.z - w.z)])
                            dif4 = max([abs(block_one.x - w.x), abs(block_one.y - 1 - w.y), abs(block_one.z - w.z)])
                            dif = min([dif1, dif2, dif3, dif4])
                            if(w.z != block_one.z):
                                temp_1 = copy.deepcopy(w)
                                temp_2 = copy.deepcopy(block_one)
                                while(temp_1.top != None and temp_2.top != None):
                                    temp_1 = temp_1.top
                                    temp_2 = temp_2.top
                                    dif = dif + 1
                                    if(temp_2 != g[1] or temp_1 != g[1]):
                                        dif = dif + 1
                        if(min_card[1] > dif):
                            min_card = (w, dif)
                dont.append(block_one.block_id)
                dont.append(min_card[0].block_id)
                if(ary[3] == "side-by-side" and min_card[0] not in block_one.sides):
                    if(min_card[0].z != block_one.z and block_one.top != None):
                        action.append("move " + block_one.block_id + " remove-top")
                    if(min_card[0].z != block_one.z and min_card[0].top != None):
                        action.append("move " + min_card[0].block_id + " remove-top")
                    if(min_card[0].z != block_one.z and min_card[0].below != None and len(min_card[0].below.sides) == 0 and block_one.below != None and len(block_one.below.sides) == 0):
                        if(min_card[0].z > block_one.z):
                            action.append("move " + block_one.block_id + " find-stack")
                        else:
                            action.append("move " + min_card[0].block_id + " find-stack")                            
                    action.append(ary[0] + " " + min_card[0].block_id + " " + block_one.block_id + " side-by-side")


                if(ary[3] == "on-top-of" and block_one.below != min_card[0]):
                    if(block_one.top != None):
                        action.append("move " + block_one.block_id + " remove-top")
                    if(min_card[0].top != None):
                        action.append("move " + min_card[0].block_id + " remove-top")
                    action.append(ary[0] + " " + block_one.block_id + " " +  min_card[0].block_id + " on-top-of")
                            
            if(ary[0] == "is" and ary[1][:8] == "wildcard" and ary[2][:8] == "wildcard"):
                if(wildcards.get(ary[1], 0) == 0):
                    for m in startState:
                        if(wildcards.get(ary[1], 0) == 0):
                            wildcards[ary[1]] = [m]
                        else:
                            wildcards[ary[1]].append(m)
                if(wildcards.get(ary[2], 0) == 0):
                    for m in startState:
                        if(wildcards.get(ary[2], 0) == 0):
                            wildcards[ary[2]] = [m]
                        else:
                            wildcards[ary[2]].append(m)
                min_card = (None, None, 1000)
                for w in wildcards[ary[1]]:
                    for v in wildcards[ary[2]]:
                        if(v != w):
                            if(ary[3] == "on-top-of"):
                                dif = max([abs(w.x - v.x), abs(w.y - v.y), abs(w.z - 1 - v.z)])
                                if(v.top != w):
                                    temp_1 = copy.deepcopy(w)
                                    temp_2 = copy.deepcopy(v)
                                    while(temp_1.top != None):
                                        temp_1 = temp_1.top
                                        dif = dif + 1
                                        if(temp_1 != g[1]):
                                            dif = dif + 1
                                    while(temp_2.top != None):
                                        temp_2 = temp_2.top
                                        dif = dif + 1
                                        if(temp_2 != g[1]):
                                            dif = dif + 1
                                blocker = v.top
                                if(blocker != w and g[1] != w and blocker != None):
                                    dif = dif + 1
                                    
                            else:
                                dif1 = max([abs(w.x + 1 - v.x), abs(w.y - v.y), abs(w.z - v.z)])
                                dif2 = max([abs(w.x - 1 - v.x), abs(w.y - v.y), abs(w.z - v.z)])
                                dif3 = max([abs(w.x - v.x), abs(w.y + 1 - v.y), abs(w.z - v.z)])
                                dif4 = max([abs(w.x - v.x), abs(w.y - 1 - v.y), abs(w.z - v.z)])
                                dif = min([dif1, dif2, dif3, dif4])
                                if(w.z != v.z):
                                    temp_1 = copy.deepcopy(w)
                                    temp_2 = copy.deepcopy(v)
                                    while(temp_1.top != None and temp_2.top != None):
                                        temp_1 = temp_1.top
                                        temp_2 = temp_2.top
                                        dif = dif + 1
                                        if(temp_2 != g[1] or temp_1 != g[1]):
                                            dif = dif + 1
                            if(min_card[2] > dif):
                                min_card = (w, v, dif)
                dont.append(min_card[0].block_id)
                dont.append(min_card[1].block_id)
                if(ary[3] == "side-by-side" and min_card[1] not in min_card[0].sides):
                    if(min_card[0].z != min_card[1].z and min_card[1].top != None):
                        if(min_card[1].below != None):
                            action.append("move " + min_card[1].below.block_id + " remove-top")
                        else:
                            action.append("move " + min_card[1].block_id + " remove-top")
                    if(min_card[0].z != min_card[1].z and min_card[0].top != None):
                        if(min_card[0].below != None):
                            action.append("move " + min_card[0].below.block_id + " remove-top")
                        else:
                            action.append("move " + min_card[0].block_id + " remove-top")
                    if(min_card[0].z != min_card[1].z and min_card[0].below != None and len(min_card[0].below.sides) == 0 and min_card[1].below != None and len(min_card[1].below.sides) == 0):
                        if(min_card[0].z > min_card[1].z):
                            action.append("move " + min_card[1].block_id + " find-stack")
                        else:
                            action.append("move " + min_card[0].block_id + " find-stack")                            
                    action.append(ary[0] + " " + min_card[0].block_id + " " + min_card[1].block_id + " side-by-side")
                    
                    
                if(ary[3] == "on-top-of" and min_card[1].top != min_card[0]):
                    if(min_card[1].top != None):
                        action.append("move " + min_card[1].block_id + " remove-top")
                    if(min_card[0].top != None):
                        action.append("move " + min_card[0].block_id + " remove-top")
                    action.append(ary[0] + " " + min_card[0].block_id + " " + min_card[1].block_id + " on-top-of")
        if(action != []):
            actions.append(colors + action)   
    top = []
    bottom = []
    
    
    
    for a in actions:
        for b in a:
            if('on-top-of' in b):
                ary = b.split()
                top.append(ary[1])
                bottom.append(ary[2])
                
    for a in actions:
        for b in a:
            if('side-by-side' in b):
                ary = b.split()
                if(ary[1] in top):
                    top.append(ary[2])
                elif(ary[2] in top):
                    top.append(ary[1])
    remove = []            
    for c in actions:
        for d in c:
            ary = d.split()
            if(ary[2] in top):
                remove.append(c)
                
    for r in remove:
        actions.remove(r)
        
    e2 = copy.deepcopy(actions)
    for inde, e in enumerate(actions):
        for indf, f in enumerate(e):
            if('move' in f):
                e2[inde][indf] = f + " " + str(dont)[1:-1].replace(',', '').replace("'", "") 
    actions = e2
                   
    return (actions, dont)

from random import randint
def take_action_H(action, state, dont):
    newState = copy.deepcopy(state)
    moves = []
    remove = []
    tops = []
    belows = []
    bottoms = {}
    sides = []
    cost = 0
    moves = []    
    for a in action:
        ary = a.split()
        if(len(ary) >= 4):
            if(ary[3] == "side-by-side"):
                sides.append(ary[1])
                sides.append(ary[2])
            if(ary[3] == "on-top-of"):
                tops.append(ary[1])
                belows.append(ary[2])
                bottoms[ary[1]] = ary[2]
                
                
    blocks = tops + belows + sides   
    actions2 = None
    actions3 = None
    act1a = None
    act1b = None
    act2a = None
    act2b = None
    
    for b in action:
        if(b != [None]):
            ary = b.split()
            if(len(ary) >= 4):
                if(ary[3] == "side-by-side"):
                    if(ary[1] in tops and ary[2] not in tops):
                        moves =  moves + remove_from_top(ary[2], blocks, newState)      
                        wildcard1 = "wildcard" + str(randint(0, 99999))
                        moves = moves + find_stack(ary[1], blocks, newState)
                        act1a = "is " + bottoms.get(ary[1], None) + " " + wildcard1 + " side-by-side"
                        act1b = "is " + ary[2] + " " + wildcard1 + " on-top-of"
                        actions2b, cost2b, parentState2b = aStarSearchLow(newState, [act1a, act1b], actions_2, take_action_2, h_5, 1000)
                        cost = cost + cost2b
                        newState = parentState2b
                        moves = moves + actions2b
                        tops.append(ary[2])
                    if(ary[2] in tops and ary[1] not in tops):
                        moves = moves + remove_from_top(ary[1], blocks, newState)
                        wildcard2 = "wildcard" + str(randint(0, 99999))
                        moves = moves + find_stack(ary[2], blocks, newState)
                        act2a = "is " + bottoms.get(ary[2], None) + " " + wildcard2 + " side-by-side"
                        act2b = "is " + ary[1] + " " + wildcard2 + " on-top-of"
                        actions2d, cost2d, parentState2d = aStarSearchLow(newState, [act2a, act2b], actions_2, take_action_2, h_5, 1000)
                        cost = cost + cost2d
                        newState = parentState2d
                        moves = moves + actions2d
                        tops.append(ary[1])
                    
    if(act1a != None):
        action.append(act1a)
    if(act1b != None):
        action.append(act1b)
    if(act2a != None):
        action.append(act2a)
    if(act2b != None):
        action.append(act2b)
    for x in action:
        if(x != [None] and x != None):
            ary = x.split()
            if(len(ary) >= 3):
                if(ary[0] == "move"):
                    if(ary[2] == "remove-top"):
                        moves = moves + remove_from_top(ary[1], ary[3::], newState)
                        remove.append(x)
            if(len(ary) >= 3):
                if(ary[0] == "move"):
                    if(ary[2] == "find-stack"):
                        moves = moves + find_stack(ary[1], ary[3::], newState)
                        remove.append(x)
    for r in remove:
        action.remove(r)
    actions, cost, parentState = aStarSearchLow(newState, action, actions_2, take_action_2, h_5, 1000)

    return (moves + actions), (cost + len(moves)), parentState

def find_stack(block_str, wildcards, state):
    block_one = find2(block_str, state)
    
    actions = []
    while(block_one.below != None and len(block_one.below.sides) == 0):
        temp = block_one
        while(temp.below != None and len(temp.below.sides) == 0):
            temp = temp.below
        if(temp.z == 0):
            best = (None, 1000, 0)
            for s in state:
                if(s.z == 0 and s.block_id not in wildcards):
                    t = copy.deepcopy(s)
                    while(t.top != None and t.top.block_id not in wildcards and t.top.z > block_one.z - 1):
                        t = t.top
                    if(t.top == None and t.z > best[2]):
                        best = (t, max([abs(block_one.z - t.z), abs(block_one.y - t.y)]), t.z)
                    if(t.top == None and t.z == best[2] and max([abs(block_one.z - t.z), abs(block_one.y - t.y)]) < best[1]):
                        best = (t, max([abs(block_one.z - t.z), abs(block_one.y - t.y)]), t.z)
            if(best[0] != None):
                answer = aStarSearchLow(state, ["is " + temp.block_id + " " + best[0].block_id + " side-by-side"], actions_2, take_action_2, h_5, 1000)
                state = answer[2]
                actions = actions + answer[0][1::]
                g = get_grabbed(state)
                if(g[1] != None):
                    release(g[1], state)
                    actions.append(("release", (g[0], g[1].block_id)))
        elif(temp.z != 0):
            best = (None, 1000)
            for s in state:
                if(s.top == None and s.block_id not in wildcards and s != block_one):
                    if(max([abs(block_one.z - s.z), abs(block_one.y - s.y), abs(block_one.z - s.z)]) < best[1]):
                        best = (s, max([abs(block_one.z - s.z), abs(block_one.y - s.y), abs(block_one.z - s.z)]))
            if(best[0] != None):
                answer = aStarSearchLow(state, ["is " + temp.block_id + " " + best[0].block_id + " side-by-side"], actions_2, take_action_2, h_5, 1000)
                state = answer[2]
                actions = actions + answer[0][1::] 
                g = get_grabbed(state)
                if(g[1] != None):
                    release(g[1], state)
                    actions.append(("release", (g[0], g[1].block_id)))
        block_one = find2(block_str, state)
    return actions

def remove_from_top(block_str, wildcards, state):
    block_one = find2(block_str, state)
    actions = []
    while(block_one.top != None):
        block_one = find2(block_str, state)
        temp = block_one
        while(temp.top != None):
            temp = temp.top
        check1 = (find(temp.x + 1, temp.y + 1, temp.z, state), (temp.x + 1, temp.y + 1, temp.z))
        check2 = (find(temp.x - 1, temp.y - 1, temp.z, state), (temp.x - 1, temp.y - 1, temp.z))
        check3 = (find(temp.x + 1, temp.y - 1, temp.z, state), (temp.x + 1, temp.y - 1, temp.z))
        check4 = (find(temp.x - 1, temp.y + 1, temp.z, state), (temp.x - 1, temp.y + 1, temp.z))
        check5 = (find(temp.x + 1, temp.y, temp.z, state), (temp.x + 1, temp.y, temp.z))
        check6 = (find(temp.x, temp.y + 1, temp.z, state), (temp.x, temp.y + 1, temp.z))
        check7 = (find(temp.x - 1, temp.y, temp.z, state), (temp.x - 1, temp.y, temp.z))
        check8 = (find(temp.x, temp.y - 1, temp.z, state), (temp.x, temp.y - 1, temp.z))
        checks = [check1, check2, check3, check4, check5, check6, check7, check8]
        remove = []
        for c in checks:
            if(c[1][0] < 0 or c[1][1] < 0 ):
                  remove.append(c)
                  
        for r in remove:
            checks.remove(r)
        not_found = True
        place = None
        while(not_found):
            check_copy = copy.deepcopy(checks)
            for indc, c in enumerate(checks):
                if(c[0] != None and c[0].top == None and c[0].block_id not in wildcards):
                    place = copy.deepcopy((c[1][0], c[1][1], c[1][2] + 1))
                    not_found = False
                elif(c[0] != None and c[0].top == None):
                    if((c[1][0] - temp.x) > 1):
                        newX = c[1][0] + 1
                    elif((c[1][0] - temp.x) < 1):
                        newX = c[1][0] - 1
                    else:
                        newX = c[1][0]
                    if((c[1][1] - temp.y) > 1):
                        newY = c[1][1] + 1
                    elif((c[1][1] - temp.y) < 1):
                        newY = c[1][1] - 1
                    else:
                        newY = c[1][1]
                    newpos = (find(newX, newY, c[1][2] + 1, state), (newX, newY, c[1][2] + 1))
                    while(newpos[0] != None):
                        newpos = (newpos[0].top, (newpos[1][0], newpos[1][1], newpos[1][2] + 1))
                    check_copy[indc] = copy.deepcopy(newpos)
                elif(c[0] != None and c[0].top != None):
                    check_copy[indc] = copy.deepcopy((c[0].top, (c[1][0], c[1][1], c[1][2] + 1)))
                elif(c[0] == None and (c[1][2] == 0 or ((find(c[1][0], c[1][1], c[1][2] - 1, state) != None) and find(c[1][0], c[1][1], c[1][2] - 1, state).block_id not in wildcards))):
                    place = copy.deepcopy((c[1][0], c[1][1], c[1][2]))
                    not_found = False
                elif(c[0] == None and (c[1][2] == 0 or find(c[1][0], c[1][1], c[1][2] - 1, state) != None)):
                    if((c[1][0] - temp.x) > 1):
                        newX = c[1][0] + 1
                    elif((c[1][0] - temp.x) < 1):
                        newX = c[1][0] - 1
                    else:
                        newX = c[1][0]
                    if((c[1][1] - temp.y) > 1):
                        newY = c[1][1] + 1
                    elif((c[1][1] - temp.y) < 1):
                        newY = c[1][1] - 1
                    else:
                        newY = c[1][1]
                    check_copy[indc] = copy.deepcopy((find(newX, newY, c[1][2], state), (newX, newY, c[1][2])))                    
                elif(c[0] == None):
                    check_copy[indc] = copy.deepcopy((find(c[1][0], c[1][1], c[1][2] - 1, state), (c[1][0], c[1][1], c[1][2] - 1)))
            checks = copy.deepcopy(check_copy)
        g = get_grabbed(state)
        if(g[1] != None):
            while(g[1].z != 0 and g[1].below == None):
                carry(g[1], 0, 0, -1, state)
                actions.append(("carry", (None, g[1].block_id), (0,0, -1)))
            release(g[1], state)
            actions.append(("release", (g[0], g[1].block_id)))
        grab(temp, state)
        actions.append(("grab", (None, temp.block_id)))
        if (place[2] == temp.z):
            move = 0
        elif (place[2] > temp.z):
            move = 1
        elif (place[2] < temp.z):
            move = -1
        while(move == 1 and (place[2] - temp.z) > 1 ):
            carry(temp, 0, 0, move, state)
            actions.append(("carry", (None, temp.block_id), (0,0, move)))
        carry(temp, place[0] - temp.x, place[1] - temp.y, move, state)
        actions.append(("carry", (None, temp.block_id), (block_one.x - place[0], block_one.y - place[1], move)))
        while(temp.z != place[2]):
            carry(temp, 0, 0, move, state)
            actions.append(("carry", (None, temp.block_id), (0, 0, move)))

        release(temp, state)
        actions.append(("release", (None, temp.block_id)))
        block_one = find2(block_str, state)
    return actions

def aStarHigh(parentNode, goalState, actionsF, take_actionF, hF, fmax):
    if(check(parentNode.state, goalState)):
        return(parentNode.moves, parentNode.g, parentNode.state)
    actions, dont = actionsF(parentNode.state, goalState)
    if not actions:
        return("no more moves", float("inf"), parentNode.state)
    children = []
    for action in actions:
        moves, cost, childState = take_actionF(parentNode.action + action if parentNode.action != None else action, parentNode.state, dont)
        h = hF(childState, goalState)
        g = parentNode.g + cost
        f = max(h+g, parentNode.f)
        childNode = Node2(state=childState, action = parentNode.action + action if parentNode.action != None else action, moves = moves, h=h, g=g, f=f)
        children.append(childNode)
    while True:
        minChild = min(children, key = lambda x: x.f)
        if minChild.f > fmax:
            return ("max steps exceded", minChild.f, parentNode.state)
        alternativef = minChild.f if len(children) > 1 else float('inf')
        result, minChild.f, parentState = aStarHigh(minChild, goalState, actionsF, take_actionF, hF, min(fmax,alternativef))
        if result is not "no more moves" and result is not "max steps exceded":   
            if(parentNode.moves != None):
                result = parentNode.moves + result
            return (result, minChild.f, parentState) 
        
def aStarSearchHigh(startState, goalState, actionsF, take_actionF, hF, fmax):
    answer = aStarHigh(Node2(state=startState, action=None, moves=None, f=0, g=0, h=0), goalState, actionsF, take_actionF, hF, fmax)
    if((answer[0] ==  "max steps exceded") or (answer[0] == "no more moves")):
        print(answer)
    else:
        return answer
    
# start_time = timeit.default_timer()
startState = read_startState(sys.argv[1])
goalState = read_goalState(sys.argv[2])
tops = []
colors = []
locations = []
sides = []
for g in goalState:
    if("color" in g):
        colors.append(g)
        
for g in goalState:
    if("location" in g):
        locations.append(g)
        
for g in goalState:
    if("on-top-of" in g):
        tops.append(g)
        
for g in goalState:
    if("side-by-side" in g):
        sides.append(g)
        
total_moves = [] 

moves, cost, state = aStarSearchHigh(startState, (colors + locations), actions_H, take_action_H, h_5, 1000)
g = get_grabbed(state)
if(g[1] != None):
    while(g[1].z > 0 and g[1].below == None):
        carry(g[1], 0, 0, -1, state)
        moves.append(("carry", (g[0], g[1].block_id), (0, 0, -1)))
    release(g[1], state)
    moves.append(("release", (g[0], g[1].block_id)))
        
if(moves != None and moves != [None] and moves != []):
    total_moves = total_moves + moves

moves, cost, state = aStarSearchHigh(state, (colors + tops), actions_H, take_action_H, h_5, 1000)
g = get_grabbed(state)
if(g[1] != None):
    while(g[1].z > 0 and g[1].below == None):
        carry(g[1], 0, 0, -1, state)
        moves.append(("carry", (g[0], g[1].block_id), (0, 0, -1)))
    release(g[1], state)
    moves.append(("release", (g[0], g[1].block_id)))

if(moves != None and moves != [None] and moves != []):
    total_moves = total_moves + moves
    
moves, cost, state = aStarSearchHigh(state, (colors + tops + locations), actions_H, take_action_H, h_5, 1000)
g = get_grabbed(state)
if(g[1] != None):
    while(g[1].z > 0 and g[1].below == None):
        carry(g[1], 0, 0, -1, state)
        moves.append(("carry", (g[0], g[1].block_id), (0, 0, -1)))
    release(g[1], state)
    moves.append(("release", (g[0], g[1].block_id)))
    
if(moves != None and moves != [None] and moves != []):
    total_moves = total_moves + moves

moves, cost, state = aStarSearchHigh(state, (colors + sides), actions_H, take_action_H, h_5, 1000)
g = get_grabbed(state)
if(g[1] != None):
    while(g[1].z > 0 and g[1].below == None):
        carry(g[1], 0, 0, -1, state)
        moves.append(("carry", (g[0], g[1].block_id), (0, 0, -1)))
    release(g[1], state)
    moves.append(("release", (g[0], g[1].block_id)))
    
if(moves != None and moves != [None] and moves != []):
    total_moves = total_moves + moves

    
moves, cost, state = aStarSearchHigh(state, (colors + tops), actions_H, take_action_H, h_5, 1000)
g = get_grabbed(state)
if(g[1] != None):
    while(g[1].z > 0 and g[1].below == None):
        carry(g[1], 0, 0, -1, state)
        moves.append(("carry", (g[0], g[1].block_id), (0, 0, -1)))
    release(g[1], state)
    moves.append(("release", (g[0], g[1].block_id)))
    
if(moves != None and moves != [None] and moves != []):
    total_moves = total_moves + moves
    
for s in sides:
    moves, cost, state = aStarSearchHigh(state, (colors + tops + [s]), actions_H, take_action_H, h_5, 1000)
    g = get_grabbed(state)
    if(g[1] != None):
        while(g[1].z > 0 and g[1].below == None):
            carry(g[1], 0, 0, -1, state)
            moves.append(("carry", (g[0], g[1].block_id), (0, 0, -1)))
        release(g[1], state)
        moves.append(("release", (g[0], g[1].block_id)))
    if(moves != None and moves != [None] and moves != []):
        total_moves = total_moves + moves

moves, cost, state = aStarSearchHigh(state, (colors + tops + sides + locations), actions_H, take_action_H, h_5, 1000) 
# g = get_grabbed(state)
# if(g[1] != None):
#     release(g[1], state)
#     moves.append(("release", g))
    
if(moves != None and moves != [None] and moves != []):
    total_moves = total_moves + moves

moves_count = 0
remove = []
if(total_moves != None and total_moves != [None] and total_moves != []):
    for indr, r in enumerate(total_moves):
        if(r == None):
            remove.append(r)
            
for rem in remove:
    total_moves.remove(rem)
remove = []            
if(total_moves != None and total_moves != [None] and total_moves != []):
    for indt, t in enumerate(total_moves):
        if(t != None and len(total_moves) - 1 > indt and t[0] == "carry" and total_moves[indt-1][0] == "grab" and total_moves[indt+1][0] == "release"):
            count = 0
            for inds, s in enumerate(total_moves[indt + 1::]):
                if(s != None and ((len(total_moves) - 1) > (1 + indt + inds)) and s[0] == "slide"):
                    break
                if(s != None and ((len(total_moves) - 1) > (1 + indt + inds)) and s[0] == "carry" and t[1][1] == s[1][1] and total_moves[1 + indt + inds-1][0] == "grab" and total_moves[1 + indt  + inds + 1][0] == "release"):
                    if(s[1][1] == t[1][1] and (s[2][0]+t[2][0]) == 0 and (s[2][1]+t[2][1]) == 0 and (s[2][2]+t[2][2]) == 0):
                        remove.append(1 + indt + inds)
                        remove.append(indt)
                    elif(s[1][1] == t[1][1]):
                        break
                    else:
                        count = count + 1
                        if(count == 2):
                            break                       
remove.sort()
remove.reverse()
for rem2 in remove:
    del total_moves[rem2-1:rem2+2]
    
remove = []    
if(total_moves != None and total_moves != [None] and total_moves != []):
    for indt, t in enumerate(total_moves):
        if(t != None and len(total_moves) - 2 > indt and t[0] == "release" and total_moves[indt+1][0] == "grab" and t[1][1] == total_moves[indt+1][1][1]):
            remove.append(indt)
            remove.append(indt + 1)
remove.sort()
remove.reverse() 
for rem3 in remove:
    del total_moves[rem3]
    
for rang in range(0, len(total_moves) - 1):
    if(total_moves != None and total_moves != [None] and total_moves != []):
        remove = []
        add = []
        for indt, t in enumerate(total_moves):
            if(t != None and len(total_moves) - 2 > indt and t[0] == "carry" and total_moves[indt+1][0] == "carry" and t[1][1] == total_moves[indt+1][1][1]):
                if(-2 < t[2][0] + total_moves[indt+1][2][0] < 2 and -2 < t[2][1] + total_moves[indt+1][2][1] < 2 and -2 < t[2][2] + total_moves[indt+1][2][2] < 2):
                    add.append((indt, (t[0], t[1], (t[2][0] + total_moves[indt+1][2][0], t[2][1] + total_moves[indt+1][2][1], t[2][2] + total_moves[indt+1][2][2]))))
                    remove.append(indt+1)
                    break
                    
    for a in add:
        total_moves[a[0]] = a[1]
                    
    remove.sort()
    remove.reverse() 
    for rem4 in remove:
        del total_moves[rem4]
print(state) 
moves_count = 0    
for a in total_moves:
    if(a != None and a != []):
        print("(" + str(a[0]) + ", " + str(a[1][1]) + ("" if (len(a) == 2) else (", " + str(a[2]))) + ")")
        moves_count = moves_count + 1
print(moves_count)
print()
print(state)
