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
def _move(game_state: typing.Dict) -> typing.Dict:
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


def move(game_state: typing.Dict) -> typing.Dict:
    
    print(f"MOVE {game_state['turn']}")

    my_head = game_state["you"]["head"]["x"], game_state["you"]["head"]["y"]
    my_target = game_state["board"]["food"][0]["x"], game_state["board"]["food"][0]["y"]

    path = search_path(game_state, my_head, my_target)

    if path is None:
        print("Path not found!")
        return {"move": "down"}
    path_list = list(path)
    print(path_list)

    if len(path_list)>1:
        return {"move": next_direction(my_head, path_list[1])}
    return {"move": "down"}
    

def search_path(game_state: typing.Dict, start, target) -> typing.Union[typing.Iterable[object], None] :
    # Create grid for A*
    height = game_state["board"]["height"]  # rows
    width = game_state["board"]["width"]  # columns
    board = [[0 for _ in range(width)] for _ in range(height)]

    for snake in game_state["board"]["snakes"]:
        for body_piece in snake["body"]:
            x = body_piece['x']
            y = body_piece['y']
            board[x][y] = 1

    for hazard in game_state["board"]["hazards"]:
        x = hazard['x']
        y = hazard['y']
        board[x][y] = 1

    board[game_state["you"]["head"]["x"]][game_state["you"]["head"]["y"]] = 0
    board_graph = create_graph(board)

    path = AStarSearch(board_graph).astar(start, target)
    return path

def next_direction(head, next_square):
    if head[0]>next_square[0]:
        return "left"
    if head[0]<next_square[0]:
        return "right"
    if head[1]>next_square[1]:
        return "down"
    if head[1]<next_square[1]:
        return "up"
    return "None"


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
            if matrix[x][y] == 0:  # Free cell
                current_node = (x, y)
                # Up
                if y < height-1 and matrix[x][y+1] == 0:
                    add_edge(current_node, (x, y+1), 100)

                # Down
                if y > 0 and matrix[x][y-1] == 0:
                    add_edge(current_node, (x, y-1), 100)

                # Left
                if x > 0 and matrix[x-1][y] == 0:
                    add_edge(current_node, (x-1, y), 100)

                # Right
                if x < width-1 and matrix[x+1][y] == 0:
                    add_edge(current_node, (x+1, y), 100)

    return nodes


# Start server when `python main.py` is run
# group 4:29 version
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
