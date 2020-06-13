from tkinter import *
import requests
import json

lastClickX = 0
lastClickY = 0
isAlwaysOnTop = False
isRevertColors = False
root = Tk()

def getPriceFromUrl():
    data = json.loads(requests.get("https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT").text)
    return str(round(float(data["price"]), 2))

def Refresher():
    price.configure(text=getPriceFromUrl())
    # Change color based on the value:
    changeBgColor(getPriceFromUrl())
    # every 2 seconds
    root.after(1000, Refresher)

maxVal = float(getPriceFromUrl())

def changeBgColor(value):
    global maxVal
    global isRevertColors
    if maxVal < float(value):
        maxVal = float(value)
        price.config(fg="white", bg="green") if isRevertColors else price.config(bg="black", fg="green")
    elif maxVal > float(value):
        price.config(fg="white", bg="red") if isRevertColors else price.config(bg="black", fg="red")
    else:
        price.config(bg="black", fg="white")

def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

def Dragging(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x , y))

def close(event):
    root.withdraw() # if you want to bring it back
    sys.exit() # if you want to exit the entire thing

def popup(event):
    menu.post(event.x_root, event.y_root)

def closeApp():
    sys.exit()

def alwaysOnTop():
    global isAlwaysOnTop
    if isAlwaysOnTop is False:
        root.attributes('-topmost', True)
        isAlwaysOnTop = True
    else:
        root.attributes('-topmost', False)
        isAlwaysOnTop = False

def revertColors():
    global isRevertColors
    if isRevertColors is False:
        isRevertColors = True
    else:
        isRevertColors = False

# Elements Initialize:
menu = Menu(root, tearoff=0)
price = Label(root, bg="black", fg="white")
price.config(font=("Lucida Grande", 16))
colorMenu = Menu(menu)
menu.add_checkbutton(label="Always On Top", command=alwaysOnTop)
menu.add_checkbutton(label="Revert Colors", command=revertColors)
menu.add_command(label="Exit", command=closeApp)

# Root Settings:
root.overrideredirect(True)
root.bind('<Button-1>', SaveLastClickPos)
root.bind('<B1-Motion>', Dragging)
root.bind('<Escape>', close)
root.bind("<Button-3>", popup)

# Refresh every 2 seconds:
Refresher()

price.pack()
root.mainloop()