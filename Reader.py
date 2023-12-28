import pandas as pd


class Reader:
    def __init__(self, filename):
        self.filename = filename
        self.__orig_df: pd.DataFrame = pd.read_csv(self.filename)
        self.__df: pd.DataFrame = self.__orig_df.copy()
        self.__df.fillna('Unknown', inplace=True)

    def get_df(self):
        return self.__df

    def get_orig_df(self):
        return self.__orig_df
