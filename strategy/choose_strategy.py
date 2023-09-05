from strategy.random_strategy import RandomStrategy
from strategy.strategy import Strategy


def choose_strategy(is_zombie: bool) -> Strategy:
    # Modify what is returned here to select the strategy your bot will use
    # NOTE: You can use "is_zombie" to use two different strategies for humans and zombies (RECOMMENDED!)
    return RandomStrategy()
