__author__ = 'Jakub Dutkiewicz'

import random
import sys
class IdGenerator:
    class Id:
        def __init__(self):
            self.val = 0
        def getCurrID(self):
            self.val += 1
            return self.val
    singleton = None
    def __init__(self):
        if not IdGenerator.singleton:
            IdGenerator.singleton = IdGenerator.Id()
    def getCurrId(self):
        return IdGenerator.singleton.getCurrID()
class State:
    def __init__(self, latent, observed = None):
        self.id = IdGenerator().getCurrId()
        self.latent = latent
        self.observed = observed
class Model:
    def __init__(self, States):
        self.States = States
        self.Transitions = {}
        self.CumulativeTransitions = {}
        for s1 in States:
            self.CumulativeTransitions[s1] = 0
            for s2 in States:
                self.Transitions[(s1,s2)] = 0
    def observe(self,value1,value2):
        State1 = self.getObservedState(value1)
        State2 = self.getObservedState(value2)
        self.Transitions[(State1,State2)] += 1
        self.CumulativeTransitions[State1] += 1
    def probability(self,value1,value2):
        State1 = self.getObservedState(value1)
        State2 = self.getObservedState(value2)
        if self.Transitions[(State1,State2)] == 0: return 0
        return self.Transitions[(State1,State2)]/self.CumulativeTransitions[State1]
    def getObservedState(self, value):
        for s in self.States:
            if s.observed == value:
                return s
    def generate_next(self,value):
        r = random.random()
        curr = 0
        State = self.getObservedState(value)
        for s in self.States:
            curr += self.probability(value,s.observed)
            if r < curr:
                return s.observed
        return None
    def printTransitionProbs(self):
        sys.stdout.write('\t\t')
        for s in self.States:
            sys.stdout.write(str(s.observed) + '\t\t')
        sys.stdout.write('\n')
        for s in self.States:
            sys.stdout.write(str(s.observed) + '\t\t')
            for s_t in self.States:
                sys.stdout.write(str(self.probability(s.observed,s_t.observed)) + '\t\t')
            sys.stdout.write('\n')
random.seed(100)

observedValues = ['a','l','b','d',None]
observedStates = []
for value in observedValues:
    observedStates.append(State(latent=0,observed=value))

hmm = Model(observedStates)
hmm.observe('a','b')
hmm.observe('b','l')
hmm.observe('a','l')
hmm.observe('b','a')
hmm.observe('a',None)


c = 'a'

hmm.printTransitionProbs()
'''
for i in range(1000):
    c = 'a'
    sys.stdout.write('\n')
    while(c!=None):
        sys.stdout.write(c)
        c = hmm.generate_next(c)
'''