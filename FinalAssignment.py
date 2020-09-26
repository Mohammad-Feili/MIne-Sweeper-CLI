from random import randint
  
global board
global external_board

# This Function Is For Generating Random Numbers



def create_bomb_numers(bomb_count, bomb_range):
    bomb_range_list = set()
    while len(bomb_range_list) < bomb_count:
        bomb_num = randint(0, bomb_range-1)
        if bomb_num not in bomb_range_list:
            bomb_range_list.add(bomb_num)

    return sorted(list(bomb_range_list))

  
# This Function Is For Making A Empty Board


def create_empty_board(row, column):

    board = [[0 for j in range(column)] for i in range(row)]

    return board

# Making The Main Board


def inside_maker(row, column, bomb_count):

    bomb_range = row * column
    bomb_list = create_bomb_numers(bomb_count, bomb_range)

    # Making A Empty Board
    board = create_empty_board(row, column)

    # Substituting The Bombs in Board
    for i in bomb_list:
        row_index = int(i/row)
        col_index = i % column
        board[row_index][col_index] = 'B'

    # Number Assignment To Entries
    for i in range(row):
        for j in range(column):
            if board[i][j] != "B":

                for k in range(row):
                    for l in range(column):
                        if k == i and l == j:
                            continue
                        if (abs(i-k) < 2) and (abs(j-l) < 2):
                            if board[k][l] == "B":
                                board[i][j] += 1

    return board


def outside_maker(row, column):

    board_display = [["X" for j in range(column)] for i in range(row)]

    return board_display


def making_str(board):

    col_index = "  \   "
    for i in range(len(board[0])):
        if len(str(i+1)) == 1:
            col_index += str(i+1) + "  "
        else:
            col_index += str(i+1) + " "

    print(col_index+"\n")
    for i in range(len(board)):
        if len(str(i+1)) == 1:
            board_rows = "  " + str(i+1) + "   "
        else:
            board_rows = "  " + str(i+1) + "  "
        for j in range(len(board[0])):
            board_rows += str(board[i][j])+'  '
        print(board_rows)


# This is For Selecting Empty Entries
def empty_entries(board, coordinates):

    x = coordinates[0]
    y = coordinates[1]

    row = len(board)
    column = len(board[0])

    empty_entry_list = set()
    empty_entry_list.add((x, y))
    new_empty_list = set()

    while new_empty_list != empty_entry_list:
        new_empty_list = {k for k in empty_entry_list}
        for i in range(row):
            for j in range(column):
                for (x, y) in new_empty_list:
                    if (abs(i-x) < 2) and (abs(j-y) < 2):
                        if board[i][j] == 0:
                            empty_entry_list.add((i, j))

    for entry in empty_entry_list:
        external_board[entry[0]][entry[1]] = "E"

    return board


def make_change(board, coordinates, mode):

    i = coordinates[0]
    j = coordinates[1]

    if mode == "U":
        if (0 <= i < len(board[0])) and (0 <= j < len(board)):
            if external_board[i][j] == "F":
                external_board[i][j] = "X"
                return board, True
            else:
                print("This Entry Already Is Not Flag!")
                return board, None
        else:
            print("Matrix Index Out of Range!")
            return board, None

    elif mode == "F":
        if (0 <= i < len(board[0])) and (0 <= j < len(board)):
            if external_board[i][j] == "X":
                external_board[i][j] = "F"
                return board, True
            else:
                print("This Entry Already Chosen!")
                return board, None
        else:
            print("Matrix Index Out of Range!")
            return board, None

    elif mode == "C":
        if (0 <= i < len(board[0])) and (0 <= j < len(board)):
            if external_board[i][j] == "F" or external_board[i][j] != "X":
                print("You Select a Entry That is Flag or Selected!")
                return board, None

            elif board[i][j] == "B":
                print("\nGame Over!\n\tTry Again.")
                return board, False

            elif board[i][j] == 0:
                board = empty_entries(board, (i, j))
                return board, True

            else:
                external_board[i][j] = board[i][j]
                return board, True
        else:
            print("Matrix Index Out of Range!")
            return board, None
    else:
        print("Error :: the Mode of chenge is wrong!")
        return board, None


def check_board(board, external_board):
    flag = True
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0 and external_board[i][j] == "E":
                continue
            elif board[i][j] == "B" and external_board[i][j] == "F":
                continue
            elif board[i][j] == external_board[i][j]:
                continue
            else:
                flag = False
                return False

    return flag


if __name__ == "__main__":

    # In The Begining Of The Game The User(Player) Must Be Choice The Level Of The My Sweeper Game
    print("\nChoice The Level Of The Game ::\n\n1.Easy\n2.Medium\n3.Hard\n")
    entry_command = input("Enter The Level : ")

    if entry_command == "Easy" or entry_command == "easy" or entry_command == "1":
        row = 8
        column = 8
        bomb_count = 10
    elif entry_command == "Medium" or entry_command == "medium" or entry_command == "2":
        row = 16
        column = 16
        bomb_count = 40
    elif entry_command == "Hard" or entry_command == "hard" or entry_command == "3":
        row = 24
        column = 24
        bomb_count = 99

    board = inside_maker(row, column, bomb_count)
    external_board = outside_maker(row, column)
    making_str(external_board)

    while True:
        print("\nEnter The Coordinates and Mode in One Line with Space Delimmiter Respectively ::\n\t")

        entry = input("Enter : ")
        entry = entry.split(' ')

        # Coordinates
        x = int(entry[0]) - 1
        y = int(entry[1]) - 1
        mode = entry[2]

        board, validity = make_change(board, (x, y), mode)

        if validity == False:
            break

        elif validity == None:
            #making_str(board)
            making_str(external_board)
            continue

        elif validity == True:
            if check_board(board, external_board):
                print("You Win.")
                break
            else:
                #making_str(board)
                making_str(external_board)
                continue
