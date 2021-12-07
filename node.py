import uuid

class Node:
    def __init__(self, id: int, initial_stake: float):
        self.id = id
        self.stake = initial_stake
        self.initial_stake = self.stake
        self.initial_fractional_stake = 0
        self.fractional_stake = 0

    def set_initial_fractional_stake(self, total_stake):
        self.initial_fractional_stake = self.initial_stake / total_stake
        self.fractional_stake = self.initial_fractional_stake

    def update_fractional_stake(self, total_stake):
        self.fractional_stake = self.stake / total_stake
