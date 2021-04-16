# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from sp import *
from parser import *
from itertools import product
from automateBase import AutomateBase

import itertools

class Automate(AutomateBase):

    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ (self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        successeurs = []
        #Parcours sur les etats de l'automates
        for state in listStates:
            #Si l'etat n'est pas dans la liste des successeurs
            if state not in successeurs:
                #Ajout dans la liste des successeurs de l'etat courant
                successeurs += self.succElem(state, lettre)
        return successeurs




    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """
    @staticmethod
    def accepte(auto,mot) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        #Liste des etats initiaux
        states = auto.getListInitialStates()

        #Parcours dans le mot passe en argument
        for l in mot:

            #On donne la liste des successeurs de l'etat courant et de la lettre
            states = auto.succ(states, l)

        #Parcours dans la liste des etats
        for s in states:

            #Verification si l'etat appartient aux etats finaux de l'automate
            if s in auto.getListFinalStates():
                return True
        return False


    @staticmethod
    def estComplet(auto,alphabet) :
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """
        #Parcours sur tous les etats de l'automate
        for state in auto.listStates:

            #Parcours sur tous les etiquettes de l'automate
            for lettre in alphabet:

                #S'il n'y a aucun successeur a partir de l'etat et sa lettre courante
                if (auto.succElem(state,lettre) == []):
                    return False

        return True



    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        #Creation de l'ensemble des etiquettes
        etiquettes = set()

        #Parcours sur les toutes les Transitions de l'automate
        for t in auto.listTransitions:
            #Ajout de l'etiquette de la Transition dans l'ensemble des etiquettes
            etiquettes.add(t.etiquette)

        #Parcours sur tous les etats
        for state in auto.listStates:

            #Parcours sur les etiquettes
            for lettre in etiquettes:

                #S'il y a plusieurs transitions a partir d'un etat
                if (len(auto.succElem(state,lettre)) > 1):
                    return False
        return True



    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        #Copie de l'automate
        newauto = copy.deepcopy(auto)

        #Parcours sur tous les etats
        for state in newauto.listStates:

            #Parcours sur les etiquettes
            for lettre in alphabet:

                #Si on ne trouve aucun successeur de l'etat courant
                if (newauto.succElem(state,lettre) == []):

                    #Creation d'un etat
                    s = State(1000, False, False)
                    newauto.addState(s)

                    #Ajout de la transition
                    t = Transition(state, lettre, s)
                    newauto.addTransition(t)

        return newauto


    @staticmethod
    def determinisation(auto) :
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        #Creation de l'automate determinise
        newauto = Automate([])

        #Creation d'une list des etats de l'automate
        list = auto.listStates

        #Creation de toutes les parties de cet ensemble
        subs = [{list[j] for j in range(len(list)) if 1<<j&i} for i in range(1,1<<len(list))]

        #Creation de nouveaux etats
        id = 0
        for label in subs:

            #Initialisation des parametres pour creer un etat
            init = False
            fin = False

            #Si toutes les etats appartiennent a l'ensemble des etats intitiaux de l'automate
            if ( label - set(auto.getListInitialStates()) ) == set():
                init = True

            #S'il y a au moins un etat final
            if ( label & set(auto.getListFinalStates()) ) != set():
                fin = True

            #Ajout de l'etat dans nouvel automate
            newauto.addState(State(id, init, fin, label))

            #Incrementation du compteur
            id+=1

        #Parours des etats de nouvel automate
        for state in newauto.listStates:

            #Parcours des etiquettes de l'automate
            for lettre in auto.getAlphabetFromTransitions():

                #Parours des etats de nouvel automate
                for s in newauto.listStates:

                    #S'il existe l'ensemble d'etats successeurs equivalent au label de l'etat s
                    if (set(auto.succ(state.label, lettre)) == s.label) :
                        newauto.addTransition(Transition(state, lettre, s))

        #Suppresion des etats inutiles
        for s in newauto.listStates:
            for l in newauto.getAlphabetFromTransitions():
                if (newauto.succElem(state,lettre) == []):
                    newauto.removeState()


        return newauto


    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """

        #Si l'auto n'est pas complet
        if not (auto.estComplet(auto, alphabet)):
            newauto = auto.completeAutomate(auto, alphabet)

        #Si l'auto n'est pas deterministe
        if not (auto.estDeterministe(auto)):
            newauto = auto.determinisation(auto)

        #Liste des etats
        states = set(newauto.listStates)

        #Liste des etats finaux
        finalst = set(newauto.getListFinalStates())

        #Parcours sur les etats qui ne appartiennent pas aux etats finaux
        for state in states.difference(finalst):

            #On met etat courant en etat final
            state.fin = True

        #Parcours sur les etats finaux
        for state in finalst:

            #On change l'etat final en etat initial
            state.fin = False

        return newauto


    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        #PAS FINIE, NOT FINISHED
        """
        newauto = Automate([])

        #Liste des etats de auto0, auto1
        L1 = auto0.listStates
        L2 = auto1.listStates

        #Creation de la Liste des auto0.auto1 etats
        States = list(itertools.product(L1, L2))

        #Parcours sur les couples des etats States
        for (s1, s2) in States:

            #Couple des etats successeurs des deux parcours
            res = ()

            #Parcours sur toutes les etiquettes de auto0
            for lettre in auto0.getAlphabetFromTransitions():

                #S'il existe des successeursa partir de l'etat et la lettre courante
                if (auto0.succElem(s1, lettre) != []):

                    #Parcours sur les etats obtenus
                    for st in auto0.succElem(s1, lettre):



            #Le meme Parcours sur toutes les etiquettes de auto1
            for lettre in auto1.getAlphabetFromTransitions():

                #S'il existe des successeursa partir de l'etat et la lettre courante
                if (auto1.succElem(s2, lettre) != []):
                    res = (,auto1.succElem(s1, lettre))

            newauto.addTransition()


        return newauto
        """
        return

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        #PAS FINIE, NOT FINISHED
        
        """
        #Creation de couples des etats de auto0.auto1
        listStates = list(itertools.product(auto0.listStates, auto1.listStates))

        #Initialisation de la liste des Transitions
        listTransitions = []

        #Il faut que les automates soient complets
        if not (auto0.estComplet(auto0, auto0.getAlphabetFromTransitions())):
            auto0 = auto0.completeAutomate(auto0, auto0.getAlphabetFromTransitions())
        if not (auto1.estComplet(auto1, auto1.getAlphabetFromTransitions())):
            auto1 = auto1.completeAutomate(auto1, auto1.getAlphabetFromTransitions())

        for st1, st2 in listStates:
            for lettre in auto0.getAlphabetFromTransitions():
                #Creation de couple des deux etats courants
                res = (st1, st2)

                for suc in auto0.succElem(st1, lettre):




        return newauto
        """
        return





    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        #PAS FINIE, NOT FINISHED
        """
        #Copie de auto1
        newauto = copy.deepcopy(auto1)

        #Changement des etats finaux de newauto
        for state in auto1.getListFinalStates():
            state.fin = False
            newauto.addState(state)

        #On verifie si les etats initiaux et finaux de l'auto1 sont disjoints
        if ( set(auto1.getListInitialStates()).isDisjoint(set(auto1.getListFinalStates)) ):
            for state in auto2.getListInitialStates():
                #On enleve l'etat initial
                state.init = False
                newauto.addState(state)

        #Ajout des Transitions
        newauto.listTransitions += auto2.listTransitions

        return newauto
        """
        return


    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        return
