import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import Graph
import Reader
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App(ttk.Frame):

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Netflix Data Analysis")
        self.root.geometry("1200x600")
        # create a reader class and a graph class
        self.__reader = Reader.Reader('netflix_titles.csv')
        self.__graph = Graph.Graph(self.__reader.get_df())
        # create the GUI
        super().__init__(self.root)
        # configure the grid
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        # create the variables
        self.__n = tk.StringVar()
        self.__data1 = None
        self.__data2 = None
        self.__n.set("Choose a graph type")

        # creating combobox
        self.__cbx_type = ttk.Combobox(self, textvariable=self.__n)
        self.__cbx_type["values"] = ["distribution graphs", "everyday graph",
                                     "scatter plot"]
        # creating buttons exit, quit
        self.__btn_plot = ttk.Button(self, text="Plot",
                                     command=self.update_plots)
        self.__btn_quit = ttk.Button(self, text="Quit",
                                     command=self.root.destroy)
        self.__describe = ttk.LabelFrame(self, text="Describe")
        self.__text1 = ttk.Label(self.__describe,
                                 text="This is a program to analyze Netflix data")
        self.__text2 = ttk.Label(self.__describe,
                                 text="Description of the graphs:")

        # construct graph on tkinter
        fig = Figure()
        self.ax = fig.add_subplot()
        self.plot = FigureCanvasTkAgg(fig, master=self)
        self.create_widgets()

    def create_widgets(self):
        self.__text1.pack()
        self.__text2.pack()

        self.__describe.grid(row=0, column=3, rowspan=2, sticky="NEWS", padx=5,
                             pady=5)
        self.__cbx_type.grid(row=1, column=0, padx=5, pady=5)
        self.__btn_plot.grid(row=1, column=1, padx=5, pady=5)
        self.__btn_quit.grid(row=1, column=2, padx=5, pady=5)
        self.plot.get_tk_widget().grid(row=0, sticky='news', padx=5, pady=5,
                                       columnspan=3)

    def update_plots(self):
        self.ax.clear()
        if isinstance(self.__data1, ttk.Label):
            self.__data1.destroy()
        if isinstance(self.__data2, ttk.Label):
            self.__data2.destroy()
        if self.__n.get() == "distribution graphs":
            answer = self.__graph.plot_distribution(self.ax, 'type')
            self.plot.draw()
            self.__data1 = ttk.Label(self.__describe,
                                     text=f"This graph shows the distribution of the types of movies and TV shows\n"
                                          f"The most common type of content is movie {answer['Movie']} times\n"
                                          f"The least common type of content is TV shows {answer['TV Show']} times\n")
            self.__data1.pack()

        elif self.__n.get() == "everyday graph":
            data = self.__graph.plot_everyday(self.ax, 'type', 'release_year')
            string = self.yr_ty_ct(data.head(10).values)
            self.plot.draw()
            self.__data1 = ttk.Label(self.__describe,
                                     text=f"This graph shows the number of movies and TV shows released each year\n"
                                          f"Here 10 highest number of movies and TV shows are shown \n")
            self.__data2 = ttk.Label(self.__describe, text=string)
            self.__data1.pack()
            self.__data2.pack()
        elif self.__n.get() == "scatter plot":
            value = self.__graph.plot_scatter(self.ax, 'release_year', 'type')
            self.plot.draw()
            self.__data1 = ttk.Label(self.__describe,
                                     text=f"This graph shows the number of movies and TV shows released each year\n")
            self.__data2 = ttk.Label(self.__describe,
                                     text=f"The correlation between the number of movies and TV shows released each year is {value:.3f}")
            self.__data1.pack()
            self.__data2.pack()

    # create a function to return the string of the year, type and count
    @staticmethod
    def yr_ty_ct(data: pd.DataFrame):
        s = ''
        for i in data:
            s += f"year {i[1]} {i[0]} type got {i[2]}\n"
        return s
