import os
import time
from tabulate import tabulate


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_logo() -> None:
    print(
"""
=====================================================================================                                              
     __ __ _____ ____  __    _____     _____ _____ _____ _____ _____ _____ _____        
    │  │  │_   _│    ╲│  │  │  _  │___│     │  _  │   │ │  _  │   __│   __│ __  │      
    │_   _│ │ │ │  │  │  │__│   __│___│ │ │ │     │ │ │ │     │  │  │   __│    ─│      
      │_│   │_│ │____╱│_____│__│      │_│_│_│__│__│_│___│__│__│_____│_____│__│__│       
                                                                      version 0.57          
=====================================================================================
"""
            )

def styled_input(prompt):
    
    match prompt:
        case "username":
            print("Enter Username:> ", "_"*25, end="\r")
            username = input("Enter Username:> ")
            return username
        case "password":
            print("Enter Password:> ", "_"*30, end="\r")
            password = input("Enter Password:> ")
            return password
        # case "option":
        #   def option_input():
        #       option = input("Enter your option:> ")
        #       return option
        case _:
            return "Baklol"

def loading_animation(message: str, duration: float) -> None:
    Loader: list[str] = ['|', '/', '—', '\\']
    start = time.perf_counter()
    i: int = 0
    frame_delay = 0.2
    net_duration: float = duration - frame_delay
    while(time.perf_counter() - start < net_duration):
        print(message, Loader[i % 4], end="\r")
        i = i + 1
        time.sleep(frame_delay)
    print(message, " Done!")

    
def display_formats_table(formats: list):
    print(tabulate(formats, headers="keys", tablefmt='simple'))

def progress_bar(percentage: float, width: int = 30) -> str:
    percentage = max(0, min(100, percentage))
    filled = int(width * percentage / 100)
    bar = '=' * filled + ' ' * (width - filled)
    return f'[{bar}]'

def print_menu(title: str, options: dict):
    
    """
        options = {
            '1': 'Menu Option 1',
            '2': 'Menu Option 2',
            '3': 'Menu Option 3',
            '4': 'Menu Option 4',
            .
            .
            .
            '0': 'Back'
        }

        follow the above mentioned dict structure to use print_menu module
    """

    print(title)
    if options:
        for key, value in options.items():
            if key != '0':
                print(f"{key}. {value}")
        if '0' in options:
            print(f"0. {options['0']}")

if __name__ == "__main__":
    clear_screen()
    