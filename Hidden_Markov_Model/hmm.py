
# Zihan Guo
# Hidden Markov Model 

import sys
from logsum import log_sum
from math import log

class Solution:

    def __init__(self):
        self.dev = sys.argv[1] 
        self.hmm_trans = sys.argv[2]
        self.hmm_emit = sys.argv[3] 
        self.hmm_prior = sys.argv[4]
        self.extract_hmm_trans() 
        self.extract_hmm_prior()
        self.nState = len(self.states)
        self.extract_hmm_emit()
        

    def extract_hmm_trans(self):
        self.trans_matrix = [] 
        for row in open(self.hmm_trans):
            row = row.strip()
            words = row.split(" ")
            acc = []
            for index in xrange(1, len(words)):
                tmpt = words[index].split(":")
                acc += [float(tmpt[i]) for i in xrange(1,len(tmpt))]
            self.trans_matrix += [acc]

    def extract_hmm_emit(self):
        self.emit_matrix = [dict() for _ in xrange(self.nState)]
        state = 0 
        for row in open(self.hmm_emit):
            row = row.strip()
            words = row.split(" ")
            for index in xrange(1, len(words)):
                tmpt = words[index].split(":")
                self.emit_matrix[state][tmpt[0]] = float(tmpt[1])
            state += 1

    def extract_hmm_prior(self):
        self.prior_matrix = []
        self.states = []
        for row in open(self.hmm_prior):
            row = row.strip()
            words = row.split(" ")
            self.prior_matrix += [float(words[1])]
            self.states += [words[0]]
        
    def forward(self):
        for line in open(self.dev):
            line = line.strip("\n")
            line = line.split(" ")
            matrix = [[0.0 for _ in xrange(len(line))] for _ in xrange(self.nState)]
            for i in xrange(self.nState):
                matrix[i][0] = (log(self.prior_matrix[i]) + 
                                log(self.emit_matrix[i][line[0]]))
            for i in xrange(1, len(line)):
                for state1 in xrange(self.nState):
                    p = matrix[0][i - 1] + log(self.trans_matrix[0][state1])
                    for state2 in xrange(1, self.nState):
                        trans = self.trans_matrix[state2][state1]
                        prev = matrix[state2][i - 1]
                        p = log_sum(prev + log(trans), p)
                    prob_o = self.emit_matrix[state1][line[i]]
                    p = p + log(prob_o)
                    matrix[state1][i] = p
            p = matrix[0][-1]
            for i in xrange(1, self.nState):
                p = log_sum(p, matrix[i][-1])
            print p

    def backward(self):
        for line in open(self.dev):
            line = line.strip("\n")
            line = line.split(" ")
            matrix = [[0.0 for _ in xrange(len(line))] for _ in xrange(self.nState)]
            for i in xrange(len(line) - 2, -2, -1):
                word = line[i + 1] 
                for state1 in xrange(self.nState):
                    p = (matrix[0][i + 1] + log(self.trans_matrix[state1][0]) + 
                                           log(self.emit_matrix[0][word]))
                    for state2 in xrange(1, self.nState):
                        p = log_sum(p, matrix[state2][i + 1] + 
                                       log(self.trans_matrix[state1][state2]) + 
                                       log(self.emit_matrix[state2][word]))
                    matrix[state1][i] = p
            p = log(self.prior_matrix[0]) + log(self.emit_matrix[0][line[0]]) + matrix[0][0]
            for i in xrange(1, self.nState):
                p = (log_sum(p, log(self.prior_matrix[i]) + 
                     log(self.emit_matrix[i][line[0]]) + matrix[i][0]))
            print p

    def viterbi(self):
        
        for line in open(self.dev):
            line = line.strip("\n")
            line = line.split(" ")

            # Step 1: Create Matrix 

            matrix = [[0.0 for _ in xrange(len(line))] for _ in xrange(self.nState)]
            # sequence contains the parent that promote maximum possibility 
            seq = [[self.states[i] for _ in xrange(len(line))] for i in xrange(self.nState)]
            for i in xrange(self.nState):
                matrix[i][0] = log(self.prior_matrix[i]) + log(self.emit_matrix[i][line[0]])
            for i in xrange(1, len(line)):
                # at time i
                for j in xrange(self.nState):
                    # at state j 
                    p = (matrix[0][i - 1] + log(self.trans_matrix[0][j]) + 
                                            log(self.emit_matrix[j][line[i]]))
                    state = 0
                    for k in xrange(1, self.nState):
                        p_trans = log(self.trans_matrix[k][j])
                        p_prev = matrix[k][i - 1]
                        p_output = log(self.emit_matrix[j][line[i]])
                        p_test = p_prev + p_trans + p_output 
                        if p_test > p:
                            p = p_test 
                            state = k
                    matrix[j][i] = round(p, 3)
                    seq[j][i] = state

            # Step 2: Obtain sequence of symbols with maximum possibility
            maximum = 0
            for i in xrange(1, self.nState):
                if matrix[i][-1] > matrix[maximum][-1]:
                    maximum = i
            key = maximum
            acc = [self.states[maximum]] 
            for i in xrange(len(line) - 1, 0, -1):
                new_key = seq[key][i] 
                key = new_key
                acc = [self.states[new_key]] + acc
            for i in xrange(len(line)):
                print line[i] + "_" + acc[i], 
            print ""


                
# End of Hidden Markov Model 
# November 23, 2016
