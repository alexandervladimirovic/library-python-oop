import logging
import uuid


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/console.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


class Book:
    """
    Представляет книгу с уникальными атрибутами.

    Класс используется для создания объектов книг с уникальным id, статусом,
    а также заданными названием, автором и годом издания. 
    Реализует методы для представления объекта в виде строки __repr__ и сравнения книг 
    по __eq__.

    Атрибуты:
        id (str): Уникальный идентификатор книги, генерируется автоматически.
        status (str): Статус книги, по умолчанию "В наличии".
        title (str): Название книги. Обязательный параметр.
        author (str): Автор книги. Обязательный параметр.
        year (int): Год издания книги. Обязательный параметр.

    Методы:
        __repr__: Возвращает строковое представление объекта.
        __eq__: Сравнивает книги по уникальному идентификатору.

    """
    def __init__(self, title: str, author: str, year: int):
        """
        Инициализатор.

        Создает экземпляр книги с уникальным id, статусом 
        "В наличии" (по умолчанию) и заданными атрибутами: название, автор и год издания. Проверяет входные
        данные на корректность, выбрасывая исключения в случае ошибок.

        """

        if not title or not isinstance(title, str):
            raise TypeError("Название должно быть строкой и не может быть пустым")
        if not author or not isinstance(author, str):
            raise TypeError(
                "Указание автора должно быть в строковом представлении и не может быть пустым"
            )
        if not year or not isinstance(year, int):
            raise TypeError("Год должен быть целым числом и не может быть пустым")

        self.id = str(uuid.uuid4())
        self.status = "В наличии"

        self.title = title
        self.author = author
        self.year = year

    def __repr__(self):
        return f"ID: {self.id}, Название: {self.title}, Автор: {self.author}, Год: {self.year}, Статус: {self.status}"

    def __eq__(self, other):
        """
        Сравнивает текущий объект книги с другим объектом.

        Метод проверяет, является ли переданный объект экземпляром класса Book.
        Если да, то сравниваются id книг.

        """
        if isinstance(other, Book):
            return self.id == other.id

        return False