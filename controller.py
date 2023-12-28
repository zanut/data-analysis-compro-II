from app import App


class Control:
    def __init__(self):
        self.app = App()

    def start(self):
        self.app.root.mainloop()
