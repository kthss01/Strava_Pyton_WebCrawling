from msvcrt import getch

while True:
    key = ord(getch())
    if key == 27: # ESC
        break
    elif key == 13: # Enter
        print('Enter')
    else:
        print(key)