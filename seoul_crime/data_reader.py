import pandas as pd
import numpy as np
import json
import googlemaps
class DataReader:
    def __init__(self):
        self._context = None
        self._fname = None

    @property
    def context(self)->str:
        return self._context
    @context.setter
    def context(self, context):
        self._context = context

    @property
    def fname(self) -> str:
        return self.fname

    @context.setter
    def fname(self, fname):
        self._fname = fname

    def new_file(self)->str:
        return self._context + self._fname

    def csv_to_dframe(self) -> object:
        file = self.new_file()
        return pd.read_csv(file, encoding='UTF-8', thousands=',')

    def xls_to_dframe(self, header, usecols)-> object:
        file = self.new_file()
        return pd.read_excel(file, encoding='UTF-8', header=header, usecols=usecols)

    def json_load(self):
        file = self.new_file()
        return json.load(open(file, encoding='UTF-8'))

    def create_gmaps(self):
        return googlemaps.Client(key='..')


