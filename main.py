# We use ZMQ to talk to the game server. The basic
# communication is set up so you shouldn't need to worry about it much
import zmq
import sys
import random

PORT = 5556

# Connect to the game server,
# Make sure it is running
print("Connecting to server")

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(f'tcp://127.0.0.1:{PORT}')

# Connect to the server using it's API
socket.send_string('start')

def get_board(message):
    board = message.replace('update board ', '').replace('\naction\n', '').replace('\ndone you win!', '').replace('settings your_id x', '').replace('settings your_id o', '').replace('\nsettings board_size 3,3\n', '').replace('\ndone computer wins', '')
    return format_board(board)

def format_board(board):
    rows = board.split(';')
    formatted_rows = []

    for row in rows:
        formatted_rows.append(row.split(','))

    return formatted_rows

def valid_move(board, h, w):
    if board[h][w] == 'x' or board[h][w] == 'o':
        return False
    else:
        return True

# If I had more time I would not make the moves random.
def random_width():
    return random.randint(0,2)

def random_height():
    return random.randint(0,2)

def make_move(message):
    board = get_board(message)
    h = random_height()
    w = random_width()

    is_valid_move = valid_move(board, h, w)

    if is_valid_move == True:
        move = '{}, {}'.format(h, w)
        return move
    else:
        return make_move(message)


# Make this function, using whatever other classes / functions you need
def get_move(message):
    
    move = make_move(message)
    return move

while True:
    sys.stdout.flush()

    # Get the next message from the server. Note that it may be multi-line
    message = socket.recv_string()

    # If the server replies 'done', the game is finished
    if 'done' in message:
        print(message)
        break

    # Message contains game state information,
    # You'll want to parse message and construct
    # a valid response
    reply = get_move(message)

    # Send reply to the server
    socket.send_string(reply)
