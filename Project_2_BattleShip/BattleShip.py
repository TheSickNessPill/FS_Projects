import time
import random as rd
import os

N = 6
M = 6

EMPTY_CELL = " "
SHIP_CELL = "■"
MISS_CELL = "T"
HIT_CELL = "X"
POSITIONS = [
    (-1, 0), (1, 0),
    (0, -1), (0, 1)
]
SHIP_SIZE_LIST = [3,2,2,1,1,1,1]


def clear_console() -> None:
    os.system('cls' if os.name=='nt' else 'clear')


class Ship:
    """ """
    def __init__(self, size, coordinates):
        self.__size = size
        self.__coordinates = coordinates

    @property
    def size(self):
        return self.__size

    @property
    def coordinates(self):
        return self.__coordinates


class ShipFactory:
    """ """
    @staticmethod
    def get_index_ship(coordinates):
        x = coordinates[0]
        y = coordinates[1]

        return (x - 1) * N + y - 1

    @staticmethod
    def is_conflict_ships(ship, indexes):
        ship_coords =ship.coordinates

        ship_status_list = []
        for coord in ship_coords:
            (x, y) = coord
            ship_ind = ShipFactory().get_index_ship(coord)
            if indexes[ship_ind] == " ":

                part_status_list = []
                for pos in POSITIONS:
                    if (1 <= x + pos[0] <= 6 and
                         1 <= y + pos[1] <= 6
                    ):
                        area_ind = ShipFactory().get_index_ship(
                            (x + pos[0], y + pos[1])
                        )
                        if indexes[area_ind] == " ":
                            part_status_list.append(True)
                        else:
                            return True

                if all(part_status_list):
                    ship_status_list.append(True)
            else:
                return True

        if all(ship_status_list):
            for coord in ship_coords:
                ship_ind = ShipFactory().get_index_ship(coord)
                indexes[ship_ind] = SHIP_CELL
            return False
        else:
            return True

    @staticmethod
    def check_area_player():
        ship_list = []
        temp_map = Map()

        for n, ship_size in enumerate(SHIP_SIZE_LIST):
            clear_console()
            print(temp_map.battle_map)
            print(f"КОРАБЛЬ №{n + 1}")
            ship = ShipFactory().create_chip_player(ship_size)
            if not ShipFactory().is_conflict_ships(ship, temp_map.map_indexes):
                ship_list.append(ship)
            else:
                raise ValueError("Корабль должен быть на расстоянии 1й пустой клетки друг от друга.")
        return ship_list

    @staticmethod
    def check_area_ai():
        ship_list = []
        temp_map = Map()

        for i in SHIP_SIZE_LIST:
            stop_while = False

            while not stop_while:
                ship = ShipFactory().create_chip_ai(i)
                if not ShipFactory().is_conflict_ships(ship, temp_map.map_indexes):
                    ship_list.append(ship)
                    stop_while = not stop_while

        return ship_list

    @staticmethod
    def create_chip_player(size):
        inp_text = f"Введите координаты для корабля на {size} кл.\n\
'X Y' - если 1 клетка\n\
'X Y, X Y, ...' - если больше 2х"
        print(inp_text)

        while True:
            input_ = input("Ввод: ").split(",")
            if len(input_) == size:
                break
            print("Введите координаты ещё раз.")

        for i in range(len(input_)):
            coords = input_[i].strip().split(" ")
            if (all(map(str.isnumeric, coords)) and
                 len(coords) == 2
            ):
                input_[i] = tuple(map(int, coords))

        for coords in input_:
            if (1 <= coords[0] <= N and
                 1 <= coords[1] <= M):
                continue
            else:
                raise ValueError("Такой клетки нет на поле")

        if len(input_) > 1:
            res = False

            for pos in POSITIONS:
                temp_list = []
                x = input_[0][0]
                y = input_[0][1]
                for i in range(size):
                    temp_list.append((x, y))
                    x = x + pos[0]
                    y = y + pos[1]

                if input_ == temp_list:
                    res = not res
                    break
            if not res:
                 raise ValueError("Корабль должен быть прямым")

        return Ship(size, input_)

    @staticmethod
    def create_chip_ai(size):
        ship_coords = []

        x_start = rd.randint(1, N)
        y_start = rd.randint(1, M)

        ship_coords.append((x_start, y_start))
        if size > 1:
            stop_while = False
            while not stop_while:
                direction = rd.choice(POSITIONS)
                temp_coords = []

                x = x_start
                y = y_start

                for i in range(size - 1):
                    x += direction[0]
                    y += direction[1]

                    if (1 <= x <= N and
                         1 <= y <= M):
                        temp_coords.append((x, y))
                    else:
                        break
                else:
                    ship_coords = ship_coords + temp_coords
                    stop_while = not stop_while

        return Ship(size, ship_coords)

class Map:
    """ """
    def __init__(self, ships_list=[]):
        self.__map_indexes = [EMPTY_CELL for i in range(N * M)]
        self.__map_disguise = [EMPTY_CELL for i in range(N * M)]
        self.__ships_list = ships_list

        self.__map = self.__spawn_map()
        self.__set_ships_on_map()

    def __spawn_map(self):
        return "\
 _ _|_1_|_2_|_3_|_4_|_5_|_6_|\n\
|_1_| {} : {} : {} : {} : {} : {} |\n\
|_2_| {} : {} : {} : {} : {} : {} |\n\
|_3_| {} : {} : {} : {} : {} : {} |\n\
|_4_| {} : {} : {} : {} : {} : {} |\n\
|_5_| {} : {} : {} : {} : {} : {} |\n\
|_6_|_{}_:_{}_:_{}_:_{}_:_{}_:_{}_|"

    @property
    def battle_map(self):
        return self.__map.format(*self.__map_indexes)

    @property
    def map_indexes(self):
        return self.__map_indexes

    @battle_map.setter
    def battle_map(self, values):
        if len(values) == N * M:
            self.__map_indexes = values
        else:
            raise ValueError("Кол-во значений не равно кол-ву клеток")

    @property
    def disguise_indexes(self):
        return self.__map_disguise

    @property
    def disguise_map(self):
        return self.__map.format(*self.__map_disguise)

    @disguise_map.setter
    def disguise_map(self, values):
        if len(values) == N * M:
            self.__map_disguise = values
        else:
            raise ValueError("Кол-во значений не равно кол-ву клеток")

    @property
    def ships_list(self):
        return self.__ships_list

    def __set_ships_on_map(self):
        if len(self.__ships_list) == len(SHIP_SIZE_LIST):
            for ship in self.__ships_list:
                for coord in ship.coordinates:
                    index = ShipFactory().get_index_ship(coord)
                    self.__map_indexes[index] = SHIP_CELL


class Player:
    """ """
    def __init__(self, name):
        self.__name = name
        self.__steps_list = []
        self.__turn_to_go = False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def steps_list(self):
        return self.__steps_list

    @steps_list.setter
    def steps_list(self, step):
        self.__steps_list.append(step)

    @property
    def turn_to_go(self):
        return self.__turn_to_go

    @turn_to_go.setter
    def turn_to_go(self, value):
        if isinstance(value, bool):
            self.__turn_to_go = value
        else:
            raise ValueError("Переданный объект не является типом 'bool'.")


class BattleShip:
    """ """
    def __init__(
        self,
        map_player, player,
        map_ai, ai
    ):
        self.__map_player = map_player
        self.__player = player

        self.__map_ai = map_ai
        self.__ai = ai

    def __interface(self):
        clear_console()
        print(f"Игрок: {self.__player.name}")
        print(self.__map_player.battle_map)
        print(f"Ходы: {self.__player.steps_list}")
        print("")
        print(f"Игрок: {self.__ai.name}")
        print(self.__map_ai.disguise_map)
        print(f"Ходы: {self.__ai.steps_list}")

    def __get_curr_player(self):
        return self.__player.name if self.__player.turn_to_go else self.__ai.name

    def __handle_move(self):
        print(f"\nОчередь игрока: {self.__get_curr_player()}")
        if self.__player.turn_to_go:
            inp_text = "\nВведите координаты клетки 'X Y'\nВвод: "
            input_ = input(inp_text).strip().split(" ")
            input_ = tuple(map(int, input_))
            map_index = ShipFactory().get_index_ship(input_)

            cell = self.__map_ai.map_indexes[map_index]
            if cell not in [HIT_CELL, MISS_CELL]:
                self.__player.steps_list = input_
                if cell == SHIP_CELL:
                    self.__map_ai.map_indexes[map_index] = HIT_CELL
                    self.__map_ai.disguise_indexes[map_index] = HIT_CELL
                    print("ПОПАДАНИЕ!! Ходите ещё раз")
                if cell == EMPTY_CELL:
                    self.__map_ai.map_indexes[map_index] = MISS_CELL
                    self.__map_ai.disguise_indexes[map_index] = MISS_CELL

                    self.__player.turn_to_go = not self.__player.turn_to_go
                    self.__ai.turn_to_go = not self.__ai.turn_to_go
                    print("ПРОМАХ!! Ход переходит противнику")
                time.sleep(2)
        else:
            input_ = (rd.randint(1, N), rd.randint(1, M))
            map_index = ShipFactory().get_index_ship(input_)
            cell = self.__map_player.map_indexes[map_index]

            if cell not in [HIT_CELL, MISS_CELL]:
                self.__ai.steps_list = input_
                if cell == SHIP_CELL:
                    self.__map_player.map_indexes[map_index] = HIT_CELL
                    self.__map_player.disguise_indexes[map_index] = HIT_CELL
                    print("ПОПАДАНИЕ!! Ходите ещё раз")
                if cell == EMPTY_CELL:
                    self.__map_player.map_indexes[map_index] = MISS_CELL
                    self.__map_player.disguise_indexes[map_index] = MISS_CELL

                    self.__player.turn_to_go = not self.__player.turn_to_go
                    self.__ai.turn_to_go = not self.__ai.turn_to_go
                    print("ПРОМАХ!! Ход переходит противнику")
                time.sleep(2)

    def start(self):
        self.__player.turn_to_go = True if rd.random() > 0.5 else False
        self.__ai.turn_to_go = not self.__player.turn_to_go

        while True:
            if SHIP_CELL not in self.__map_player.map_indexes:
                clear_console()
                print(self.__interface())
                print(f"ПОБЕДА ИГРОКА: {self.__player.name}")
                time.sleep(5)
                break
            if SHIP_CELL not in self.__map_ai.map_indexes:
                clear_console()
                print(self.__interface())
                print(f"ПОБЕДА ИГРОКА: {self.__ai.name}")
                time.sleep(5)
                break

            self.__interface()
            print("")
            self.__handle_move()


if __name__ == "__main__":
    clear_console()
    print("Добро пожаловать в Морской Бой!!!")
    input_ = input("Введите своё имя: ").strip()

    player = Player(input_)
    ship_list_player = ShipFactory().check_area_player()
    map_player = Map(ships_list=ship_list_player)

    ai = Player("AI")
    ship_list_ai = ShipFactory().check_area_ai()
    map_ai = Map(ships_list=ship_list_ai)

    battle_ship = BattleShip(
        map_player=map_player,
        player=player,

        map_ai=map_ai,
        ai=ai
    )

    while True:
        battle_ship.start()
        answer = input("\nХотите ли вы сыграть ещё раз? (1 - да, 0 - нет): ")
        if answer in ["0", "1"]:
            if not int(answer):
                break
