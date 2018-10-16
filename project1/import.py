'''
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
'''

import os
path = '/home/miha/programer/CS50-web/project1/books.csv'

file = open(path, 'r')

for line in file:
    # [0] isbn
    # [1] title
    # [2] author
    # [3] release year
    # print(line.split(',')[0])