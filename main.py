import random
import typing
from astar import AStar


class AStarSearch(AStar):
    def __init__(self, nodes):
        self.nodes = nodes

    def neighbors(self, n):
        for n1, d in self.nodes[n]:
            yield n1

    def distance_between(self, n1, n2):
        for n, d in self.nodes[n1]:
            if n == n2:
                return d

    def heuristic_cost_estimate(self, current, goal):
        return 1

    def is_goal_reached(self, current, goal):
        return current == goal


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#FFF888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    # board origin: BL

    

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    l_distance = my_head["x"]
    r_distance = board_width - 1 - l_distance
    b_distance = my_head["y"]
    t_distance = board_height - 1 - b_distance

    if my_neck["x"] < my_head["x"] or l_distance == 0:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
        l_distance = 0

    elif my_neck["x"] > my_head["x"] or r_distance == 0:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
        r_distance = 0

    elif my_neck["y"] < my_head["y"] or b_distance == 0:  # Neck is below head, don't move down
        is_move_safe["down"] = False
        b_distance = 0
    elif my_neck["y"] > my_head["y"] or t_distance == 0:  # Neck is above head, don't move up
        is_move_safe["up"] = False
        t_distance = 0

    furthest_move = {l_distance: "left",
                     r_distance: "right",
                     b_distance: "down",
                     t_distance: "up"}.get(max(l_distance, r_distance, b_distance, t_distance))

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    next_move = safe_moves.pop()
    if is_move_safe[furthest_move]:
        next_move = furthest_move

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


def _move(game_state: typing.Dict) -> typing.Dict:

    # Create grid for A*
    #    for i in range(game_state["board"]["height"]):
    #        for j in range(game_state["board"]["width"]):
    height = game_state["board"]["height"]
    width = game_state["board"]["width"]
    board = [[0 for _ in range(width)] for _ in range(height)]
    
    for snake in game_state["board"]["snakes"]:
        for body_piece in snake["body"]:
            x = body_piece['x']
            y = body_piece['y']
            board[y][x] = 1

    for hazard in game_state["board"]["hazards"]:
        x = hazard['x']
        y = hazard['y']
        board[y][x] = 1

    board[game_state["you"]["head"]["x"]][game_state["you"]["head"]["y"]] = 0
    board_graph = create_graph(board)

    my_head = game_state["you"]["head"]["x"], game_state["you"]["head"]["y"]
    my_target = game_state["board"]["food"][0]["x"], game_state["board"]["food"][0]["y"]

    path = AStarSearch(board_graph).astar(my_head, my_target)
    print(path)


def create_graph(matrix):
    height = len(matrix)
    width = len(matrix[0])
    nodes = {}

    def add_edge(node1, node2, cost):
        if node1 in nodes:
            nodes[node1].append((node2, cost))
        else:
            nodes[node1] = [(node2, cost)]

    for y in range(height):
        for x in range(width):
            if matrix[y][x] == 0:  # Free cell
                current_node = (y, x)
                # Up
                if y > 0 and matrix[y - 1][x] == 0:
                    add_edge(current_node, (y - 1, x), 100)
                # Down
                if y < height - 1 and matrix[y + 1][x] == 0:
                    add_edge(current_node, (y + 1, x), 100)
                # Left
                if x > 0 and matrix[y][x - 1] == 0:
                    add_edge(current_node, (y, x - 1), 100)
                # Right
                if x < width - 1 and matrix[y][x + 1] == 0:
                    add_edge(current_node, (y, x + 1), 100)

    return nodes


# Start server when `python main.py` is run
# group 4:29 version
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
