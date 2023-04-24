import tkinter as tk

# --- functions ---

def clicked_callback(event):
    #canvas.move(label_id, 5, 0)
    canvas.coords(label_id, event.x, event.y)

# --- main ---

root = tk.Tk()
root.geometry("800x600")

canvas = tk.Canvas(root, width=1000, height=600, bg='blue')
canvas.bind("<Button-1>", clicked_callback)
canvas.place(relwidth=0.9, relheight=0.8, relx=0.05, rely=0.05)

l2 = tk.Label(canvas, text="Test", bg='red')
#l2.bind("<Button-1>", clicked_callback)
label_id = canvas.create_window((100, 100), window=l2)

root.mainloop()