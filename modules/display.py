import os
import time

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

if __name__ == "__main__":
    print("Hello this is display!")
    time.sleep(1)
    clear_screen()
    loading_animation(message="Load Animation Testing...", duration=20)