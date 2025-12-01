import os
import sqlite3
from sqlite3 import Connection, Cursor

import flet as ft  # type: ignore

# _______________________
# CONFIGURATION
# _______________________

# Ensure the directory exists before connecting
conctat_data_db: str = "./storage/data/conctat_data.db"
os.makedirs(os.path.dirname(conctat_data_db), exist_ok=True)

# _______________________
# DATABASE FUNCTIONS
# _______________________


def start_db() -> None:
    con: Connection = sqlite3.connect(database=conctat_data_db)
    cur: Cursor = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT
        )
    """)
    con.commit()
    con.close()


def read_from__database() -> list[tuple[int, str, str]]:
    con: Connection = sqlite3.connect(database=conctat_data_db)
    cur: Cursor = con.cursor()
    cur.execute("SELECT * FROM contact")
    result: list[tuple[int, str, str]] = cur.fetchall()
    con.close()
    return result


def save_to_database(nome: str, telefone: str) -> None:
    con: Connection = sqlite3.connect(database=conctat_data_db)
    cur: Cursor = con.cursor()
    cur.execute("INSERT INTO contact (nome, telefone) VALUES (?, ?)", (nome, telefone))
    con.commit()
    con.close()


def delete_from_database(id_conctat: int) -> None:
    con: Connection = sqlite3.connect(database=conctat_data_db)
    cur: Cursor = con.cursor()
    cur.execute("DELETE FROM contact WHERE id = ?", (id_conctat,))
    con.commit()
    con.close()


# _______________________
# MAIN APP
# _______________________


def main(page: ft.Page) -> None:
    page.title = "SQLite Phonebook"
    page.window.width = 400  # Updated from page.window.width
    page.window.height = 600  # Updated from page.window.height
    # page.scroll = "AUTO"  # Allows scrolling if list gets long

    # Initialize DB table
    start_db()

    # Create Controls
    nome_input = ft.TextField(label="Name", hint_text="Enter the contact name")
    telephone_input = ft.TextField(label="Mobile", hint_text="Enter the mobile number")

    # We define the list container here
    contact_list = ft.Column()

    # --- LOGIC FUNCTIONS ---
    # def delete_contact(e: ft.ControlEvent) -> None:
    #     # FIX: Check type to prevent "Unknown type" error
    #     button = e.control
    #     assert isinstance(button, ft.IconButton)

    #     id_to_delete = button.data
    #     delete_from_database(id_to_delete)
    #     load_data()  # Refresh list

    def delete_contact(e: ft.ControlEvent) -> None:
        id_to_delete = e.control.data  # type: ignore
        delete_from_database(id_to_delete)  # type: ignore
        load_data()  # Refresh list

    def load_data() -> None:
        contact_list.controls.clear()
        conctat_data: list[tuple[int, str, str]] = read_from__database()

        for conctat in conctat_data:
            id_db: int = conctat[0]
            nome_db: str = conctat[1]
            tel_db: str = conctat[2]

            linha = ft.Row(
                controls=[
                    ft.Text(value=f"{nome_db}\n{tel_db}", size=16, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="red",
                        data=id_db,  # Store ID in the button
                        on_click=delete_contact,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            contact_list.controls.append(linha)
        page.update()  # type: ignore

    def add_contact(e: ft.ControlEvent) -> None:
        if nome_input.value:
            save_to_database(nome=str(nome_input.value), telefone=str(telephone_input.value))
            nome_input.value = ""
            telephone_input.value = ""
            load_data()
            nome_input.focus()  # Move cursor back to name
            page.update()  # type: ignore
        else:
            snack_bar = ft.SnackBar(content=ft.Text(value="Name is a compulsory field"))
            page.open(control=snack_bar)  # type: ignore
            # page.snack_bar = ft.SnackBar(ft.Text("Name is a compulsory field"))
            # page.snack_bar.open = True
            page.update()  # type: ignore

    save_btn = ft.ElevatedButton(text="Save contact", on_click=add_contact)

    # --- LAYOUT SETUP ---

    # FIX: We add everything to the page only ONCE here.
    page.add(
        ft.Text(value="Simple Telephone Rubrica", size=24, weight=ft.FontWeight.BOLD),
        nome_input,
        telephone_input,
        save_btn,
        ft.Divider(),
        ft.Text(value="Contacts menu:", size=20),
        contact_list,
    )

    # Initial data load
    load_data()


ft.app(target=main)  # type: ignore
