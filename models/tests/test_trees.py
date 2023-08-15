from tale.models.trees import *

grammar = '''
S -> NP VP
VP -> V NP
VP -> VIntr

NP -> Title Name

Name -> Ford
Name -> 
Name -> Hunger

'''
