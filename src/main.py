#
#  Import LIBRARIES
import sqlite3  # noqa: F401
from sqlite3 import Connection, Cursor

# import flet as ft

#  Import FILES
#
#  _______________________


def iniciar_banco() -> None:
    con: Connection = sqlite3.connect(database="../storage/data/dados.db")
    cur: Cursor = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contatos( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT,
        telefone TEXT
        )  
    """)
    con.commit()


print("Done!!!")

iniciar_banco()

# def main(page: ft.Page):


# if __name__ == "__main__":
#     ft.app(main)
