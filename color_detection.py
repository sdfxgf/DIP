from PIL import Image
import cv2
import pandas as pd
from tkinter import *
from tkinter import ttk
def display_text():
    global path  # Declare 'path' as a global variable
    path = entry.get()  # Store the input text in the 'path' variable
    label.config(text=path, fg="white", font=("Arial", 16, "bold"))

def clear_text():
    entry.delete(0, END)
    label.config(text="", fg="white")

win = Tk()
win.geometry("750x250")
win.title("APP PROJECT_PYTHON")
win.configure(bg="black")  # Set a dark background color

# Create a Label for the software title
title_label = Label(win, text="COLOR DETECTION SOFTWARE", font=("Arial", 18, "bold"), bg="black", fg="white")
title_label.pack(side=TOP, pady=10)

# Create a Label with dark-themed styling for the file name
file_label = Label(win, text="ENTER YOUR FILE NAME", font=("Arial", 14, "bold"), bg="black", fg="orange")
file_label.pack()

# Initialize a Label with dark-themed styling
label = Label(win, text="", font=("Arial", 16, "bold"), fg="orange", bg="black")
label.pack()

# Create an Entry widget with dark-themed styling
entry = Entry(win, width=40, font=("Arial", 12), bg="gray", fg="white", insertbackground="orange")
entry.focus_set()
entry.pack()

# Create a custom style for the button
button_style = ttk.Style()
button_style.configure("Custom.TButton", background="black", foreground="black", font=("Arial", 12, "bold"))

# Create a Display Text Button with the custom style
display_button = ttk.Button(win, text="Get file", width=20, command=display_text, style="Custom.TButton")
display_button.pack(pady=20)

# Create a Clear Text Button with the custom style
clear_button = ttk.Button(win, text="Clear Text", width=20, command=clear_text, style="Custom.TButton")
clear_button.pack()

win.mainloop()

img = cv2.imread(path)

# declaring global  (are used later on)
clicked = False
r = g = b = x_pos = y_pos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:

    cv2.imshow("image", img)
    if clicked:

        # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()

