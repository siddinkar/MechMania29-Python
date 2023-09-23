# This is a simple human strategy:
# 6 Marksman, 6 Medics, and 4 Traceurs
# Move as far away from the closest zombie as possible
# If there are any zombies in attack range, attack the closest
# If a Medic's ability is available, heal a human in range with the least health

import random
from game.character.action.ability_action import AbilityAction
from game.character.action.ability_action_type import AbilityActionType
from game.character.action.attack_action import AttackAction
from game.character.action.attack_action_type import AttackActionType
from game.character.action.move_action import MoveAction
from game.character.character_class_type import CharacterClassType
from game.game_state import GameState
from game.util.position import Position
from strategy.strategy import Strategy



class SimpleHumanStrategy(Strategy):
    
    
    def decide_character_classes(
            self,
            possible_classes: list[CharacterClassType],
            num_to_pick: int,
            max_per_same_class: int,
            ) -> dict[CharacterClassType, int]:
        # The maximum number of special classes we can choose is 16
        # Selecting 6 Marksmen, 6 Medics, and 4 Traceurs
        # The other 4 humans will be regular class
        choices = {
            CharacterClassType.MARKSMAN: 5,
            CharacterClassType.MEDIC: 5,
            CharacterClassType.TRACEUR: 1,
            CharacterClassType.BUILDER: 5,
        }
        return choices

    def decide_moves(
            self, 
            possible_moves: dict[str, list[MoveAction]], 
            game_state: GameState
            ) -> list[MoveAction]:
        
        choices = []

        for [character_id, moves] in possible_moves.items():
            if len(moves) == 0:  # No choices... Next!
                continue

            print("Health of " + str(character_id) +" is " + str(game_state.characters[character_id].health))
            
            pos = game_state.characters[character_id].position  # position of the human
            closest_zombie_pos = pos  # default position is zombie's pos
            closest_zombie_distance =  1234  # large number, map isn't big enough to reach this distance
            
            # for c in game_state.characters.values():
            #     if not c.is_zombie:
            #         continue
                
            #     move_choice = moves[0]
                
            #     distance = abs(50-c.position.x) + abs(50 - c.position.y)
                
            #     for m in moves:
            #         mDistance = abs(50-m.destination.x) + abs(50 - m.destination.y)
            #         if mDistance < distance:
            #             move_choice = m
            #     choices.append(move_choice)    
                    
            # Iterate through every zombie to find the closest one
            if game_state.characters[character_id].class_type == CharacterClassType.MEDIC:
                for c in game_state.characters.values():
                    if c.is_zombie:
                        continue  # Fellow humans are frens :D, ignore them
                    if c.class_type != CharacterClassType.MEDIC:
                        distance = abs(c.position.x - pos.x) + abs(c.position.y - pos.y)  # calculate manhattan distance between human and zombie
                        if distance < closest_zombie_distance:  # If distance is closer than current closest, replace it!
                            closest_zombie_pos = c.position
                            closest_zombie_distance = distance

                # Move as far away from the zombie as possible EDITED THIS LINE TO MOVE TOWARDS ZOMBIES AND STUNLOCK THEM
                move_distance = -1  # Distance between the move action's destination and the closest zombie
                move_choice = moves[0]  # The move action the human will be taking
                
                
                for m in moves:
                    distance = abs(m.destination.x - closest_zombie_pos.x) + abs(m.destination.y - closest_zombie_pos.y)  # calculate manhattan distance

                    if distance > move_distance:  # If distance is further, that's our new choice!
                        move_distance = distance
                        move_choice = m
            else: 
                    for c in game_state.characters.values():
                        if not c.is_zombie:
                            continue  # Fellow humans are frens :D, ignore them

                        distance = abs(c.position.x - pos.x) + abs(c.position.y - pos.y)  # calculate manhattan distance between human and zombie
                        if distance < closest_zombie_distance:  # If distance is closer than current closest, replace it!
                            closest_zombie_pos = c.position
                            closest_zombie_distance = distance

                    # Move as far away from the zombie as possible EDITED THIS LINE TO MOVE TOWARDS ZOMBIES AND STUNLOCK THEM
                    move_distance = -1  # Distance between the move action's destination and the closest zombie
                    move_choice = moves[0]  # The move action the human will be taking
                    
                    for m in moves:
                        distance = abs(m.destination.x - closest_zombie_pos.x) + abs(m.destination.y - closest_zombie_pos.y)  # calculate manhattan distance

                        if distance > move_distance:  # If distance is further, that's our new choice!
                            move_distance = distance
                            move_choice = m
            
            choices.append(move_choice)  # add the choice to the list

        return choices

    def decide_attacks(self, possible_attacks: dict[str, list[AttackAction]], game_state: GameState) -> list[AttackAction]:
        choices = []
        zombie_is_attacked = {}
        for c in game_state.characters.values():
                if c.is_zombie:
                    zombie_is_attacked[c.id] = False
        
        
        for [character_id, attacks] in possible_attacks.items():
            if len(attacks) == 0:  # No choices... Next!
                continue

            pos = game_state.characters[character_id].position  # position of the human
            closest_zombie = None  # Closest zombie in range
            closest_zombie_distance = 404  # Distance between closest zombie and human
            
                    
            # Iterate through zombies in range and find the closest one
            for a in attacks:
                if a.type is AttackActionType.CHARACTER:
                    attackee_pos = game_state.characters[a.attacking_id].position  # Get position of zombie in question
                    
                    distance = abs(attackee_pos.x - pos.x) + abs(attackee_pos.y - pos.y)  # Get distance between the two
                    if zombie_is_attacked[a.attacking_id] == False:
                        print("zombie was not stunned "+str(game_state.turn)+" "+ str(a.attacking_id)+" "+ str(a.executing_character_id))
                        if distance < closest_zombie_distance:  # Closer than current? New target!
                            closest_zombie = a
                            closest_zombie_distance = distance
                    else:
                        print("zombie was stunned "+str(game_state.turn)+" "+ str(a.attacking_id)+" "+ str(a.executing_character_id))

            if closest_zombie:  # Attack the closest zombie, if there is one
                choices.append(closest_zombie)
                print("shot at zombie" + closest_zombie.attacking_id)
                zombie_is_attacked[closest_zombie.attacking_id] = True
            else:
                for a in attacks:    
                    choices.append(random.choice(attacks))

        return choices

    def decide_abilities(self, possible_abilities: dict[str, list[AbilityAction]], game_state: GameState) -> list[AbilityAction]:
        choices = []

        for [character_id, abilities] in possible_abilities.items():
            if len(abilities) == 0:  # No choices? Next!
                continue
            if game_state.characters[character_id].class_type == CharacterClassType.MEDIC:
                # Since we only have medics, the choices must only be healing a nearby human
                human_target = abilities[0]  # the human that'll be healed
                least_health = 999  # The health of the human being targeted

                for a in abilities:
                    health = game_state.characters[a.character_id_target].health  # Health of human in question
                    if (health < 10):
                        if health < least_health:  # If they have less health, they are the new patient!
                            human_target = a
                            least_health = health

                if human_target:  # Give the human a cookie
                    print("healing"+str(human_target.character_id_target))
                    choices.append(human_target)
            elif game_state.characters[character_id].class_type == CharacterClassType.BUILDER:
                print("FOUND BUILDER")
                #abilities[0].positional_target = Position(game_state.characters[character_id].position.x, game_state.characters[character_id].position.y+1)
                choices.append(abilities[0])
        # for [character_id, abilities] in possible_abilities.items():
        #     if len(abilities) == 0:  # No choices? Next!
        #         continue
               
        #     #if game_state.characters[character_id].class_type == CharacterClassType.MEDIC:
        #             # Since we only have medics, the choices must only be healing a nearby human
        #     human_target = abilities[0]  # the human that'll be healed
        #     least_health = 999  # The health of the human being targeted

        #     for a in abilities:
        #         health = game_state.characters[a.character_id_target].health  # Health of human in question

        #         if health < least_health:  # If they have less health, they are the new patient!
        #             human_target = a
        #             least_health = health

        #         if human_target:  # Give the human a cookie
        #             print("added human to heal list")
        #             print("target:"+str(human_target.character_id_target)+"medic"+str(human_target.executing_character_id))
        #             choices.append(human_target)
                
        #     #elif game_state.characters[character_id].class_type == CharacterClassType.BUILDER:
        #         #print("BUILDER FOUND"+str(abilities[0].type))
        #         #choices.append[abilities[0]]
        # #print("done with ability stage")
        return choices
