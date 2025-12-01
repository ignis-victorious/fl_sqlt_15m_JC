#
#  Import LIBRARIES
import sqlite3  # noqa: F401
from sqlite3 import Connection, Cursor

import flet as ft  # type: ignore

#  Import FILES
#
#  _______________________


#  name and location of database
contact_data_db: str = "./storage/data/contact_data.db"


#  Database creation and controls
def start_db() -> None:
    con: Connection = sqlite3.connect(database=contact_data_db)
    cur: Cursor = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telephone TEXT
        )
    """)
    con.commit()
    con.close()


def read_from_database() -> list[tuple[int, str, str]]:
    con: Connection = sqlite3.connect(database=contact_data_db)
    cur: Cursor = con.cursor()
    cur.execute("SELECT * FROM contact")
    result: list[tuple[int, str, str]] = cur.fetchall()
    con.close()
    return result


def save_to_database(nome: str, telephone: str) -> None:
    con: Connection = sqlite3.connect(database=contact_data_db)
    cur: Cursor = con.cursor()
    cur.execute("INSERT INTO contact (nome, telephone) VALUES (?, ?)", (nome, telephone))
    con.commit()
    con.close()


def delete_from_database(id_contact: int) -> None:
    con: Connection = sqlite3.connect(database=contact_data_db)
    cur: Cursor = con.cursor()
    cur.execute("DELETE FROM contact WHERE id = ?", (id_contact,))
    con.commit()
    con.close()


#  Create UI
def main(page: ft.Page) -> None:
    page.title = "SQLite Phonebook"
    page.window.width = 400
    page.window.height = 600

    # Initialise DB and table
    start_db()

    # Create page input fields
    name_imput = ft.TextField(label="Name", hint_text="Enter the contact name")
    telephone_input = ft.TextField(label="Mobile", hint_text="Enter the mobile number")

    # Create a column that will contain the list of contacts
    contact_list = ft.Column()

    def delete_contact(e: ft.ControlEvent) -> None:
        id_to_delete: int = e.control.data  # type: ignore
        delete_from_database(id_contact=id_to_delete)  # type: ignore
        load_data()  # Refresh list

    def load_data() -> None:
        contact_list.controls.clear()
        contact_data: list[tuple[int, str, str]] = read_from_database()

        for contact in contact_data:
            id_db: int = contact[0]
            nome_db: str = contact[1]
            tel_db: str = contact[2]

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
        if name_imput.value:
            save_to_database(nome=str(object=name_imput.value), telephone=str(object=telephone_input.value))
            name_imput.value = ""
            telephone_input.value = ""
            load_data()
            name_imput.focus()  # Move cursor back to name
            page.update()  # type: ignore
        else:
            snack_bar = ft.SnackBar(content=ft.Text(value="Name is a compulsory field"))
            page.open(control=snack_bar)  # type: ignore
            # page.snack_bar = ft.SnackBar(ft.Text("Name is a compulsory field"))
            # page.snack_bar.open = True
            page.update()  # type: ignore

    save_btn = ft.ElevatedButton(text="Save contact", on_click=add_contact)

    #  Layout - put it all together
    page.add(
        ft.Text(value="Simple Telephone Rubrica", size=24, weight=ft.FontWeight.BOLD),
        name_imput,
        telephone_input,
        save_btn,
        ft.Divider(),
        ft.Text(value="Contacts menu:", size=20),
        contact_list,
    )

    # Initial data load
    load_data()


ft.app(target=main)  # type: ignore
