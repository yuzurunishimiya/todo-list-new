"""basic version of to-do list"""

from typing import List, Dict
from typing import Optional, Literal, Union

import json
import pprint


def read_db(table: str):
    """read db file"""

    with open("db.json", "r") as f:
        data: dict = json.loads(f.read())
        return data.get(table)


def write_db(object_type: Literal["user", "todo", "serial_user", "serial_todo"], data: Union[List[Dict], int]):
    """overwrite to db"""

    obj = {
        "user": "users",
        "todo": "todos",
        "serial_user": "serial_user",
        "serial_todo": "serial_todo",
    }

    if object_type in obj:
        db_data = None
        with open("db.json", "r") as f:
            db_data = json.loads(f.read())
        with open("db.json", "w") as f:
            db_data[obj[object_type]] = data
            f.write(json.dumps(db_data, indent=4))
    else:
        print(f"expected error occured, write db object type: {object_type}")
        exit()


def ex_todos(todos: List[Dict]) -> List[Dict]:
    """to restructure todos"""

    structured_todos: List[Dict] = []
    for todo in todos:
        structured_todos.append({
            "id": todo["id"],
            "todo": todo["content"],
            "time": todo["timestamp"],
        })

    return structured_todos


def login(username: str, password: str) -> Optional[Dict]:
    """login"""

    data: List[Dict] = read_db("users")
    user = None
    for u in data:
        if u["username"] == username:
            user = u
            break
    else:
        return

    if user["password"] == password:
        return u


def menu_login():
    """login menu"""

    user = None
    print("Login !")

    while user is None:
        username = input("username: ")
        password = input("password: ")
        user = login(username, password)
        if user is None:
            print("Username atau password salah! Ulangi")

    return user


def filter_todo(todos: List[Dict], user_id: int):
    """get todos by user"""
    user_todo_lists = []
    for todo in todos:
        if todo["user_id"] == user_id:
            user_todo_lists.append(todo)

    return user_todo_lists

def menu_todo(user_id: int):
    """get user's todo list"""

    while True:
        print(
            """
        ===== ***** =====
        menu:
        1. Lihat todo list anda
        2. Tambah todo list anda
        3. Edit todo list
        4. Hapus todo list
        99. Keluar
            """
        )
        choice = input("pilihan: ")

        if choice == "1":
            todos = read_db("todos")
            user_todo_lists = filter_todo(todos, user_id)
            user_todo_lists = ex_todos(user_todo_lists)

            print("todo-list kamu: ")
            pprint.pprint(user_todo_lists, indent=2)

        elif choice == "2":
            todos: List[Dict] = read_db("todos")
            todo_max_id: int = read_db("serial_todo") + 1

            new_content = input("input konten: ")
            new_time = input("input tanggal [format: yyyy-mm-dd hh:mm]: ")
            new_todo = {"id": todo_max_id, "user_id": user_id, "content": new_content, "timestamp": new_time}

            todos.append(new_todo)
            write_db("todo", todos)
            write_db("serial_todo", todo_max_id)
            print("Selamat! todo sudah ditambahkan!", end="\n\n")

        elif choice == "3":
            id_target = int(input("silahkan masukkan id todolist yang akan diedit: "))
            target = None

            todos = read_db("todos")
            for todo in todos:
                if todo["id"] == id_target:
                    target = todo

            if target is None or target["user_id"] != user_id:
                print("id target tidak ditemukan")
            else:
                print(
                    """
                    Silahkan kosongkan(jangan diisi) apabila anda tidak ingin mengubahnya
                    Apabila kosong, maka akan diisi dengan konten atau waktu sebelumnya.
                    """
                )
                new_content = input("konten baru: ")
                new_time = input("input tanggal baru [format: yyyy-mm-dd hh:mm]: ")

                if new_content or new_time:
                    if new_content:
                        todo["content"] = new_content
                    if new_time:
                        todo["timestamp"] = new_time

                    write_db("todo", todos)
                    print("data todo sudah diupdate")

        elif choice == "4":
            id_target = int(input("silahkan masukan id todolist yang akan kamu hapus: "))
            target = None
            index_target = None

            todos = read_db("todos")
            for index, todo in enumerate(todos):
                if todo["id"] == id_target:
                    target = todo
                    index_target = index
                    break

            if target is None:
                print("id target tidak ditemukkan")
            else:
                todos.pop(index_target)
                write_db("todo", todos)
                print("data todo sudah dihapus")

        elif choice == "99":
            print("exiting....!")
            exit()


def menu_daftar():
    """daftar"""

    users: List[Dict] = read_db("users")
    new_id: int = read_db("serial_user") + 1

    while True:
        username = input("username baru: ")
        password = input("password baru: ")

        for user in users:
            if user["username"] == username:
                print("username sudah digunakan, silahkan gunakan username lain!")
                break
        else:
            new_user = {"id": new_id, "username": username, "password": password}
            users.append(new_user)
            write_db("user", data=users)
            write_db("serial_user", data=new_id)
            print("User telah terdaftar, silahkan login")
            break


def main():
    """main"""

    user = None
    while user is None:
        print(
            """
        Selamat datang!
        Silahkan pilih menu:
        1. Login
        2. Daftar
        99. Keluar
            """
        )

        choice = input("pilihan kamu: ")
        if choice == "1":
            user = menu_login()
        elif choice == "2":
            menu_daftar()
        elif choice == "99":
            print("exiting...")
            exit()

    menu_todo(user_id=user["id"])


if __name__ == "__main__":
    main()
