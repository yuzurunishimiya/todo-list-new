"""basic version of to-do list"""

from typing import Any, List, Dict
from typing import Optional

import json
import pprint

from security import hash_text, verify_hashed


DB_Tables = {
    "users",
    "todos",
    "serial_user",
    "serial_todo",
}


class DB:
    """DB's class"""

    def __init__(self, db_file: str) -> None:
        """initialize class fields"""

        self.__db_file = db_file

    def read(self, table: str = None) -> Optional[Any]:
        """read db file"""

        with open(self.__db_file, "r", encoding="utf-8") as f:
            data: dict = json.loads(f.read())
            if table:
                return data.get(table)

            return data

    def write(self, object_type: str, data: Any) -> None:
        """overwrite to db"""

        if object_type in DB_Tables:
            db_data = self.read()

            with open(self.__db_file, "w", encoding="utf-8") as f:
                db_data[object_type] = data
                f.write(json.dumps(db_data, indent=4))


class Auth:
    """main's class"""

    def __init__(self, db: DB) -> None:
        self.__db = db

    def sign_up(self) -> None:
        """daftar"""

        users: List[Dict] = self.__db.read("users")
        new_id: int = self.__db.read("serial_user") + 1

        while True:
            username = input("username baru: ")
            password = input("password baru: ")

            for user in users:
                if user["username"] == username:
                    print("username sudah digunakan, silahkan gunakan username lain!")
                    break
            else:
                new_user = {"id": new_id, "username": username, "password": hash_text(password)}
                users.append(new_user)
                self.__db.write("users", data=users)
                self.__db.write("serial_user", data=new_id)
                print(
                    "Sign-up berhasil, silahkan login untuk melanjutkan; ",
                    "username anda: " + username)
                break

    def login(self, username: str, password: str) -> Optional[Any]:
        """login"""

        users: List[Dict[str, Any]] = self.__db.read("users")
        user: Dict[str, Any] = {}
        for u in users:
            if u["username"] == username:
                user = u
                break

        if user.get("password"):
            hashed = user["password"]
            if not verify_hashed(password, hashed):
                user = None

        return user


class Todo:
    """todo's class"""

    def __init__(self, db: DB) -> None:

        self.__db = db

    @staticmethod
    def _filter_todo(todos: List[Dict], user_id: int):
        """get todos by user"""
        user_todo_lists = []
        for todo in todos:
            if todo["user_id"] == user_id:
                user_todo_lists.append(todo)

        return user_todo_lists


    def todo(self, user_id: int):
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
                todos = self.__db.read("todos")
                user_todo_list = self._filter_todo(todos, user_id)
                user_todo_list = [
                    {
                        "id": todo["id"],
                        "todo": todo["content"],
                        "time": todo["timestamp"],
                    } for todo in user_todo_list
                ]

                print("todo-list kamu: ")
                pprint.pprint(user_todo_list, indent=2)

            elif choice == "2":
                todos: List[Dict] = self.__db.read("todos")
                todo_max_id: int = self.__db.read("serial_todo") + 1

                new_content = input("input konten: ")
                new_time = input("input tanggal [format: yyyy-mm-dd hh:mm]: ")
                new_todo = {
                    "id": todo_max_id,
                    "user_id": user_id,
                    "content": new_content,
                    "timestamp": new_time,
                }

                todos.append(new_todo)
                self.__db.write("todos", todos)
                self.__db.write("serial_todo", todo_max_id)
                print("Selamat! todo sudah ditambahkan!", end="\n\n")

            elif choice == "3":
                id_target = int(input("silahkan masukkan id todolist yang akan diedit: "))
                target = None

                todos = self.__db.read("todos")
                for todo in todos:
                    if todo["id"] == id_target:
                        target = todo
                        break

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
                            target["content"] = new_content
                        if new_time:
                            target["timestamp"] = new_time

                        self.__db.write("todos", todos)
                        print("data todo sudah diupdate")

            elif choice == "4":
                id_target = int(input("silahkan masukan id todolist yang akan kamu hapus: "))
                target = None
                index_target = None

                todos = self.__db.read("todos")
                for index, todo in enumerate(todos):
                    if todo["id"] == id_target:
                        target = todo
                        index_target = index
                        break

                if target is None or target["user_id"] != user_id:
                    print("id target tidak ditemukkan")
                else:
                    todos.pop(index_target)
                    self.__db.write("todos", todos)
                    print("data todo sudah dihapus")

            elif choice == "99":
                print("exiting....!")
                exit()


class Main:
    """k"""

    def __init__(self) -> None:
        db_file = "db.json"
        self.__db = DB(db_file)
        self.__todo = Todo(self.__db)
        self.__auth = Auth(self.__db)

    def run(self):
        """run app"""

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
                while user is None:
                    username = input("username: ")
                    password = input("password: ")
                    user = self.__auth.login(username, password)
                    if user is None:
                        print("username atau password salah, silahkan ulangi")
                        break_key = input("input 0 untuk kembali ke menu utama: ")
                        if break_key == "0":
                            break

            elif choice == "2":
                self.__auth.sign_up()

            elif choice == "99":
                print("exiting...")
                exit()

        self.__todo.todo(user_id=user)


if __name__ == "__main__":
    app = Main()
    app.run()
