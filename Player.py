import numpy as np
from events import single, double, triple, home_run, error, free_pass, out_in_play, strike_out

class Player():
    def __init__(
            self,
            plate_appearences,
            at_bats,
            errors,
            outs,
            strike_outs,
            walks,
            hbp,
            singles,
            doubles,
            triples,
            home_runs
    ) -> None:
        self.plate_appearences = plate_appearences
        self.at_bats = at_bats
        self.errors = errors
        self.p_error = errors / plate_appearences
        self.outs = outs
        self.p_out = outs / plate_appearences
        self.strike_outs = strike_outs
        self.p_strike_out = strike_outs / plate_appearences
        self.walks = walks
        self.p_walk = walks / plate_appearences
        self.hbp = hbp
        self.p_hbp = hbp / plate_appearences
        self.singles = singles
        self.p_single = singles / plate_appearences
        self.doubles = doubles
        self.p_double = doubles / plate_appearences
        self.triples = triples
        self.p_triple = triples / plate_appearences
        self.home_runs = home_runs
        self.p_home_run = home_runs / plate_appearences
        self.probabilities = self.normalize_probabilites([self.p_error, self.p_out, self.p_strike_out, self.p_walk, self.p_hbp, self.p_single, self.p_double, self.p_triple, self.p_home_run])
    
    def normalize_probabilites(self, probabilities):
        total_prob = sum(probabilities)
        return [p / total_prob for p in probabilities]
    
    def simulate_ab(self, current_state):
        new_state = [current_state[0],0,0,0]
        runs_scored = 0

        outcomes = ['Error', 'Out', 'Strike Out', 'Walk', 'HBP', 'Single', 'Double', 'Triple', 'Home Run']
        outcome = np.random.choice(outcomes, p=self.probabilities)

        if outcome == 'Home Run':
            new_state, runs_scored = home_run(current_state)
        elif outcome == 'Triple':
            new_state, runs_scored = triple(current_state)
        elif outcome == 'Double':
            new_state, runs_scored = double(current_state)
        elif outcome == 'Error':
            new_state, runs_scored = error(current_state)
        elif outcome == 'Walk' or outcome == 'HBP':
            new_state, runs_scored = free_pass(current_state)
        elif outcome == 'Single':
            new_state, runs_scored = single(current_state)
        elif outcome == 'Strike Out':
            new_state, runs_scored = strike_out(current_state)
        elif outcome == 'Out':
            new_state, runs_scored = out_in_play(current_state)
        else:
            new_state = current_state

        return new_state, runs_scored