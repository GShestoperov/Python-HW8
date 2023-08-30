import sqlite3 as sl
import os.path


def create_db():
    cur.execute(
        """CREATE TABLE IF NOT EXISTS phones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT,
        first_name TEXT,
        middle_name TEXT,
        phone TEXT,
        email TEXT
        )"""
    )

    con.commit()


def bot_loop():
    while True:
        command = int(
            input(
                "----------------\n"
                + "Введите команду: \n"
                + "1 - Вывести всю информацию\n"
                + "2 - Добавить запись\n"
                + "3 - Поиск записи\n"
                + "4 - Импорт данных из другой БД\n"
                + "5 - Редактирование записи\n"
                + "6 - Удаление записи\n"
                + "0 - выйти из БД\n"
                + "> "
            )
        )
        if command == 0:
            print("Завершение работы")
            con.commit()
            break
        elif command == 1:  # вывод на экран всех записей
            show_all_records()
        elif command == 2:  # добавление записи
            add_record()
        elif command == 3:  # поиск записи
            find_record()
        elif command == 4:  # импорт БД
            import_record()
        elif command == 5:  # редактирование записи
            edit_record()
        elif command == 6:  # удаление записи
            delete_record()


def show_all_records():
    print(
        "Фамилия         | Имя             | Отчество        | Телефон         | E-mail\n"
        + "------------------------------------------------------------------------------------------"
    )
    cur.execute("SELECT last_name, first_name, middle_name, phone, email FROM phones")
    for row in cur.fetchall():
        print(f"{row[0]:15} | {row[1]:15} | {row[2]:15} | {row[3]:15} | {row[4]:20}")


def add_record():
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    middle_name = input("Введите отчество: ")
    phone = input("Введите телефон: ")
    email = input("Введите email: ")
    cur.execute(
        f"""INSERT INTO phones(last_name, first_name, middle_name, phone, email)
        VALUES('{last_name}', '{first_name}', '{middle_name}','{phone}','{email}')"""
    )
    con.commit()


def find_record():
    findtype = int(input("1 - поиск по имени, 2 - поиск по фамилии, другое - отмена: "))
    sql_text = "SELECT last_name, first_name, middle_name, phone, email FROM phones "
    if findtype == 1:
        first_name = input("Введите имя: ")
        cur.execute(sql_text + f" WHERE UPPER(first_name) = '{first_name.upper()}'")
    elif findtype == 2:
        last_name = input("Введите фамилию: ")
        cur.execute(sql_text + f" WHERE UPPER(last_name) = '{last_name.upper()}'")
    if findtype == 1 or findtype == 2:
        row = cur.fetchone()
        if row == None:
            print("Записей не найдено")
        else:
            print(
                "Фамилия         | Имя             | Отчество        | Телефон         | E-mail\n"
                + "-----------------------------------------------------------------------------------------"
            )
            while row != None:
                print(
                    f"{row[0]:15} | {row[1]:15} | {row[2]:15} | {row[3]:15} | {row[4]:20}"
                )
                row = cur.fetchone()


def import_record():
    db_filename = input("Введите имя файла БД: ")
    if os.path.exists(db_filename):
        with sl.connect(db_filename) as con_import:
            cur_import = con_import.cursor()
            cur_import.execute(
                "SELECT last_name, first_name, middle_name, phone, email FROM phones"
            )
            n = 0
            for row in cur_import.fetchall():
                cur.execute(
                    "INSERT INTO phones(last_name, first_name, middle_name, phone, email)"
                    " VALUES(?,?,?,?,?)",
                    row,
                )
                n += 1
            con.commit()
            print(f"Импортировано {n} записей")

        con_import.close()
    else:
        print(f"Файл {db_filename} не найден")


def edit_record():
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    middle_name = input("Введите отчество: ")
    cur.execute(
        "SELECT phone, email FROM phones WHERE UPPER(first_name) = ? AND UPPER(last_name) = ? "
        + " AND UPPER(middle_name) = ?",
        (first_name.upper(), last_name.upper(), middle_name.upper()),
    )
    row = cur.fetchone()
    if row != None:
        phone = input(f"Найден телефон '{row[0]}'. Введите новый телефон: ")
        email = input(f"Найден email '{row[1]}'. Введите новый email: ")
        cur.execute(
            "UPDATE phones SET phone = ?, e5`mail = ? "
            + "WHERE UPPER(first_name) = ? AND UPPER(last_name) = ? AND UPPER(middle_name) = ?",
            (phone, email, first_name.upper(), last_name.upper(), middle_name.upper()),
        )
        print(f"Успешно изменены {cur.rowcount} записей")
        con.commit()
    else:
        print("Записей не найдено")


def delete_record():
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    middle_name = input("Введите отчество: ")
    cur.execute(
        "SELECT * FROM phones WHERE UPPER(first_name) = ? AND UPPER(last_name) = ? "
        + " AND UPPER(middle_name) = ?",
        (first_name.upper(), last_name.upper(), middle_name.upper()),
    )
    row = cur.fetchone()
    if row != None:
        cur.execute(
            "DELETE FROM phones "
            + "WHERE UPPER(first_name) = ? AND UPPER(last_name) = ? AND UPPER(middle_name) = ?",
            (first_name.upper(), last_name.upper(), middle_name.upper()),
        )
        print(f"Успешно удалены {cur.rowcount} записей")
        con.commit()
    else:
        print("Записей не найдено")


con = sl.connect("phones.db")
cur = con.cursor()

create_db()
bot_loop()

con.close()
