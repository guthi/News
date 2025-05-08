import tkinter as tk
from model import NewsModel
from view import NewsView
from controller import NewsController

def main():
    root = tk.Tk()
    model = NewsModel()
    controller = NewsController(model, None)
    view = NewsView(root, controller)
    controller.view = view
    root.mainloop()

if __name__ == "__main__":
    main()
