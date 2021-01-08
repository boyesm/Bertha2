from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Boolean, select
from global_vars import queue_table
import request_handler
#engine = create_engine('sqlite:///bertha2.db')




# # creating a row
#conn = engine.connect()

#create_row = queue_table.insert().values(username='mamae', link='https://www.youtube.com/watch?v=mJdeFEog-YQ', filename='mJdeFEog-YQ', isconverted=False, isqueued=False)
#conn.execute(create_row)
#create_row = queue_table.insert().values(username='mamae', link='https://www.youtube.com/watch?v=mJdeFEog-YQ', filename='mJdeFEog-YQ', isconverted=False, isqueued=False)
#conn.execute(create_row)


# # modifying a row
# req = queue_table.update().where(queue_table.c.id == 2).value(username="new username")
# conn.execute(req)


# #deleting a row


# # reading a row
# s = select([queue_table])
# result = conn.execute(s)

# ## get one row
# row = result.fetchone()
# row['column_title'] # get data from a column

# ## get all rows (not sure)
# # row = result.fetchall()
# # row['']


# conn = engine.connect()
# conn.execute(ins)
