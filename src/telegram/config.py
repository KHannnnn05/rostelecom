import os
from dotenv import load_dotenv
from os.path import join, dirname
from db.employee import DataBase
import sqlite3

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

token = os.environ.get('API_TOKEN')
sv_id = int(os.environ.get('SV_ID'))

with sqlite3.connect('db.sqlite') as con:
    cur = con.cursor()

db = DataBase(con, cur)