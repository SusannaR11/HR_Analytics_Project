from pathlib import Path
import duckdb

# class for reading data from local warehouse.
class AdsDB:
    def __init__(self, db_file="ads_data_warehouse.duckdb"):
        self.db_path = Path(__file__).parent.parent / db_file
        self.conn = duckdb.connect(str(self.db_path), read_only=True)
        

    # function for executing query return dataframe
    def query(self, sql):
        return self.conn.execute(sql).fetchdf()

    # function for closing connection to duckdb
    def close(self):
        self.conn.close()