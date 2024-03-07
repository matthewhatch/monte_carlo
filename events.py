import numpy as np

def single(current_state):
    types = ['Short', 'Medium', 'Long']
    probabilities = [.2, .5, .3]
    type = np.random.choice(types, p=probabilities)

    new_state = [current_state[0],0,0,0]
    runs_scored = 0
    
    if type == 'Short':
        new_state, runs_scored = short_single(current_state)

    if type == 'Medium':
        new_state, runs_scored = medium_single(current_state)
    
    if type == 'Long':
        new_state, runs_scored = long_single(current_state)

    return new_state, runs_scored

def short_single(current_state):
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    if current_state[3] == 1:
        runs_scored = runs_scored + 1

    # move runners on 1st and second up 1 base
    new_state[2] = current_state[1]
    new_state[3] = current_state[2]
    new_state[1] = 1

    return new_state, runs_scored

def medium_single(current_state):
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    runs_scored = runs_scored + current_state[2] + current_state[3]
    
    new_state[1] = 1
    new_state[2] = current_state[1]
    new_state[3] = 0

    return new_state, runs_scored

def long_single(current_state):
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    runs_scored = runs_scored + current_state[2] + current_state[3]

    new_state[1] = 1   
    new_state[2] = 0    
    new_state[3] = current_state[1]

    return new_state, runs_scored

def double(current_state):
    types = ['Short', 'Long']
    probabilities = [.8, .2]
    type = np.random.choice(types, p=probabilities)
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    if type == 'Short':
        new_state, runs_scored = short_double(current_state)

    if type == 'Long':
        new_state, runs_scored = long_double(current_state)

    return new_state, runs_scored

def short_double(current_state):
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    new_state[1] = 0
    new_state[2] = 1
    runs_scored = runs_scored + current_state[2] + current_state[3]
    new_state[3] = current_state[1]
    
    return new_state, runs_scored

def long_double(current_state):
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    new_state[1] = 0
    new_state[2] = 1
    new_state[3] = 0
    runs_scored = runs_scored + current_state[1] + current_state[2] + current_state[3]

    return new_state, runs_scored

def triple(current_state):
    new_state = [current_state[0],0,0,0]
    runs_scored = 0
    
    new_state[1] = 0
    new_state[2] = 0
    new_state[3] = 1
    runs_scored = runs_scored + current_state[1] + current_state[2] + current_state[3]

    return new_state, runs_scored

def home_run(current_state):
    new_state = [current_state[0],0,0,0]
    runs_scored = 0

    runs_scored = runs_scored + current_state[1] + current_state[2] + current_state[3] + 1
    new_state = [current_state[0],0,0,0]

    return new_state, runs_scored

def error(current_state):
    new_state = [current_state[0],1,current_state[1],current_state[2]]
    runs_scored = 0

    runs_scored = runs_scored + current_state[3]

    return new_state, runs_scored

def free_pass(current_state):
    new_state = [current_state[0], 0,0,0]
    runs_scored = 0

    new_state[1] = 1
    
    if current_state[1] == 1 and current_state[2] == 0 and current_state[3] == 0:
        new_state[2] = current_state[1]
        
    if current_state[1] == 1 and current_state[2] == 1 and current_state[3] == 0:
        new_state[2] == 1
        new_state[3] == 1

    if current_state[1] == 1 and current_state[2] == 0 and current_state[3] == 1:
        new_state[2] = 1
        new_state[3] = 1
    
    if current_state[3] == 1 and current_state[2] == 1 and current_state[1] == 1:
        runs_scored = runs_scored + 1
        new_state[2] = 1
        new_state[3] = 1 

    return new_state, runs_scored

def out_in_play(current_state):
    types = ['Ground', 'Line', 'Fly']
    probabilities = [.538, .153, .309]
    type = np.random.choice(types, p=probabilities)

    new_state = [current_state[0], 0,0,0]
    runs_scored = 0

    if type == 'Fly':
        new_state, runs_scored = fly_ball(current_state)
    elif type == 'Ground':
        new_state, runs_scored = ground_ball(current_state)
    else:
        new_state = [current_state[0] + 1, current_state[1], current_state[2], current_state[3]]
    
    return new_state, runs_scored

def strike_out(current_state):
    new_state = [current_state[0] + 1, current_state[1], current_state[2], current_state[3]]
    return new_state, 0

def ground_ball(current_state):
    types = ['GO', 'GIDP']
    probabilities = [.5, .5]
    type = np.random.choice(types, p=probabilities)

    if type == 'GO':
        new_state, runs_scored = ground_out(current_state)
    if type == 'GIDP':
        new_state, runs_scored = gidp(current_state)
    
    return new_state, runs_scored
    
def ground_out(current_state):
    new_state = [current_state[0], 0,0,0]
    runs_scored = 0
    new_state[current_state[0] + 1]

    if new_state[0] == 3:
        return new_state, runs_scored
    
    runners_state = current_state[1:3]
    if runners_state in [[1,0,0], [1,1,0], [0,0,0]]:
        # lead runner is out
        # if someone is on second, they are the lead and batter is safe,
        # if someone is not on second, then the runner will be thrown out
        new_state[1] = current_state[2]
        new_state[2] = current_state[3]
    
    if runners_state == [1,1,1]:
        # we'll assume the double play is attempted.
        # runner out at 2nd, safe at first, safe at 3rd, run scores
        runs_scored = runs_scored + 1
        new_state[1] = 1
        new_state[2] = 0
        new_state[3] = 1

    if runners_state ==  [0,0,1]:
        runs_scored = runs_scored + 1
        new_state[1] = 0
        new_state[2] = 0
        new_state[3] = 0
    
    if runners_state == [0,1,0]:
        new_state[1] = 0
        new_state[2] = 1
        new_state[3] = 0

    return new_state, runs_scored

def gidp(current_state):
    new_state = [current_state[0],0,0,0]
    runs_scored = 0
    runners_state = current_state[1:3]
    
    # if there are no runners there can't be a double play
    if runners_state == [0,0,0]:
        return ground_out(current_state)
    
    if current_state[0] > 0:
        # inning will be over with no runs scored
        new_state[0] = 3
        return new_state, runs_scored
    
    if runners_state in [[1,0,0], [1,1,0]]:
        # lead runners are out
        new_state[0] = new_state[0] + 2
        new_state[3] = 0
        new_state[2] = 0
        new_state[1] = current_state[2]
    
    if runners_state == [1,1,1,]:
        # runner scores, batter and runner at 1st going to second is out
        runs_scored = runs_scored + 1
        new_state[0] + 2
        new_state[1] = 0
        new_state[2] = 0
        new_state[3] = 1

    return new_state, runs_scored

def fly_ball(current_state):
    types = ['Short', 'Medium', 'Long']
    probabilities = [.3, .5, .2]
    type = np.random.choice(types, p=probabilities)
    runs_scored = 0
    new_state = [current_state[0], 0, 0, 0]

    if type == 'Short':
        new_state, runs_scored = short_fly(current_state)
    
    if type == 'Medium':
        new_state, runs_scored = medium_fly(current_state)

    if type == 'Long':
        new_state, runs_scored = long_fly(current_state)
    
    return new_state, runs_scored

def short_fly(current_state):
    new_state = [current_state[0], 0,0,0]
    runs_scored = 0

    new_state = [current_state[0] + 1, current_state[1], current_state[2], current_state[3]]
    return new_state, runs_scored

def medium_fly(current_state):
    new_state = [current_state[0], 0,0,0]
    runs_scored = 0

    if current_state[3] == 1 and current_state[0] < 2:
        runs_scored = runs_scored + 1
        new_state[3] = 0
    
    new_state[0] = current_state[0] + 1
    new_state[1] = current_state[1]
    new_state[2] = current_state[2]

    return new_state, runs_scored

def long_fly(current_state):
    new_state = [current_state[0], 0,0,0]
    runs_scored = 0

    if current_state[3] == 1 and current_state[0] < 2:
        runs_scored = runs_scored + 1

    new_state[1] = 0
    new_state[2] = current_state[1]
    new_state[3] = current_state[2]

    return new_state, runs_scored    
