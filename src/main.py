#
#  Import LIBRARIES
import sqlite3  # noqa: F401
from sqlite3 import Connection, Cursor

import flet as ft  # type: ignore

#  Import FILES
#
#  _______________________

dados_db: str = "./storage/data/dados.db"


def iniciar_banco() -> None:
    con: Connection = sqlite3.connect(database=dados_db)
    cur: Cursor = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT
        )
    """)
    con.commit()
    con.close()


def ler_do_banco() -> list[int | str]:
    con: Connection = sqlite3.connect(database=dados_db)
    cur: Cursor = con.cursor()
    cur.execute("SELECT * FROM contatos")
    resultado: list[int | str] = cur.fetchall()
    print(resultado)
    con.close()
    return resultado


def salvar_no_banco(nome: str, telefone: str) -> None:
    con: Connection = sqlite3.connect(database=dados_db)
    cur: Cursor = con.cursor()
    cur.execute("INSERT INTO contatos (nome, telefone) VALUES (?, ?)", (nome, telefone))
    con.commit()
    con.close()


def deletar_do_banco(id_contato: int) -> None:
    con: Connection = sqlite3.connect(database=dados_db)
    cur: Cursor = con.cursor()
    cur.execute("DELETE FROM contatos WHERE id = ?", (id_contato,))
    con.commit()
    con.close()


# iniciar_banco()
# salvar_no_banco(nome="Emagnu", telefone="+39-7172388386")
# salvar_no_banco(nome="Elle", telefone="+44-123456789")
# ler_do_banco()

# print("Done!!!")
# iniciar_banco()


def main(page: ft.Page) -> None:
    page.title = "Minha Agenda SQLite"
    page.window.width = 400
    page.window.height = 600

    iniciar_banco()

    nome_input = ft.TextField(label="Nome", hint_text="Digite o nome")
    telefone_input = ft.TextField(label="Telefone", hint_text="Digite o número")
    print(f"nome_input={nome_input}, telefone_input={telefone_input}")
    lista_contatos = ft.Column()

    page.add(nome_input, telefone_input)

    lista_contatos = ft.Column()

    def carregar_dados() -> None:
        lista_contatos.controls.clear()

        dados: list[int | str] = ler_do_banco()

        for contato in dados:
            id_db = contato[0]
            nome_db: str = contato[1]
            tel_db: str = contato[2]
            print(f"id_db={id_db}, nome_db={nome_db}, tel_db={tel_db}")
            print(f"contato[0]={contato[0]}, contato[1]={contato[1]}, contato[2]={contato[2]}")

            linha = ft.Row(
                controls=[
                    ft.Text(value=f"{nome_db} \n{tel_db}", size=16, expand=True),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color="red",
                        # O data=id_db guarda o ID do banco no botão
                        data=id_db,
                        on_click=deletar_contato,
                    ),
                ]
            )
            lista_contatos.controls.append(linha)
        page.update() # type: ignore

    def adicionar_contato(e: ft.ControlEvent) -> None:
        print(f"Inside Addictionar_copntato - nome_input.value={nome_input.value}")
        if nome_input.value:
            salvar_no_banco(nome: str =nome_input.value, telefone: str =telefone_input.value)
            nome_input.value = ""
            telefone_input.value = ""
            carregar_dados()
        else:
            snack_bar = ft.SnackBar(ft.Text("Nome é Obrigatório"))
            page.open(snack_bar)
            page.update()  # type: ignore

    btn_salvar = ft.ElevatedButton(text="Salvar Contato", on_click=adicionar_contato)

    def deletar_contato(e: ft.ControlEvent) -> None:
        id_para_deletar = e.control.data
        deletar_do_banco(id_para_deletar)
        carregar_dados()

    page.add(
        ft.Text(value="Agenda Simples", size=24, weight=ft.FontWeight.BOLD),
        nome_input,
        telefone_input,
        btn_salvar,
        ft.Divider(),
        ft.Text(value="Meus Contatos:", size=20),
        lista_contatos,
    )

    carregar_dados()


ft.app(target=main)


# if __name__ == "__main__":
#     ft.app(main)
