import numpy as np

class Body:
    def __init__(self, mass, x, y):
        self.mass = mass
        self.x = x
        self.y = y

class QuadTreeNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center_x = x + width / 2
        self.center_y = y + height / 2
        self.mass = 0
        self.center_of_mass_x = 0
        self.center_of_mass_y = 0
        self.children = [None, None, None, None]  # NW, NE, SW, SE

    def insert(self, body):
        if self.width <= 1 and self.height <= 1:
            # Leaf node, store the body here
            self.mass += body.mass
            self.center_of_mass_x += body.x * body.mass
            self.center_of_mass_y += body.y * body.mass
        else:
            # Non-leaf node, recursively insert into children
            quadrant = self.get_quadrant(body)
            if self.children[quadrant] is None:
                self.children[quadrant] = self.create_child(quadrant)
            self.children[quadrant].insert(body)

    def get_quadrant(self, body):
        if body.x < self.center_x:
            if body.y < self.center_y:
                return 0  # NW
            else:
                return 2  # SW
        else:
            if body.y < self.center_y:
                return 1  # NE
            else:
                return 3  # SE

    def create_child(self, quadrant):
        if quadrant == 0:  # NW
            return QuadTreeNode(self.x, self.y, self.width / 2, self.height / 2)
        elif quadrant == 1:  # NE
            return QuadTreeNode(self.center_x, self.y, self.width / 2, self.height / 2)
        elif quadrant == 2:  # SW
            return QuadTreeNode(self.x, self.center_y, self.width / 2, self.height / 2)
        else:  # SE
            return QuadTreeNode(self.center_x, self.center_y, self.width / 2, self.height / 2)

def calculate_force(node, body, theta):
    dx = node.center_of_mass_x - body.x
    dy = node.center_of_mass_y - body.y
    distance = np.sqrt(dx**2 + dy**2)

    if distance == 0:
        return 0, 0  # Avoid division by zero

    if node.width / distance < theta:
        # Far enough, approximate with a single force
        force = G * node.mass / distance**2
        fx = force * dx / distance
        fy = force * dy / distance
        return fx, fy

    # Recurse into children
    fx, fy = 0, 0
    for child in node.children:
        if child is not None:
            cfx, cfy = calculate_force(child, body, theta)
            fx += cfx
            fy += cfy

    return fx, fy

# Constants
G = 6.67430e-11  # Gravitational constant
theta = 0.5  # Barnes-Hut parameter

# Create bodies and a root node for the quad tree
bodies = [Body(10000, 10, 10), Body(10000, 20, 20)]
root = QuadTreeNode(0, 0, 100, 100)

# Insert bodies into the quad tree
for body in bodies:
    root.insert(body)

# Calculate forces for each body
for body in bodies:
    fx, fy = calculate_force(root, body, theta)
    print(f"Force on body: ({fx}, {fy})")