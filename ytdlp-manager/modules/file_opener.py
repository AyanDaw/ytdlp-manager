import subprocess
import platform
import os

# no need of back

# TODO: See future_enhancement.txt for v1 plans
def open_file(filepath: str) -> bool:
    if not os.path.exists(filepath):
        return False
    
    open_ask = input("Do you want to open the file? [Y/n]:> ").strip().lower()
    if open_ask in ('y', 'yes', ''):
        try:
            if platform.system() == 'Windows':
                subprocess.Popen(['start', '', filepath], shell=True)
            elif platform.system() == 'Darwin':  # Mac
                subprocess.Popen(['open', filepath])
            else:  # Linux
                subprocess.Popen(['xdg-open', filepath])
            return True
        except Exception as e:
            return False
    
    return False
    

if __name__ == "__main__":
    filepath = input("Enter Your filepath:>")
    filepath = filepath.strip().strip('"').strip("'")
    open_file(filepath=filepath)