from simulation import Simulation
from experiment import Experiment
from numpy import random

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # PARAMETERS
    epochs = 10
    block_interval = 210
    starting_stake_per_node = 32
    number_of_nodes = 100
    T = epochs*block_interval #timesteps
    R = 1000000

    runs = 10
    rng = random.RandomState(42)
    random.seed(42)

    steps = block_interval * epochs
    nodes = []

    for i in range(number_of_nodes):
        nodes.append(starting_stake_per_node)


    def handler(experiment):
        sim = Simulation(nodes, block_interval, R, T )
        sim.run(steps=steps, should_print_intermediate_states=False, experiment=experiment)

    experiment = Experiment(block_interval, epochs, run_handler=handler)
    experiment.run(10)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

