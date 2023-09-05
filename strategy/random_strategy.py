import random
from game.character.action.attack_action import AttackAction
from game.character.action.move_action import MoveAction
from game.game_state import GameState
from strategy.strategy import Strategy


class RandomStrategy(Strategy):
    def decide_moves(
        self, possible_moves: dict[str, list[MoveAction]], game_state: GameState
    ) -> list[MoveAction]:
        choices = []

        for [character_id, moves] in possible_moves.items():
            #  NOTE: You will have to handle the case where there is no move to be made, such as when stunned
            if len(moves) == 0:
                continue  # random.choice does not support an empty list of options.
            choices.append(random.choice(moves))

        return choices

    def decide_attacks(
        self, possible_attacks: dict[str, list[AttackAction]], game_state: GameState
    ) -> list[AttackAction]:
        choices = []

        for [character_id, attacks] in possible_attacks.items():
            #  NOTE: You will have to handle the case where there is no move to be made, such as when stunned
            if len(attacks) == 0:
                continue  # random.choice does not support an empty list of options.
            choices.append(random.choice(attacks))

        return choices
