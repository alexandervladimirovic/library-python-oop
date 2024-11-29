import time

from library.library import Library

def main():
    """
    Консольный интерфейс для управления библиотекой.
    """

    library = Library(input("Введите путь к файлу библиотеки: "))

    while True:

        print("Доступные команды: \n")

        print("1. - Добавить книгу")
        print("2. - Удалить книгу")
        print("3. - Искать книги")
        print("4. - Показать все книги")
        print("5. - Обновить статус книги")
        print("6. - Сохранить библиотеку в JSON")
        print("7. - Загрузить библиотеку из JSON")
        print("8. - Выход")

        command = input("\nВыберите команду: ")

        if command == "1":
            try:
                title = input("Введите название книги: ").strip()
                author = input("Введите автора книги: ").strip()
                year = int(input("Введите год издания книги: "))
                library.add_book(title, author, year)
                print("\nКнига успешно добавлена!")
            except Exception as e:
                print(f"Ошибка при добавлении книги: {e}")

        elif command == "2":

            book_id = input("Введите ID книги для удаления: ")

            try:
                library.remove_book(book_id)
                print("\nКнига успешно удалена!")
            except Exception as e:
                print(f"Ошибка при удалении книги: {e}")

        elif command == "3":

            print("\nПараметры поиска: title, author, year")

            params = {}

            title = input("Введите название книги (или нажмите Enter для пропуска): ").strip()
            author = input("Введите автора книги (или нажмите Enter для пропуска): ").strip()
            year = (input("Введите год издания книги (или нажмите Enter для пропуска): ")).strip()

            if title:
                params["title"] = title
            if author:
                params["author"] = author
            if year:
                try:
                    params["year"] = int(year)
                except ValueError:
                    print("Год должен быть числом!")
                    continue
            try:
                results = library.search_books(**params)
                if results:
                    for book in results:
                        print(book)
                else:
                    print("Книги не найдены.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif command == "4":
            library.all_books()

        elif command == "5":
            book_id = input("Введите ID книги для обновления статуса: ")
            new_status = input("Введите новый статус книги ('в наличии', 'выдана'): ").strip()
            try:
                library.update_status(book_id, new_status)
                print("\nСтатус книги успешно обновлен!")
            except Exception as e:
                print(f"Ошибка при обновлении статуса книги: {e}")

        elif command == "6":
            try:
                library.write_data_to_json()
                print("\nБиблиотека успешно сохранена!")
            except Exception as e:
                print(f"Ошибка при сохранении библиотеки в файл: {e}")

        elif command == "7":



            try:
                library.read_data_from_json()
                print("\nБиблиотека успешно загружена!")
            except Exception as e:
                print(f"Ошибка при загрузке библиотеки из файла: {e}")

        elif command == "8":
            print("Программа завершена.")
            break

        else:
            print("Некорректная команда.")
        
        time.sleep(5)




if __name__ == "__main__":
    main()
            