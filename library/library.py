import os
import json
import logging
from typing import Union

from library.book import Book


if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/console.log")]
)
logger = logging.getLogger(__name__)

class Library:
    """
    Класс Library представляет собой систему управления библиотекой.

    Этот класс предоставляет функциональность для работы с библиотекой книг, 
    включая добавление, удаление, поиск, обновление статусов книг, а также 
    чтение и запись данных в формате JSON.

    Методы:

    write_data_to_json(file_path: str) -> None
        Записывает данные библиотеки в указанный JSON-файл.

    read_data_from_json(file_path: str) -> None
        Считывает данные библиотеки из указанного JSON-файла.

    add_book(title: str, author: str, year: int) -> None
        Добавляет новую книгу в библиотеку.

    remove_book(book_id: str) -> None
        Удаляет книгу из библиотеки по указанному id.

    search_books(**kwargs) -> list
        Ищет книги по заданным параметрам (title, author, year).

    search_books_by_id(book_id: str) -> Union[Book, None]
        Ищет книгу в библиотеке по id.

    all_books() -> None
        Отображает список всех книг в библиотеке в табличном формате.

    update_status(book_id: str, new_status: str) -> None
        Изменяет статус книги по id.

    """
    VALID_STATUSES = {"в наличии", "выдана"}

    def __init__(self, file_path: str = "library.json"):
        
        self.books = {}
        self.file_path = file_path
        self.read_data_from_json()

    def write_data_to_json(self):
        """
        Записывает данные библиотеки в файл JSON
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([book.to_dict() for book in self.books.values()], file, indent=4, ensure_ascii=False)
            logger.info("Данные успешно записаны в файл %s", self.file_path)
        except Exception as e:
            logger.error("Ошибка при записи данных в файл: %s", e)
            raise ValueError(f"Ошибка при записи данных в файл: {e}") from e


    def read_data_from_json(self):
        """
        Читает данные из файла JSON
        """
        try:
            if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:

                with open(self.file_path, "r", encoding="utf-8") as file:
                    books_data = json.load(file)

                    for book_data in books_data:
                        book = Book(book_data["title"], book_data["author"], book_data["year"])
                        book.id = book_data["id"]
                        book.status = book_data["status"]
                        self.books[book.id] = book

                logger.info("Данные успешно загружены из файла %s", self.file_path)
            else:
                logger.warning("Файл %s пуст или не существует", self.file_path)
        
        except Exception as e:
            logger.error("Неизвестная ошибка при чтении данных из файла: %s", e)
            raise ValueError(f"Ошибка при чтении данных из файла: {e}") from e

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет книгу в библиотеку.

        Создает новый объект книги с указанными атрибутами и добавляет его в список
        книг библиотеки. Если входные данные некорректны, будет выброшено исключение TypeError, которое будет
        зафиксировано в логах
        """
        try:
            new_book = Book(title, author, year)
            self.books[new_book.id] = new_book
            logger.info("Добавлена книга: %s (%s, %d)", new_book.title, new_book.author, new_book.year)
            logger.info("Всего книг в библиотеке: %d", len(self.books))

        except TypeError as e:
            logger.error("Ошибка при добавлении книги: %s", e)
            raise


    def remove_book(self, book_id: str) -> None:
        """
        Удаляет книгу из библиотеки по id.

        Если книга с таким id не существует, генерируется исключение ValueError.
        """
        book_remove = self.books.get(book_id)

        if book_remove:
            del self.books[book_id]
            logger.info("Книга с id %s удалена", book_id)
        else:
            logger.error("Книга с id %s не найдена", book_id)
            raise ValueError(f"Книга с id {book_id} не найдена")


    def search_books(self, **kwargs) -> list:
        """
        Ищет книги по title, author, year.

        Можно указать один или несколько параметров для поиска.
        """
        if not self.books:
            logger.warning("Библиотека пуста")
            return []

        if not kwargs:
            logger.warning("Параметры поиска не указаны")
            return []

        sup_keys = {"title", "author", "year"}
        search = {key: value for key, value in kwargs.items() if key in sup_keys}

        for key, value in search.items():

            if key == "year" and not isinstance(value, int):
                logger.error("Некорректный тип значения для year: %s", value)
                raise TypeError("Year должен быть целым числом")

            if key in {"title", "author"} and not isinstance(value, str):
                logger.error("Некорректный тип значения для %s: %s", key, value)
                raise TypeError(f"{key} должен быть строкой")

        if not search:
            logger.error("Некорректные параметры поиска: %s", kwargs)
            raise ValueError(f"Допустимые параметры поиска: {', '.join(sup_keys)}")


        result = [
            book for book in self.books.values() if
            all(getattr(book, key) == value for key, value in search.items())
        ]

        if result:
            logger.info("Найдены книги: %s", [book.to_dict() for book in result])
        else:
            logger.warning("Книги по заданным критериям не найдены: %s", search)
            return []

        return result


    def search_books_by_id(self, book_id: str) -> Union[Book, None]:
        """
        Ищет книгу по id.
        """
        return self.books.get(book_id, None)


    def all_books(self) -> None:
        """
        Печатает список всех книг.

        Если библиотека пуста, выводит сообщение об отсутствии книг.
        """
        if not self.books:
            logger.warning("Библиотека пуста")
            print("Библиотека пуста")
            return

        print(f"{'ID':<36} | {'Название':<35} | {'Автор':<25} | {'Год':<6} | {'Статус':<10}")
        print("-" * 125)

        for book in self.books.values():

            print(f"{book.id:<36} | {book.title:<35} | {book.author:<25} | {book.year:<6} | {book.status:<10}")

        logger.info("Отображено книг: %d", len(self.books))


    def update_status(self, book_id: str, new_status: str) -> None:
        """
        Изменяет статус книги по id.

        Пользователь указывает id книги и новый статус.
        Если книга с указанным id не найдена или статус некорректный, генерируется исключение.
        """

        if new_status.lower() not in self.VALID_STATUSES:

            logger.error("Некорректный статус: %s", new_status.capitalize())
            raise ValueError(f"Недопустимый статус. Возможные значения: {', '.join(self.VALID_STATUSES)}")

        book = self.search_books_by_id(book_id)

        if not book:

            logger.error("Книга с id %s не найдена", book_id)
            raise ValueError(f"Книга с id {book_id} не найдена")

        book.status = new_status.capitalize()

        logger.info("Статус книги с id %s изменён на '%s'", book_id, new_status)
