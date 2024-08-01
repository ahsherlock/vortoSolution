import helper_classes
import sys


# Create class for solving the problem.
class Solution:

    def __init__(self):
        self.drivers = []
        self.loadByID = {}
        self.depot = helper_classes.Cartesian(0, 0)
        self.max_distance = 12 * 60

    ##loads problem from file
    def load_problem(self, file_path):
        loads = helper_classes.loadFromFile(file_path)
        for load in loads:
            self.loadByID[int(load.id)] = load

    def compute_savings(self):
        savings = []
        for i in self.loadByID:
            for j in self.loadByID:
                if i != j:
                    load1 = self.loadByID[i]
                    load2 = self.loadByID[j]
                    key = (i, j)
                    saving = (key, helper_classes.EuclideanDistance(load1.dropoff, self.depot)
                              + helper_classes.EuclideanDistance(self.depot, load2.pickup)
                              - helper_classes.EuclideanDistance(load1.dropoff, load2.pickup))
                    savings.append(saving)

        savings = sorted(savings, key=lambda x: x[1], reverse=True)

        return savings

    def compute_distance(self, nodes):

        if not nodes:
            return 0.0

        distance = 0.0
        for i in range(len(nodes)):
            distance += nodes[i].delivery_distance
            if i != (len(nodes) - 1):
                distance += helper_classes.EuclideanDistance(nodes[i].dropoff, nodes[i + 1].pickup)

        distance += helper_classes.EuclideanDistance(self.depot, nodes[0].pickup)
        distance += helper_classes.EuclideanDistance(nodes[-1].dropoff, self.depot)

        return distance

    def print_solution(self):

        for driver in self.drivers:
            print([int(load.id) for load in driver.route])

    # calculates the all the required data
    def compute_answers(self):
        savings = self.compute_savings()

        for link, _ in savings:

            load1 = self.loadByID[link[0]]
            load2 = self.loadByID[link[1]]
            if not load1.assigned and not load2.assigned:

                # checking for the constraints
                cost = self.compute_distance([load1, load2])
                if cost <= self.max_distance:
                    driver = helper_classes.Driver()
                    driver.route = [load1, load2]
                    self.drivers.append(driver)
                    load1.assigned = driver
                    load2.assigned = driver
            elif load1.assigned and not load2.assigned:

                driver = load1.assigned
                i = driver.route.index(load1)
                # if node is the last node of route
                if i == len(driver.route) - 1:
                    # check constraints
                    cost = self.compute_distance(driver.route + [load2])
                    if cost <= self.max_distance:
                        driver.route.append(load2)
                        load2.assigned = driver

            elif not load1.assigned and load2.assigned:

                driver = load2.assigned
                i = driver.route.index(load2)
                # if node is the first node of route
                if i == 0:
                    # check constraints
                    cost = self.compute_distance([load1] + driver.route)
                    if cost <= self.max_distance:
                        driver.route = [load1] + driver.route
                        load1.assigned = driver
            else:

                driver1 = load1.assigned
                i1 = driver1.route.index(load1)

                driver2 = load2.assigned
                i2 = driver2.route.index(load2)
                if (i1 == len(driver1.route) - 1) and (i2 == 0) and (driver1 != driver2):
                    cost = self.compute_distance(driver1.route + driver2.route)
                    if cost <= self.max_distance:
                        driver1.route = driver1.route + driver2.route
                        for load in driver2.route:
                            load.assigned = driver1

                        self.drivers.remove(driver2)

        # Assign all unassigned drivers to remaining routes
        for load in self.loadByID.values():
            if not load.assigned:
                driver = helper_classes.Driver(0, [])
                driver.route.append(load)
                self.drivers.append(driver)
                load.assigned = driver


if __name__ == "__main__":
    #check for proper args
    if len(sys.argv) != 2:
        print("Usage: python solution.py <file_path>")
        sys.exit(1)
    #get file path from commandline
    file_path = sys.argv[1]
    #create solution instance
    solution = Solution()
    #load problems from file path
    solution.load_problem(file_path)
    #compute all required data
    solution.compute_answers()
    #print to STDOUT
    solution.print_solution()
