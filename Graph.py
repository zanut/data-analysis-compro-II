import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr


class Graph:
    def __init__(self, df: pd.DataFrame):
        self.__df = df

    def plot_distribution(self, ax: plt.Axes, column: str):
        ax.clear()
        count = {}
        for row in self.__df[column].unique():
            count[row] = len(self.__df[self.__df[column] == row])
        sns.barplot(x=list(count.keys()), y=list(count.values()), ax=ax)
        ax.set_title(f"Distribution of {column}")
        ax.set_ylabel("Frequency")
        return count

    def plot_everyday(self, ax: plt.Axes, column: str, time):
        ax.clear()
        year = (self.__df.groupby([column, time]).size()).reset_index(name='count')
        sns.lineplot(data=year, x=time, y='count', hue=column, ax=ax, marker='o')
        ax.set_title(f"Line graph of {column}")
        ax.set_ylabel("Frequency")
        return year.sort_values("count", ascending=False)

    def plot_scatter(self, ax: plt.Axes, column1: str, column2: str):
        ax.clear()
        data = pd.crosstab(self.__df[column1], self.__df[column2])
        sns.scatterplot(data=data, x='Movie', y='TV Show', ax=ax)
        ax.set_title(f"Scatter plot of Movie and TV Show")
        ax.set_xlabel('Movie')
        ax.set_ylabel('TV Show')
        # pearsonr is a function that returns a tuple of (Pearson’s correlation coefficient, 2-tailed p-value)
        # ref https://machinelearningmastery.com/how-to-use-correlation-to-understand-the-relationship-between-variables/
        corr, p = pearsonr(data['Movie'], data['TV Show'])
        return corr
