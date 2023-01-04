import os
import sys
import time
import random as rd

combinations = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    #
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    #
    (0, 4, 8),
    (6, 4, 2)
]


def clear_console() -> None:
    os.system('cls' if os.name=='nt' else 'clear')


def make_grid(values: list) -> None:
    print(
        ("  __1___2___3__\n" + \
        "1 |_{0}_|_{1}_|_{2}_|\n" + \
        "2 |_{3}_|_{4}_|_{5}_|\n" + \
        "3 |_{6}_|_{7}_|_{8}_|").format(*values)
    )


def save_data(player: dict, grid_state: list) -> None:
    while True:
        data = input(f"[{player['name']}], введите координаты ячейки X и Y (шаблон 'X Y'): ").split(" ")

        if (all(map(str.isnumeric, data)) and
                len(data) == 2):
            data = (int(data[0]), int(data[1]))
            index = (data[0] - 1) * 3 + data[1] - 1
            if ((1 <= data[0] <= 3 and
                    1 <= data[1] <= 3) and
                       grid_state[index] == " "):
                player["steps"].append((player["label"], data))
                grid_state[index] = player["label"]
                break


def game_intro(player_1: dict, player_2: dict) -> None:
    player_1["name"] = input("введите имя для Player_1: ").strip()
    player_2["name"] = input("введите имя для Player_2: ").strip()

    player_1["label"] = "X" if rd.random() > 0.5 else "O"
    player_2["label"] = "X" if player_1["label"] == "O" else "O"
    clear_console()
    print(
        f"Внимание, [{player_1['name']}] и [{player_2['name']}]\n" + \
        "Cлучайным выбором\n" + \
        f"[{player_1['name']}] играет знаком: {player_1['label']}\n" + \
        f"[{player_2['name']}] играет знаком: {player_2['label']}\n" + \
        "Игра началась!"
    )


def check_combinations(combs: list,
                       grid_state: list,
                       player: dict)-> bool:
    for comb in combs:
        (c1, c2, c3) = comb
        if (grid_state[c1] == grid_state[c2] == grid_state[c3] and
        " " not in [grid_state[c1], grid_state[c2], grid_state[c3]]):
            return f"Победа игрока - {player['name']}!!"
        elif " " not in grid_state:
            return "Ничья"


def xs_os(player_1: dict,
          player_2: dict,
          grid_state: list,
          combinations: list) -> int:
    change_player = None
    result_message = None
    step_counter = 1

    game_intro(player_1, player_2)
    time.sleep(3)
    clear_console()

    while True:
        clear_console()
        print(f"STEP: {step_counter}\t" + \
              f"([{player_1['name']}] - {player_1['label']} | " + \
              f"[{player_2['name']}] - {player_2['label']})")
        make_grid(grid_state)
        print(f"[{player_1['name']}]: {player_1['steps']}")
        print(f"[{player_2['name']}]: {player_2['steps']}")
        print("-"*60)

        if result_message:
            print(result_message)
            return 1

        if (step_counter == 1 and
                player_1["label"] == "O"):
            change_player = True
        elif (step_counter == 1 and
                player_2["label"] == "O"):
            change_player = False

        if not change_player: 
            save_data(player_1, grid_state)
            result_message = check_combinations(
                combinations,
                grid_state,
                player_1
            )
        else:
            save_data(player_2, grid_state)
            result_message = check_combinations(
                combinations,
                grid_state,
                player_2
            )

        step_counter += 1
        change_player = not change_player

if __name__ == "__main__":
    while True:
        player_1 = {
            "label": "",
            "name": "",
            "steps": []
        }
        player_2 = {
            "label": "",
            "name": "",
            "steps": []
        }
        grid_state = [" " for i in range(9)]

        xs_os(player_1,
              player_2,
              grid_state,
              combinations)
        while True:
            answer = input("Хотите ли вы сыграть ещё раз? (1 - да, 0 - нет): ")
            if answer in ["0", "1"]:
                break
        if not int(answer):
            break
