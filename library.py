import os
import json
import logging
import uuid

from typing import Union


if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/console.log")]
)
logger = logging.getLogger(__name__)



class Book:
    """
    Представляет книгу с уникальными атрибутами.

    Класс используется для создания объектов книг с уникальным id, статусом,
    а также заданными названием, автором и годом издания
    Реализует методы для представления объекта в виде строки __repr__ и сравнения книг
    по __eq__

    Атрибуты:
        id (str): Уникальный идентификатор книги, генерируется автоматически
        status (str): Статус книги, по умолчанию "В наличии"
        title (str): Название книги. Обязательный параметр
        author (str): Автор книги. Обязательный параметр
        year (int): Год издания книги. Обязательный параметр

    Методы:
        __repr__: Возвращает строковое представление объекта
        __eq__: Сравнивает книги по уникальному идентификатору
    """

    def __init__(self, title: str, author: str, year: int):
        """
        Инициализатор.

        Создает экземпляр книги с уникальным id, статусом
        "В наличии" (по умолчанию) и заданными атрибутами: название, автор и год издания. Проверяет входные
        данные на корректность, выбрасывая исключения в случае ошибок
        """

        if not title or not isinstance(title, str):
            logger.error("Некорректное название книги: %s", title)
            raise TypeError("Название должно быть строкой и не может быть пустым")
        if not author or not isinstance(author, str):
            logger.error("Некорректное имя автора: %s", author)
            raise TypeError(
                "Указание автора должно быть в строковом представлении и не может быть пустым"
            )
        if not year or not isinstance(year, int):
            logger.error("Некорректный год издания: %s", year)
            raise TypeError("Год должен быть целым числом и не может быть пустым")

        self.id = str(uuid.uuid4())
        self.status = "В наличии"

        self.title = title
        self.author = author
        self.year = year

        logger.info("Создана новая книга: %s (%d)", self.title, self.year)

    def __repr__(self) -> str:
        return f"ID: {self.id}, Название: {self.title}, Автор: {self.author}, Год: {self.year}, Статус: {self.status}"

    def __eq__(self, other) -> bool:
        """
        Сравнивает текущий объект книги с другим объектом

        Метод проверяет, является ли переданный объект экземпляром класса Book
        Если да, то сравниваются id книг
        """
        if isinstance(other, Book):
            return self.id == other.id

        return False

    def to_dict(self) -> dict:
        """
        Преобразует объект книги в словарь
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }


class Library:

    VALID_STATUSES = {"в наличии", "выдана"}

    def __init__(self):
        self.books = {}


    def write_data_to_json(self, file_path):
        """
        Записывает данные библиотеки в файл JSON
        """
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump([book.to_dict() for book in self.books.values()], file, indent=4, ensure_ascii=False)
            logger.info("Данные успешно записаны в файл library.json")
        except Exception as e:
            logger.error("Ошибка при записи данных в файл: %s", e)
            raise ValueError(f"Ошибка при записи данных в файл: {e}") from e


    def read_data_from_json(self, file_path):
        """
        Читает данные библиотеки из файла JSON
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                books_data = json.load(file)

                for book_data in books_data:

                    book = Book(
                                    book_data["title"],
                                    book_data["author"],
                                    book_data["year"]
                                )
                    book.id = book_data["id"]
                    book.status = book_data["status"]
                    self.books[book.id] = book

            logger.info("Данные успешно загружены из файла library.json")

        except FileNotFoundError as e:
            logger.warning("Файл library.json не найден")
            raise FileNotFoundError("Файл library.json не найден") from e

        except Exception as e:
            logger.error("Ошибка при чтении данных из файла: %s", e)
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

        print(f"{'ID':<36} | {'Название':<20} | {'Автор':<20} | {'Год':<6} | {'Статус':<10}")
        print("-" * 92)

        for book in self.books.values():

            print(f"{book.id:<36} | {book.title:<20} | {book.author:<20} | {book.year:<6} | {book.status:<10}")

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
