#
#  Import LIBRARIES
import sqlite3  # noqa: F401
from sqlite3 import Connection, Cursor

# import flet as ft

#  Import FILES
#
#  _______________________

database: str = "../storage/data/dados.db"


def iniciar_banco() -> None:
    con: Connection = sqlite3.connect(database=database)
    cur: Cursor = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contatos( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT,
        telefone TEXT
        )  
    """)
    con.commit()
    con.close()


def ler_do_banco() -> list[int | str | str]:
    con: Connection = sqlite3.connect(database=database)
    cur: Cursor = con.cursor()
    cur.execute("SELECT * FROM coritatos")
    risultado: list[int | str | str] = cur.fetchall()
    con.close()
    return risultado


def salvar_no_banco(nome, telefone) -> None:
    con: Connection = sqlite3.connect(database=database)
    cur: Cursor = con.cursor()
    cur.execute("INSERT INTO contatos (nome, telefone) VALUES (?,?)", (nome, telefone))
    con.commit()
    con.close()


def deletar_do_banco(id_contato) -> None:
    con: Connection = sqlite3.connect(database=database)
    cur: Cursor = con.cursor()
    cur.execute("DELETE FROM contatos WHERE id =?", (id_contato))
    con.commit()
    con.close()


# print("Done!!!")
# iniciar_banco()


# def main(page: ft.Page):


# if __name__ == "__main__":
#     ft.app(main)
