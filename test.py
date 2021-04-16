# -*- coding: utf-8 -*-
"""
Code modifiable.
"""

from automate import Automate
from state import State
from transition import Transition
from parser import *
import itertools

"""
automate = Automate.creationAutomate("exempleAutomate.txt")
automate.show("exempleAutomate")
"""
"""
#1
#creation etats
s0 = State(0, True, False)
s1 = State(1, False, False)
s2 = State(2, False, True)

#creation transitions
t1 = Transition(s0, "a", s0)
t2 = Transition(s0, "b", s1)
t3 = Transition(s1, "a", s2)
t4 = Transition(s1, "b", s2)
t5 = Transition(s2, "a", s0)
t6 = Transition(s2, "b", s1)
"""

#2 PRISE EN MAIN
#2.1
#1
"""
auto = Automate([t1,t2,t3,t4,t5,t6])
print(auto)
auto.show("A_ListeTrans")
"""

#2
"""
auto1 = Automate([t1,t2,t3,t4,t5,t6], [s0,s1,s2])
print(auto1)
auto1.show("A_ListeTrans1")
"""

#3
"""
auto2 = Automate.creationAutomate("auto.txt")
print(auto2)
auto2.show("auto")
"""
#2.2
#1
"""
t = Transition(s0, "a", s1)
auto.addTransition(t)
print(auto)
auto.removeTransition(t)
print(auto)
auto.removeTransition(t1)
print(auto)
auto.addTransition(t1)
print(auto)
"""

#2
"""
auto.removeState(s1)
print(auto)
auto.addState(s1)
print(auto)
s3 = State(3, True, False)
auto.addState(s3)
print(auto)
"""

#3
"""
print(auto.getListTransitionsFrom(s1))
print(auto1.getListTransitionsFrom(s1))
"""

#3 EXERCICES DE BASE
#1
#print(auto.succ([s0,s1,s2], "a"))
"""
monauto = Automate.creationAutomate("auto.txt")
print(monauto);
monauto.show("auto")
"""

"""
#2
if monauto.accepte(monauto,"aaa"):
    print "L'automate accepte le mot aaa"
else:
    print "L'automate n'accepte pas le mot aaa"

#3
if monauto.estComplet(monauto, "ab"):
    print "L'automate est complet"
else:
    print "L'automate n'est pas complet"

#4
if monauto.estDeterministe(monauto):
    print "L'automate est deterministe"
else:
    print "L'automate n'est pas deterministe"

#5
autocomplet = monauto.completeAutomate(monauto,"abc")
print(autocomplet)
autocomplet.show("autocomplet")
"""

#4 DETERMINISATION
"""
autodet = monauto.determinisation(monauto)
print(autodet)
autodet.show("autodet")
"""

#5 CONSTRUCTION SUR LES AUTOMATES REALISANT DES OPERATIONS SUR LES LANGAGES ACCEPTES

#1
"""
autocomplementaire = monauto.complementaire(monauto, "ab")
print(autocomplementaire)
autocomplementaire.show("autocomplementaire")
"""

#2
L1 = [1, 2, 3]
L2 = ["a", "b", "c"]
L = list(itertools.product(L1, L2))
print(L)
"""
auto0 = Automate.creationAutomate("auto0.txt")
auto1 = Automate.creationAutomate("auto1.txt")

inter = auto0.intersection(auto0, auto1)
"""
