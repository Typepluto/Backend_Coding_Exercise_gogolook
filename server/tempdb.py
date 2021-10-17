import pandas as pd


class TempDB:
    def __init__(self):
        self.db = pd.DataFrame(columns=['id', 'name', 'status'])
        self.db.set_index('id', inplace=True)
        self.primary_key = 0

    def create(self, data):
        data.update({'status': 0})
        self.db.loc[self.primary_key] = data
        data.update({'id': self.primary_key})
        self.primary_key += 1
        return data

    def delete(self, primary_key):
        self.db.drop(primary_key, inplace=True)
        return True

    def update(self, data, primary_key):
        self.db.loc[primary_key] = data
        data.update({'id': primary_key})
        return data

    def read_all(self):
        return self.db.reset_index().to_dict('records')
