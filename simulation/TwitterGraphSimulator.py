class TwitterGraphSimulator:
    def __init__(self, avg_num_following, max_iterations):
        """
        Initialize the TwitterGraphSimulator with average number of followers and maximum iterations.

        Parameters:
        avg_num_following (float): Average number of followers a user follows.
        max_iterations (int): Maximum number of iterations for simulation.
        """
        self.avg_num_following = avg_num_following
        self.max_iterations = max_iterations
    
    def simulate(self, names):
        """
        Simulate a Twitter-like graph.

        Parameters:
        names (pandas DataFrame or Series): A collection of user names.

        Returns:
        tuple: A tuple containing nodes, edges, iterations, lengths_nodes, and lengths_edges.
        """
        import numpy as np  # Import numpy for random number generation

        # Initialize sets to store nodes and edges
        nodes = set([names.mode().values[0]])
        edges = set()

        # Initialize lists to store iteration counts, node lengths, and edge lengths
        iterations = []
        lengths_nodes = []
        lengths_edges = []

        # Iterate through the simulation process
        for i in range(self.max_iterations):
            iterations.append(i)  # Store the current iteration count
            lengths_nodes.append(len(nodes))  # Store the current number of nodes
            lengths_edges.append(len(edges))  # Store the current number of edges
            
            new_nodes = set()  # Initialize a set to store new nodes for the current iteration
            for node in nodes:
                # Generate a random number of following based on a normal distribution
                random_float = np.random.normal(loc=self.avg_num_following - len(nodes)*(0.6/(i+1)), scale=4)
                random_following_num = max(int(round(random_float)), 10)  # Ensure a minimum of 10 following
                following_nodes = names.sample(random_following_num)  # Sample random following nodes from names
                for following in following_nodes:
                    edges.add((node, following))  # Add edges between current node and following nodes
                new_nodes = new_nodes.union(following_nodes)  # Add following nodes to the new_nodes set
            nodes = nodes.union(new_nodes)  # Update the set of nodes with new nodes
        
        return nodes, edges, iterations, lengths_nodes, lengths_edges  # Return simulation results