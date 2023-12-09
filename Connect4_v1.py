import random
import time
import copy
import json

class Connect4:
   def __init__(self):
       self.board = [[0 for _ in range(7)] for _ in range(6)]
       self.current_player = 1

   def drop_piece(self, column,result=[]):
       for row in range(5, -1, -1):
           if self.board[row][column] == 0:
               result.append([self.current_player,(row,column)])
               self.board[row][column] = self.current_player
               return True
       return False

   def check_win(self):
       # Check horizontally
       for row in range(6):
           for col in range(4):
               if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == self.board[row][col + 3] != 0:
                   return True

       # Check vertically
       for col in range(7):
           for row in range(3):
               if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][col] != 0:
                   return True

       # Check diagonally (/)
       for row in range(3):
           for col in range(4):
               if self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == self.board[row + 3][col + 3] != 0:
                   return True

       # Check diagonally (\)
       for row in range(3, 6):
           for col in range(4):
               if self.board[row][col] == self.board[row - 1][col + 1] == self.board[row - 2][col + 2] == self.board[row - 3][col + 3] != 0:
                   return True

       return False

   def print_board(self):
       for row in self.board:
           print(' '.join(str(cell) for cell in row))

def play_game():
   game = Connect4()
   while True:
        game.print_board()

        if game.current_player == 1:
            col = int(input("Player " + str(game.current_player) + ", choose a column to drop your piece: "))
        elif game.current_player == 2:
            start_time = time.time()
            f = open("results_v1.json","w",encoding="utf-8")
            r = dict()
            r[1] = []
            r[2] = []            
            while (time.time() - start_time) <= 4:
                #print("hi")
                game_temp = copy.deepcopy(game)
                result = []
                while True:
                    col = random.randint(0,6)

                    if not game_temp.drop_piece(col,result):
                        continue

                    if game_temp.check_win():
                        r[game_temp.current_player].append(result)
                        break
                    else:
                        n = 0
                        for row in game_temp.board:
                            if 0 in row:
                                n += 1
                        if n == 0:
                            break
                    game_temp.current_player = 2 if game_temp.current_player == 1 else 1
            r = json.dumps(r)
            f.write(r)
            f.close()

            b = read_result()
            temp = 0
            col = 0
            for r in range(6):
                for c in range(7):
                    if b[r][c] > temp:
                        temp = b[r][c]
                        col = c


            
        #col = int(input("Player " + str(game.current_player) + ", choose a column to drop your piece: "))

        if not game.drop_piece(col):
            continue
        print()

        if game.check_win():
            game.print_board()
            print("Player " + str(game.current_player) + " wins!")
            break

        game.current_player = 2 if game.current_player == 1 else 1

def read_result():
    b = [[0 for _ in range(7)] for _ in range(6)]

    results = open("results_v1.json",encoding="utf-8")
    results = json.loads(results.read())

    for game in results["2"]:
        row = game[0][1][0]
        col = game[0][1][1]
        b[row][col] += 1

    for row in range(6):
        for col in range(7):
            b[row][col] /= (len(results["1"]) + len(results["2"]))

    return b

    
play_game()