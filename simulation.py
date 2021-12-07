from numpy import median
import numpy as np
from itertools import accumulate
from bisect import bisect
from node import Node
from tester import Tester
import random
import csv
import time


class Simulation:

    def __init__(self, stake_distribution, block_interval,  R, T):
        self.number_of_nodes = 0
        self.nodes = []
        self.blocks = 0
        self.block_interval = block_interval
        self.initial_stakes = []
        self.R = R
        self.T = T

        for stake in stake_distribution:
                validator = Node(self.number_of_nodes, stake)

                self.number_of_nodes += 1
                self.nodes.append(validator)

        total_stake = self.get_total_stake()

        for node in self.nodes:
            node.set_initial_fractional_stake(total_stake)

    def selection_of_proposer(self,nodes):
        weights = []
        for node in nodes:
            weights.append(node.stake)
        prop = random.choices(nodes, weights)
        return prop[0]

    def get_total_stake(self):
        return sum([node.stake for node in self.nodes])

    def stakes(self):
        stakes = []
        stakes.append([node.stake for node in self.nodes])
        return stakes

    def propotional_sampling(self, nodes):
        # calculate cumulative sum from A:
        A = []
        for node in nodes:
            A.append(node.stake/self.get_total_stake())
        cum_sum = [*accumulate(A)]

        i = random.random()                     # i = [0.0, 1.0)
        idx = bisect(cum_sum, i*cum_sum[-1])    # get index to list A
        return idx

    def generate_reward(self, step, R, T):
        #geometric reward
        reward = (1+R)**(step/T)-(1+R)**((step-1)/T)
            
        return reward

    def run(self, steps, should_print_intermediate_states, experiment=None):
        # self.print_state(0)
        run_at_time=time.time()

        #calculate equitability for abitrary party:
        product_second_term = 1

        for step in range(1, steps + 1):
            proposer = self.selection_of_proposer(self.nodes)
            reward = self.generate_reward(step, self.R, self.T)
            prev=proposer.stake
            proposer.stake += reward

            #calculate equitability for abitrary party:
            #S(n) total stake at n

            if step == 1:
                total_stake_step = self.get_total_stake()
            else:
                total_stake_step_minus_1 = total_stake_step
                total_stake_step = self.get_total_stake()
                product_second_term = total_stake_step/total_stake_step_minus_1*product_second_term

            if should_print_intermediate_states:
                pass
                self.print_state(step)

            experiment.collect(
                Tester.gini_coefficient(self.nodes),
                Tester.equitability(self.nodes),
                1 + step // self.block_interval,
                reward,
                self.get_total_stake()/self.number_of_nodes,
                median(self.stakes()),
                np.std(self.stakes())
            )
            with open('all_values_per_tick_geometric.csv', mode='a') as value_file:
                value_writer = csv.writer(value_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = '\n')
                value_writer.writerow([run_at_time, step, Tester.gini_coefficient(self.nodes), Tester.equitability(self.nodes), reward, self.get_total_stake()/self.number_of_nodes, median(self.stakes()),np.std(self.stakes())])

            total_stake = self.get_total_stake()

            [node.update_fractional_stake(total_stake) for node in self.nodes]

        if not should_print_intermediate_states:
            self.print_state(steps)
            pass

    def print_state(self, step):
        print()
        print("POS_CONSTANT")
        print(f'Step #{step}:')
        print()

        print(f'Total stake {self.get_total_stake()}')
        print(f'Equitability = {Tester.equitability(self.nodes)}')
        print(f"Gini coefficient = {Tester.gini_coefficient(self.nodes)}")
        print()

        print()
        print('----------------')
