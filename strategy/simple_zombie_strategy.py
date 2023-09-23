# This is a simple zombie strategy:
# Move directly towards the closest human. If there are any humans in attacking range, attack a random one.
# If there are no humans in attacking range but there are obstacles, attack a random obstacle.

import random
from game.character.action.ability_action import AbilityAction
from game.character.action.attack_action import AttackAction
from game.character.action.move_action import MoveAction
from game.game_state import GameState
from game.character.action.attack_action_type import AttackActionType
from strategy.strategy import Strategy


class SimpleZombieStrategy(Strategy):

    def decide_moves(
            self, 
            possible_moves: dict[str, list[MoveAction]], 
            game_state: GameState
            ) -> list[MoveAction]:
        
        choices = []
        
        predictX = 0
        predictY = 0
        
        
        

        for [character_id, moves] in possible_moves.items():
            
            if len(moves) == 0:  # No choices... Next!
                continue

            pos = game_state.characters[character_id].position  # position of the zombie
            closest_human_pos = pos  # default position is zombie's pos
            closest_human_distance = 1984  # large number, map isn't big enough to reach this distance

            # Iterate through every human to find the closest one
            for c in game_state.characters.values():
                if c.is_zombie:
                    continue  # Fellow zombies are frens :D, ignore them

                distance = abs(c.position.x - pos.x) + abs(c.position.y - pos.y) # calculate manhattan distance between human and zombie
                if distance < closest_human_distance:  # If distance is closer than current closest, replace it!
                    closest_human_pos = c.position
                    closest_human_distance = distance

            initDistance = abs(game_state.characters[character_id].position.x - closest_human_pos.x) + abs(game_state.characters[character_id].position.y)
            if (pos.x > closest_human_pos.x):
                predictX = closest_human_pos.x - 2
            elif (pos.x == closest_human_pos.x):
                predictX = closest_human_pos.x
            else :
                predictX = closest_human_pos.x + 3
                
            if (pos.y > closest_human_pos.y):
                predictY = closest_human_pos.y - 2
            elif (pos.y == closest_human_pos.y):
                predictY = closest_human_pos.y
            else:
                predictY = closest_human_pos.y + 1

            print(str(predictX))
            print(str(predictY))
            # Move as close to the human as possible
            move_distance = 1337  # Distance between the move action's destination and the closest human
            move_choice = moves[0]  # The move action the zombie will be taking
            for m in moves:
                #if ((abs(m.destination.x - c.position.x) + abs(m.destination.y - c.position.y)) < 3):
                    #distance = abs(m.destination.x - c.position.x) + abs(m.destination.y - c.position.y)
                #else :
                #if closest_human_distance > 5:
                distance = abs(m.destination.x - predictX) + abs(m.destination.y - predictY)  # calculate manhattan distance
                #else:
                #distance = abs(m.destination.x - c.position.x) + abs(m.destination.y - c.position.y)
                # If distance is closer, that's our new choice!
                if distance < move_distance:  
                    move_distance = distance
                    move_choice = m
            
            choices.append(move_choice)  # add the choice to the list

        return choices

    def decide_attacks(
            self, 
            possible_attacks: dict[str, list[AttackAction]], 
            game_state: GameState
            ) -> list[AttackAction]:

        choices = []

        for [character_id, attacks] in possible_attacks.items():
            if len(attacks) == 0:  # No choices... Next!
                continue

            humans = []  # holds humans that are in range
            
            currentChar = game_state.characters[character_id]
            closest_human_distance = 1234
            closest_human = None

            # Gather list of humans in range
            for a in attacks:
                if a.type is AttackActionType.CHARACTER:
                    attackee_pos = game_state.characters[a.attacking_id].position  # Get position of human in question
                    
                    distance = abs(attackee_pos.x - currentChar.position.x) + abs(attackee_pos.y - currentChar.position.y)  # Get distance between the two
                    if (game_state.characters[a.attacking_id].health > 0):
                        if (distance < closest_human_distance):
                            closest_human = a
                            closest_human_distance = distance
                    
                    humans.append(closest_human)

            if humans:  # Attack a closest human in range
                choices.append(closest_human)
            else:  # No humans? Shame. The targets in range must be terrain. May as well attack one.
                choices.append(random.choice(attacks))

        return choices
