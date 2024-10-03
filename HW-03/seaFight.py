import random


class ShipPlacementError(Exception):
    pass
class ShipAddError(Exception):
    pass
class MoveError(Exception):
    pass




class Dot:

    def __init__(self, x, y, value="o"):
        self.x = x
        self.y = y
        self.v = value

    def __eq__(self, other):
        return self.v is other

    def __str__(self):
        return f"{self.v}"


class Ship:

    def __init__(self, length, d1, d2=None, d3=None):
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        self.l = length  # Длина
        self.n = d3 if d3 else d2 if d2 else d1  # Нос корабля
        self.vect = None if self.l == 1 else "V" if self.n.y != self.d1.y else "H"  # Направление
        self.a = length

    def dots(self):
        res = [self.d1]
        if self.d2:
            res.append(self.d2)
        if self.d3:
            res.append(self.d3)
        return res


class Board:

    def __init__(self, hid):
        self.b = [[Dot(i, j) for i in range(1, 7)] for j in range(1, 7)] # Двумерный список
        self.s = [] # Корабли
        self.hid = hid # Скрыть корабли или нет
        self.l = [] # Живые
        self.check = {0}

    def add_ship(self, ship):
        dots = ship.dots()
        if not self.s:
            self.s.append(ship)
            self.l.append(ship)
            for dot in dots:
                self.b[dot.y - 1][dot.x - 1], self.b[dot.y - 1][dot.x - 1].v = dot, "■"
            self.check.update(((dot.y, dot.x) for dot in self.contour(ship)))
            return None
        for dot in dots:
            if (dot.y, dot.x) in self.check:
                raise ShipPlacementError("Неверное расположение корабля")
        for dot in dots:
            self.b[dot.y - 1][dot.x - 1], self.b[dot.y - 1][dot.x - 1].v = dot, "■"
        self.check.update(((dot.y, dot.x) for dot in self.contour(ship)))
        self.l.append(ship)
        self.s.append(ship)
        return None

    def show(self):
        if self.hid:
            res = "  1 2 3 4 5 6\n"
            for i in range(6):
                res += f"{i + 1} "
                for j in range(6):
                    res += self.b[i][j].v + " "
                res += "\n"
            res = res.replace("■", "o")
            return res
        else:
            res = "  1 2 3 4 5 6\n"
            for i in range(6):
                res += f"{i + 1} "
                for j in range(6):
                    res += self.b[i][j].v + " "
                res += "\n"
            return res
    def out(self, dot):
        if 0 < dot.x < 7 and 0 < dot.y < 7:
            return False
        else:
            return True

    def shot(self, dot):
        if self.out(dot):
            raise MoveError
        if dot.v == "T" or dot.v == "x":
            raise MoveError
        if dot.v == "o":
            dot.v = "T"
            return False
        else:
            dot.v = "x"
            for ship in self.l:
                dots = ship.dots()
                if dot in dots:
                    if ship.a != 1:
                        ship.a -= 1
                        return True
                    else:
                        self.l.remove(ship)
                        self.contour(ship, True)
                        return True

    def contour(self, ship, write=False):
        res = []
        for dot in ship.dots():
            remove_y = [-2, -1, 0]
            remove_x = [-2, -1, 0]
            if dot.x == 1:
                remove_x.remove(-2)
            if dot.x == 6:
                remove_x.remove(0)
            if dot.y == 1:
                remove_y.remove(-2)
            if dot.y == 6:
                remove_y.remove(0)
            for i in remove_y:
                for j in remove_x:
                    res.append(self.b[dot.y + i][dot.x + j])

        if write:
            delete = ship.dots()
            for i, dot in enumerate(res):
                if dot in delete:
                    res.pop(i)
            for dot in res:
                self.b[dot.y - 1][dot.x - 1].v = "T"
            return None
        else:
            return res


class Player:

    def __init__(self, enemy_board, self_board):
        self.B = self_board
        self.E = enemy_board

    def ask(self):
        pass

    def move(self):
        cond = True
        while cond:
            target = self.ask()
            try:
                shot = self.E.shot(target)
            except MoveError:
                print("Попробуй снова!")
            else:
                cond = False
        return shot


class AI(Player):

    def ask(self):
        av = [] # Available
        for line in self.E.b:
            for dot in line:
                if dot.v == "■" or dot.v == "o":
                    av.append(dot)
        res = random.choice(av)
        return self.E.b[res.y - 1][res.x - 1]


class User(Player):

    def ask(self):
        try:
            dot = tuple(map(int, input("Введите координаты! - ").split(",")))
        except TypeError:
            print("Неверные координаты!")
            self.ask()
        else:
            return self.E.b[dot[1] - 1][dot[0] - 1]


class Game:

    def __init__(self):
        self.user_board = Board(False)
        self.ai_board = Board(True)


    def random_board(self):
        self.ai_board = Board(True)
        cnt = 6

        choose = [self.ai_board.b[i][j] for j in range(4) for i in range(4)]
        v = ("V", "H")
        v = v[random.randint(0, 1)]
        target = random.choice(choose)
        self.ai_board.add_ship(Ship(3, target, Dot(target.x + 1 if v == "H" else target.x, target.y + 1 if v == "V" else target.y),
                        Dot(target.x + 2 if v == "H" else target.x, target.y + 2 if v == "V" else target.y)))

        choose = [self.ai_board.b[i][j] for j in range(5) for i in range(5)]
        while True:
            try:
                v = ("V", "H")
                v = v[random.randint(0, 1)]
                target = random.choice(choose)
                self.ai_board.add_ship(Ship(2, target,
                                 Dot(target.x + 1 if v == "V" else target.x, target.y + 1 if v == "H" else target.y)))
            except ShipPlacementError:
                choose.remove(target)
            else:
                cnt -= 1
                if cnt == 4:
                    break

        choose = [self.ai_board.b[i][j] for j in range(6) for i in range(6)]
        while cnt != 0:
            if len(choose) == 0:
                self.random_board()
                break
            try:
                v = ("V", "H")
                v = v[random.randint(0, 1)]
                target = random.choice(choose)
                self.ai_board.add_ship(Ship(1, target))
            except ShipPlacementError:
                choose.remove(target)
            else:
                cnt -= 1
                if not cnt:
                    break

    def great(self):
        print(" {---} Здравствуйте, игроки в \"Морской бой!\",\n",
              "В этой игре нужно потопить все корабли противника, при этом сохранив свои -\n",
              "доску противника вы не видите и стреляете наугад.\n",
              "---\n",
              "{---} Сначала ходите вы, затем противник. Если вы попадаете в корабль, то у вас\n",
              "есть право на следующий ход, а при подбитии всего корабля он признаётся \"Убитым\"\n",
              "Тот, кто первый потопит все корабли противника - выиграет!\n",
              "---\n",
              "{---} Формат ввода хода - \"Координата Х,Координата Y\" (без пробелов)\n")

        input("Для начала игры введите ENTER")

        print("Расставьте свои корабли:")
        av = {3:1, 2:2, 1:4}
        print(self.user_board.show(),
              '''Формат ввода корабля - Длина:Координаты Х первой клетки,Координаты Y второй клетки:...
               (вводить без пробелов)''')
        while True:
            try:
                sh = input().split(":")
                sh[0] = int(sh[0])

                if av.get(sh[0]) == 0:
                    raise ShipAddError
                if len(sh[1:]) != sh[0]:
                    raise ShipAddError

                dots = [Dot(int(d[0]), int(d[2])) for d in sh[1:]]
                if len(dots) == 3:
                    self.user_board.add_ship(Ship(sh[0], dots[0], dots[1], dots[2]))
                elif len(dots) == 2:
                    self.user_board.add_ship(Ship(sh[0], dots[0], dots[1]))
                else:
                    self.user_board.add_ship(Ship(sh[0], dots[0]))
            except ShipAddError:
                print("Неверный ввод данных корабля")
            except ShipPlacementError:
                print("Неверное расположение корабля (клетка занята)")
            else:
                av[sh[0]] -= 1
            if all([av.get(1) == 0,
                   av.get(2) == 0,
                   av.get(3) == 0]):
                break
            print(self.user_board.show())


    def loop(self):
        self.random_board()
        self.user = User(enemy_board=self.ai_board, self_board=self.user_board)
        self.ai = AI(enemy_board=self.user_board, self_board=self.ai_board)
        while True:
            print("Ваша доска:")
            print(self.user_board.show())
            print("Доска противника:")
            print(self.ai_board.show())

            while True:
                if not self.user.move():
                    break
                if not self.ai_board.l:
                    winner = "User"
                    break
                print("Вы попали! Повторите ход!")
                print(self.ai_board.show())

            if not self.ai_board.l:
                winner = "User"
                break

            while True:
                if not self.ai.move():
                    break
                if not self.user_board.l:
                    winner = "AI"
                    break

            if not self.user_board.l:
                winner = "AI"
                break

        print("---\n"
              "Игра завершена\n!"
              f"Победитель - {winner}")

    def start(self):
        self.great()
        self.loop()


game = Game()

game.start()
