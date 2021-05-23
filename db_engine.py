from sqlalchemy import create_engine
import pandas as pd

# Handles most of the database querying, usually returning a dataset for a query
class dbEngine:
    Server = ''
    Username = ''
    Password = ''
    Database = ''
    Driver = ''

    DatabaseConnection = ''

    engine = None

    con = None

    # Sets up the engine for use
    def __init__(self):

        # Get database information from file:
        with open("server_info") as fp:

            # Reads the first line, and splits it into items
            elements = fp.readline()

            elements = elements.split(",")

            for i in range(len(elements)):

                if i == 0:
                    self.Server = elements[i]
                elif i == 1:
                    self.Database = elements[i]
                elif i == 2:
                    self.Driver = elements[i]
                elif i == 3:
                    self.Username = elements[i]
                elif i == 4:
                    self.Password = elements[i]

            fp.close()


        Database_Con = f'mssql://{self.Username}:{self.Password}@{self.Server}/{self.Database}?driver={self.Driver}'

        engine = create_engine(Database_Con)

        self.con = engine.connect()

        print("Connected to " + self.Database)

    # Runs a basic query
    def selectQuery(self, query):


        # try:

        return pd.read_sql_query(query, self.con)


        # except:

        # print("Error running query: " + query)

    def insertQuery(self, query):

        self.con.execute(query)
        print("Inserted into database")

