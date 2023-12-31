import random
import time
import copy
import json
import statistics

class Connect4:
   def __init__(self):
       self.board = [[0 for _ in range(7)] for _ in range(6)]
       self.current_player = 1

   def drop_piece(self, column,result=[]):
       for row in range(5, -1, -1):
           try:
                if self.board[row][column] == 0:
                    result.append([self.current_player,(row,column)])
                    self.board[row][column] = self.current_player
                    return True
           except:
               print("Not a Valid Input")
               print()
               return False
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

class Analyse:
    def __init__(self,col):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.col = col


def play_game():
   game = Connect4()
   while True:
        game.print_board()

        if game.current_player == 1:
            col = int(input("Player " + str(game.current_player) + ", choose a column to drop your piece: "))
        elif game.current_player == 2:
            start_time = time.time()
            f = open("results_v3.json","w",encoding="utf-8")
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

            condition = True
            col = 0 
            for c in range(7):
                game_temp1 = copy.deepcopy(game)
                game_temp1.current_player = 1
                if game_temp1.drop_piece(c):
                    # print()
                    # game_temp1.print_board()
                    # print(game_temp1.check_win())
                    if game_temp1.check_win():
                         col = c
                         condition = False
                         break
            
            l = []
            for c in range(7):
                game_temp2 = copy.deepcopy(game)
                game_temp2.current_player = 2
                if game_temp2.drop_piece(c):
                    if game_temp2.check_win():
                        continue
                    game_temp2.current_player = 1
                    if game_temp2.drop_piece(c):
                        if game_temp2.check_win():
                            l.append(c)

            if condition:
                col = read_result(l)
            print()
            print("AI Placed In Column "+str(col))

        #col = int(input("Player " + str(game.current_player) + ", choose a column to drop your piece: "))

        if not game.drop_piece(col):
            continue
        print()

        if game.check_win():
            game.print_board()
            print()
            print("Player " + str(game.current_player) + " wins!")
            break
        else:
            n = 0
            for row in game.board:
                if 0 in row:
                    n += 1
            if n == 0:
                print("It's A Tie")
                break

        game.current_player = 2 if game.current_player == 1 else 1


def read_result(l):
    analyze_boards = []
    for b in range(7):
        analyze_boards.append(Analyse(b))

    results = open("results_v3.json",encoding="utf-8")
    results = json.loads(results.read())

    for game in results["2"]:
        row = game[0][1][0]
        col = game[0][1][1]
        b = analyze_boards[col].board
        b[row][col] += 1
        for play in game[1:]:
            if play[0] == 2:
                b[play[1][0]][play[1][1]] += 1

    # print()
    # for b in analyze_boards:
    #     for row in b.board:
    #         print(row)
    #     print()

    total_games = [0 for _ in range(7)]
    for i in range(7):
        for g1 in results["1"]:
            if g1[0][1][1] == i:
                total_games[i] += 1
        for g2 in results["2"]:
            if g2[0][1][1] == i:
                total_games[i] += 1

    # print(total_games)

    i = 0
    for board in analyze_boards:
        b = board.board
        for row in range(6):
            for col in range(7):
                try:
                    b[row][col] /= total_games[i]
                except:
                    pass
        #analyze_boards[i] = b
        i += 1

    # print()
    # for b in analyze_boards:
    #     for row in b.board:
    #         print(row)
    #     print()

    over_70 = []
    col = 0
    for board in analyze_boards:
        b = board.board
        for row in range(5, -1, -1):
            if b[row][col] != 0:
                if b[row][col] >= 0.70:
                    over_70.append(col)
                break
        col += 1


    col = 0
    c3 = 0
    tem = 0
    v = 0
    for board in analyze_boards:
        b = board.board
        if col in l:
            col += 1
            continue
        for row in range(5, -1, -1):
            if b[row][col] != 0 and b[row][col] > tem:
                tem = b[row][col]
                c3 = col
                break
            elif b[row][col] != 0 and b[row][col] == tem:
                count = 0
                count_max = 0
                for a in analyze_boards[c3].board:
                    for bn in a:
                        if bn == 0:
                            count += 1
                
                for a in analyze_boards[col].board:
                    for bn in a:
                        if bn == 0:
                            count_max += 1
                
                if count_max > count:
                    c3 = col
                    v = b[row][col]
        col += 1

    if v == 1 or tem == 1:
        return c3


    for board in analyze_boards:
        b_temp = [[0 for _ in range(7)] for _ in range(6)]
        # b = board.board
        for row in range(6):
            for col in range(7):
                val = board.board[row][col]
                if val != 0:
                    total = 0
                    denominator = 1
                    for r in board.board:
                        for v in r:
                            if v != 0:
                                total += val - v
                                denominator += 1
                    if total == 0:
                        b_temp[row][col] = val
                    else:
                        b_temp[row][col] = total/denominator
        board.board = b_temp
                            

    # print()
    # for b in analyze_boards:
    #     for row in b.board:
    #         print(row)
    #     print()

    temp = 0
    c = 0
    col = 0
    v = 0
    for board in analyze_boards:
        b = board.board
        if col in l:
            col += 1
            continue
        for row in range(5, -1, -1):
            if b[row][col] != 0 and b[row][col] > temp:
                temp = b[row][col]
                c = col
                break
            elif b[row][col] != 0 and b[row][col] == temp:
                count = 0
                count_max = 0
                for a in analyze_boards[c].board:
                    for bn in a:
                        if bn == 0:
                            count += 1
                
                for a in analyze_boards[col].board:
                    for bn in a:
                        if bn == 0:
                            count_max += 1
                
                if count_max > count:
                    c = col
                    v = b[row][col]
                    # print(v)

        col += 1
    # print(temp)
    if v == 1 or temp == 1:
        return c


    c2 = 0
    total = 10
    col2 = 0
    for board in analyze_boards:
        if col2 in l:
            col2 += 1
            continue
        if col2 not in over_70:
            col2 += 1
            continue
        total_sub = 0
        b = board.board
        for col in range(7):
            for row in range(5, -1, -1):
                if b[row][col] != 0:
                    if col != col2:
                        total_sub += b[row][col]
                    break
        # print(total_sub)
        if total_sub < total:
            total = total_sub
            c2 = col2
        col2 += 1
    

    # print(over_70)
    # print(total)
    # print()
    # print(c3)
    # print(c)
    # print(c2)
    # print()

    if len(over_70) == 0:
        if c == c3:
            return c
        else:
            return c3
    else:
        if statistics.mode([c,c2,c3]) == c and c != c2 and c != c3:
            return c2
        if total < 0:
            return c2
        else:
            return c
    
play_game()