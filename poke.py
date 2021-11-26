#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 09:58:02 2021

@author: Jonathan
""" 
# Using Object Oriented Programming
##### Create a pokemon ######################################################

class Pokemon: 
    
    def __init__(self, name, primary_type, max_hp, attack, attack_type, speed): 
        self.name = name
        self.primary_type = primary_type
        self.hp = max_hp
        self.max_hp = max_hp
        self.attack = attack
        self.attack_type = attack_type
        self.speed = speed
        
        
    def __str__(self):
        return f"{self.name} ({self.primary_type}: {self.hp}/{self.max_hp})"
        

    # Heal them
    def heal(self): 
        """
        heal - function to restore health to pokemon
        
        Argument:
            self: each instance of pokemon class
        """
    
        # don't want to heal if already at max_hp
        if self.hp < self.max_hp:
            self.hp += 1
            print(f"{self.name} is now at {self.hp} health!")
        else:
            print(f"{self.name} is at full health!")
            
    # Battle 
    def battle(self, other): # need two pokemon to interact
        """
        
        battle - pokemon battle
        
        Arguments:
            self: instance of pokemon class (pokemon)
            other: 2nd pokemon so that there can be a battle
            
        The two pokemon battle and once one has zero HP, the other wins and
        the battle is over.
            
        """
    
    
    
    
        print(f"Youngster Joey challenges you to a battle! He sends out {other.name}!")
        print(f"Go {self.name}!")
        
        i = 1
        self.hp = self.max_hp
        other.hp = other.max_hp
        
        print(f"{self.name}'s max HP: {self.hp}")
        print(f"{other.name}'s max HP: {other.hp}")
        while self.hp > 0 and other.hp > 0:
            if self.speed > other.speed:
                eff = self.moves(self.attack_type, other.primary_type)
                other.hp -= eff[1]
                print(f"{self.name} used {self.attack} attack! {eff[0]}!")
                print(f"{other.name}'s HP: {other.hp}")
                
                eff2 = self.moves(other.attack_type, self.primary_type)
                self.hp -= eff2[1]
                print(f"{other.name} used {other.attack} attack! {eff2[0]}!")
                print(f"{self.name}'s HP: {self.hp}")
                
                print("Turn", i, "ends")
                i += 1
                
            elif self.speed < other.speed:
                eff2 = self.moves(other.attack_type, self.primary_type)
                self.hp -= eff2[1]
                print(f"{other.name} used {other.attack} attack! {eff2[0]}!")
                print(f"{self.name}'s HP: {self.hp}")
                
                eff = self.moves(self.attack_type, other.primary_type)
                other.hp -= eff[1]
                print(f"{self.name} used {self.attack} attack! {eff[0]}!")
                print(f"{other.name}'s HP: {other.hp}")
                
                print("Turn", i, "ends")
            i += 1
                
        if self.hp <= 0 or other.hp <= 0:
            if self.hp < other.hp:
                print(f"{self.name} fainted! Youngster Timmy and {other.name} win!")
            else:
                print(f"{other.name} fainted! You and {self.name} win!")
            
    
    @staticmethod 
    def moves(type1, type2):
        """
        
        moves - encodes move types and their effectivness against other types
        
        Arguments:
            type1: the type of attack the first pokemon is using 
                (fire, grass, etc)
            type2: the type of attack the second pokemon is using
            
        This function determines how much damage Pokemon 1 will do to 
        Pokemon 2 based on the type of attack Pokemon 1 is using and 
        Pokemon 2's type.

        """
        
        
        eff = {0:["Not very effective", 5], 1:["Super effective", 15],
               -1:["Effective", 10]}
        
        move_map = {"Water":0, "Fire":1, "Grass":2}
        adv_matrix = [
            [-1, 1, 0],
            [0, -1, 1],
            [1, 0, -1]
            ]
        
        adv_result = adv_matrix[move_map[type1]][move_map[type2]]
        return eff[adv_result]
            

if __name__ == '__main__': # only runs these if you run the whole script
    Charizard = Pokemon("Charizard", "Fire", 78, "Fire Blast", "Fire", 100)
    Blastoise = Pokemon("Blastoise", "Water", 79, "Hydro Pump", "Water", 78)
    Venusaur = Pokemon("Venusaur", "Grass", 80, "Petal Dance", "Grass", 80)
    print(Charizard.battle(Venusaur))
    
    
    
    
    
    
    
    
    
    
    
    
    