import copy


def is_terminal_move(game_state, snake_id):
    if snake_id is None:
        return False

    if game_state is None:
        return True

    snake_state = game_state["snakes"]

    for snake in snake_state:
        if snake["id"] == snake_id:
            return False
    return True


def eval_state(game_state):
    return 1 # TODO


def update_head_coord(x, y, move):
    if (move == "up"):
        y = y - 1
    elif (move == "down"):
        y = y + 1
    elif (move == "left"):
        x = x - 1
    elif (move == "right"):
        x = x + 1

    return x, y


def is_snake_present(game_state, snake_id):
    snakes = game_state["board"]["snakes"]
    for index, snake in enumerate(snakes):
        if snake["id"] == snake_id:
            return index
    return None


def make_move(game_state, snake_id, move):
    board_width = len(game_state["board"]["state_board"][0])
    board_height = len(game_state["board"]["state_board"])

    new_game_state = copy.deepcopy(game_state)

    snake_index = is_snake_present(game_state, snake_id)
    if snake_index is None:
        return None

    snake_head = (game_state["board"]["snakes"][snake_index]["head"]["x"],
                  game_state["board"]["snakes"][snake_index]["head"]["y"])
    snake_new_head = update_head_coord(snake_head[0], snake_head[1], move)




    return new_game_state



def minimax_run(game_state, depth, evaluating_snake_id, our_snake_id, previous_snake_id, alpha, beta, current_turn):
    if depth == 0 or is_terminal_move(game_state, previous_snake_id):
        return eval_state(game_state)

    # find the ID of the next snake that we are going to minimax
    curr_index = 0
    for index, snake in enumerate(game_state["snakes"]):
        if snake["id"] == evaluating_snake_id:
            curr_index = index
            break

    next_snake_id = game_state["snakes"][(curr_index + 1) % len(game_state["snakes"])]["id"]

    possible_moves = ["up", "down", "right", "left"]

    # maximise our value, opponent minimises
    if evaluating_snake_id == our_snake_id:
        # our move: max
        highest_value = float("-inf")
        best_move = None

        for move in possible_moves:
            new_game_state = make_move(game_state, evaluating_snake_id, move)
            (current_value, _) = minimax_run(new_game_state,
                                             depth - 1,
                                             next_snake_id,
                                             our_snake_id,
                                             evaluating_snake_id,
                                             alpha,
                                             beta,
                                             current_turn + 1)
            if current_value > highest_value:
                best_move = move
                highest_value = current_value

            alpha = max(alpha, current_value)

            if alpha >= beta:
                break

        return highest_value, best_move

    else:
        # opponent's move: min
        lowest_value = float("inf")
        best_move = None
        for move in possible_moves:
            new_game_state = make_move(game_state, evaluating_snake_id, move)
            (current_value, _) = minimax_run(new_game_state,
                                             depth - 1,
                                             next_snake_id,
                                             our_snake_id,
                                             evaluating_snake_id,
                                             alpha,
                                             beta,
                                             current_turn + 1)

            if lowest_value > current_value:
                best_move = move
                lowest_value = current_value

            beta = min(current_value, beta)

            if beta <= alpha:
                break
        return lowest_value, best_move
