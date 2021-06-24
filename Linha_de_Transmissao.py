import tkinter as tk
from PIL import ImageTk, Image
import threading
import time


#############################################################
# Parameters

Vi = 30
L = 100
e = 1
Rg = 50
Rl = 100
Z0 = 50

# Check if they are ok
assert Z0 > 0 and Rg > 0 and Rl > 0 and Z0 > 0 and L > 0 and e > 0

# Reference values are 233 for 0 and 467 for L
# Calculating a and b for length conversion
a = L/(467-233)
b = -a*233

# Calculate velocity for time update
v = 3e8/e**(1/2)
#############################################################


def voltage_calculations(Vi, Z0, Rl, Rg):

    Vi = Vi*Z0/(Z0 + Rg)
    reflect_l = (Rl - Z0)/(Rl + Z0)
    reflect_g = (Rg - Z0)/(Rg + Z0)

    V = [round(Vi,2)]
    round_about = 0
    while round_about < 6:
        if round_about % 2 == 0 and round_about <= 6:
            Vi = Vi*reflect_l
            V.append(round(Vi,2))
            round_about = round_about + 1
        elif round_about % 2 == 1 and round_about <= 6:
            Vi = Vi * reflect_g
            V.append(round(Vi,2))
            round_about = round_about + 1

    return V


def length_calculator(point, a, b):

    L = a*point + b
    return round(L, 2)


def update_time(pos, L):

    ti = pos/v*1e9
    tr = (L - pos)/v*1e9
    t = ti
    yield round(t,2)

    round_about = 0
    for i in range(5):
        if round_about % 2 == 0:
            t = t + 2*tr
            round_about = round_about + 1
            yield round(t,2)
        else:
            t = t + 2*ti
            round_about = round_about + 1
            yield round(t,2)


# Mouse track function:
def mouse_tracker(event, P, T):

    global click_flag

    if 65 <= event.y <= 110 and 233 <= event.x <= 467:

        position_x = length_calculator(event.x, a, b)
        for i in range(len(P)):
            P[i] = position_x

        for t, i in zip(update_time(position_x, L), range(len(T))):
            T[i] = t

        click_flag = 1


window = tk.Tk()
window.title("Join")
window.geometry("1200x700")
click_flag = 0

path = "transmission_line.png"

img = ImageTk.PhotoImage(Image.open(path))

panel = tk.Label(window, image = img)

panel.pack(side="top")


# Parte do comprimento
P_button = tk.Button(window, text="Position (m)")
P = [1, 2, 3, 4, 5, 6]

# Parte da voltagem
V_button = tk.Button(window, text="Voltage (V)")
V_button.place(x=450, y=350)
table_V = tk.Listbox(window, height=6, font=('Times', 20))
table_V.place(x=450, y=400)

V = voltage_calculations(Vi, Z0, Rl, Rg)

table_V.insert(1, V[0])
table_V.insert(2, V[1])
table_V.insert(3, V[2])
table_V.insert(4, V[3])
table_V.insert(5, V[4])
table_V.insert(6, V[5])

# Parte do tempo
T_button = tk.Button(window, text="Time (ns)")
T = [1, 2, 3, 4, 5, 6]

# Atualização dos valores
update_T_values = lambda event: mouse_tracker(event, P, T)
window.bind('<Button-1>', update_T_values)


def update_values():

    # Position Widget
    P_button.place(x=50, y=350)
    table_P = tk.Listbox(window, height=6, font=('Times', 20))
    table_P.place(x=50, y=400)

    # Time Widget
    T_button.place(x=850, y=350)
    table_T = tk.Listbox(window, height=6, font=('Times', 20))
    table_T.place(x=850, y=400)

    global click_flag
    while True:
        time.sleep(0.01)
        if click_flag:

            # Atualização da posição
            table_P.destroy()
            table_P = tk.Listbox(window, height=6, font=('Times', 20))
            table_P.place(x=50, y=400)

            table_P.insert(0, P[0])
            table_P.insert(1, P[1])
            table_P.insert(2, P[2])
            table_P.insert(3, P[3])
            table_P.insert(4, P[4])
            table_P.insert(5, P[5])

            # Atualização do tempo
            table_T.destroy()
            table_T = tk.Listbox(window, height=6, font=('Times', 20))
            table_T.place(x=850, y=400)

            table_T.insert(0, T[0])
            table_T.insert(1, T[1])
            table_T.insert(2, T[2])
            table_T.insert(3, T[3])
            table_T.insert(4, T[4])
            table_T.insert(5, T[5])

            click_flag = 0


time_thread = threading.Thread(target=update_values)
time_thread.daemon = True
time_thread.start()

list_of_threads = [time_thread]


def on_closing():
    exit()


window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()

# table_T.delete(0)
# table_T.delete(1)
# table_T.delete(2)
# table_T.delete(3)
# table_T.delete(4)
# table_T.delete(5)