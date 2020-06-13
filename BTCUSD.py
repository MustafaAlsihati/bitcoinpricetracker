from tkinter import *
import requests
import json

lastClickX = 0
lastClickY = 0

def getPriceFromUrl():
    data = json.loads(requests.get("https://api.binance.com/api/v1/ticker/price?symbol=BTCUSDT").text)
    return str(round(float(data["price"]), 2))

def Refresher():
    price.configure(text=getPriceFromUrl())
    root.after(2000, Refresher) # every second...

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

root = Tk()
root.overrideredirect(True)
root.attributes('-topmost', True)
root.bind('<Button-1>', SaveLastClickPos)
root.bind('<B1-Motion>', Dragging)
root.bind('<Escape>', close)
price = Label(root, bg="black", fg="white")
price.config(font=("Courier", 18))
Refresher()
price.pack()
root.mainloop()