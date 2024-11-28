import os
import json
import uuid
import unittest
from unittest.mock import patch

from library import Library, Book


class TestAddBook(unittest.TestCase):
    
    def setUp(self):

        self.library = Library()

    def test_add_book_success(self):

        self.library.add_book("1984", "Джордж Оруэлл", 1949)

        self.assertEqual(len(self.library.books), 1)

        book = next(iter(self.library.books.values()))
        
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "Джордж Оруэлл")
        self.assertEqual(book.year, 1949)
        self.assertEqual(book.status, "В наличии")

    def test_add_book_invalid_title(self):
        
        with self.assertRaises(TypeError) as context:
            self.library.add_book("", "Джордж Оруэлл", 1949)

        self.assertIn("Название должно быть строкой и не может быть пустым", str(context.exception))
    
    def test_add_book_invalid_author(self):
        
        with self.assertRaises(TypeError) as context:
            self.library.add_book("1984", "", 1949)

        self.assertIn("Указание автора должно быть в строковом представлении и не может быть пустым", str(context.exception))
    
    def test_add_book_invalid_year(self):
        
        with self.assertRaises(TypeError) as context:
            self.library.add_book("1984", "Джордж Оруэлл", "1949")

        self.assertIn("Год должен быть целым числом и не может быть пустым", str(context.exception))

class TestRemoveBook(unittest.TestCase):
    
    def setUp(self):

        self.library = Library()
        self.book = Book("1984", "Джордж Оруэлл", 1949)
        self.library.books[self.book.id] = self.book

    def test_remove_success(self):

        init_len = len(self.library.books)
        self.library.remove_book(self.book.id)

        self.assertEqual(len(self.library.books), init_len - 1)
        self.assertNotIn(self.book.id, self.library.books)

    def test_remove_not_found(self):
        invalid_id = "invalid id"
        with self.assertRaises(ValueError) as context:
            self.library.remove_book(invalid_id)
        
        self.assertIn(f"Книга с id {invalid_id} не найдена", str(context.exception))

class TestSearchBook(unittest.TestCase):

    def setUp(self):
        
        self.library = Library()

        self.book1 = Book("1984", "Джордж Оруэлл", 1949)
        self.book2 = Book("451 градус по Фаренгейту", "Рэй Брэдбери", 1953)
        self.book3 = Book("Великий Гэтсби", "Ф. Скотт Фицджеральд", 1925)

        self.library.books[self.book1.id] = self.book1
        self.library.books[self.book2.id] = self.book2
        self.library.books[self.book3.id] = self.book3

    def test_search_by_title(self):
        
        result = self.library.search_books(title="1984")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "1984")
    
    def test_search_by_author(self):

        result = self.library.search_books(author="Джордж Оруэлл")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].author, "Джордж Оруэлл")

    def test_search_by_year(self):

        result = self.library.search_books(year=1953)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].year, 1953)

    def test_seach_by_year_and_author(self):

        result = self.library.search_books(author="Рэй Брэдбери", year=1953)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].author, "Рэй Брэдбери")

    def test_search_by_title_and_author(self):

        result = self.library.search_books(title="1984", author="Джордж Оруэлл")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "1984")

    def test_search_no_results(self):

        result = self.library.search_books(title="Над пропастью во ржи")

        self.assertEqual(len(result), 0)

    def test_search_empty_library(self):
        
        self.library.books = {}
        result = self.library.search_books(title="1984")

        self.assertEqual(result, [])

class TestSearchByIdBook(unittest.TestCase):

    def setUp(self):

        self.library = Library()

        self.book1 = Book("1984", "Джордж Оруэлл", 1949)
        self.book2 = Book("451 градус по Фаренгейту", "Рэй Брэдбери", 1953)

        self.library.books[self.book1.id] = self.book1
        self.library.books[self.book2.id] = self.book2

    def test_search_success(self):
        
        result = self.library.search_books_by_id(self.book1.id)

        self.assertEqual(result.id, self.book1.id)
        self.assertEqual(result.title, "1984")

    def test_search_invalid(self):

        result = self.library.search_books_by_id("nonexistent_id")
        self.assertIsNone(result)

class TestPrintAllBooks(unittest.TestCase):
    
    def setUp(self):
    
        self.library = Library()

        self.book1 = Book("1984", "Джордж Оруэлл", 1949)
        self.book2 = Book("451 градус по Фаренгейту", "Рэй Брэдбери", 1953)

        self.library.books[self.book1.id] = self.book1
        self.library.books[self.book2.id] = self.book2

    @patch("builtins.print")
    def test_all(self, mock_print):
       
        self.library.all_books()

        mock_print.assert_any_call(f"{'ID':<36} | {'Название':<20} | {'Автор':<20} | {'Год':<6} | {'Статус':<10}")
        mock_print.assert_any_call("-" * 92)

        mock_print.assert_any_call(
            f"{self.book1.id:<36} | {self.book1.title:<20} | {self.book1.author:<20} | {self.book1.year:<6} | {self.book1.status:<10}"
        )
        mock_print.assert_any_call(
            f"{self.book2.id:<36} | {self.book2.title:<20} | {self.book2.author:<20} | {self.book2.year:<6} | {self.book2.status:<10}"
        )

    @patch("builtins.print")
    def test_all_books_empty_library(self, mock_print):

        self.library.books = {}
        self.library.all_books()

        mock_print.assert_called_once_with("Библиотека пуста")

class TestUpdateStatus(unittest.TestCase):

    def setUp(self):

        self.library = Library()

        self.library.VALID_STATUSES = {"в наличии", "выдана"}
        self.book1 = Book("1984", "George Orwell", 1949)

        self.library.books[self.book1.id] = self.book1


    def test_update_status_success(self):

        self.library.update_status(self.book1.id, "Выдана")

        self.assertEqual(self.book1.status, "Выдана")

    def test_update_status_invalid(self):
        
        with self.assertRaises(ValueError) as context:
            self.library.update_status(self.book1.id, "Неизвестный статус")

        self.assertIn("Недопустимый статус", str(context.exception))

    def test_update_status_case_insensitive(self):
        
        self.library.update_status(self.book1.id, "выдана")
        self.assertEqual(self.book1.status, "Выдана")

class TestWriteJson(unittest.TestCase):

    def setUp(self):

        self.library = Library()

        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.add_book("451° по Фаренгейту", "Рэй Брэдбери", 1953)

        self.file_path = "test_library.json"

    def tearDown(self) -> None:

        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_write_json_success(self):

        self.library.write_data_to_json(self.file_path)

        self.assertTrue(os.path.exists(self.file_path))

        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        exp_data = [book.to_dict() for book in self.library.books.values()]

        self.assertEqual(data, exp_data)

    def test_write_json_failed(self):

        invalid_path = "/Этого пути нет/я сказал нет/test_library.json"

        with self.assertRaises(ValueError) as context:
            self.library.write_data_to_json(invalid_path)

        self.assertIn("Ошибка при записи данных в файл", str(context.exception))

class TestReadJson(unittest.TestCase):

    def setUp(self):

        self.library = Library()
        self.path_file = "test_library.json"

        self.books_data = [
            {
                "id": str(uuid.uuid4()),
                "title": "1984",
                "author": "Джордж Оруэлл",
                "year": 1949,
                "status": "В наличии"
            },
            {
                "id": str(uuid.uuid4()),
                "title": "451 градус по Фаренгейту",
                "author": "Рэй Брэдбери",
                "year": 1953,
                "status": "Выдана"  
            }
        ]

        with open(self.path_file, "w", encoding="utf-8") as file:
            json.dump(self.books_data, file, ensure_ascii=False, indent=4)

    def tearDown(self):

            if os.path.exists(self.path_file):
                os.remove(self.path_file)

    def test_read_json_success(self):

        self.library.read_data_from_json(self.path_file)

        self.assertEqual(len(self.library.books), len(self.books_data))

        for book_data in self.books_data:

            book = self.library.books[book_data["id"]]

            self.assertEqual(book.title, book_data["title"])
            self.assertEqual(book.author, book_data["author"])
            self.assertEqual(book.year, book_data["year"])
            self.assertEqual(book.status, book_data["status"])

    def test_read_json_not_found_file(self):

        invalid_path = "/Этого пути нет/я сказал нет/test_library.json"

        with self.assertRaises(FileNotFoundError) as context:
            self.library.read_data_from_json(invalid_path)

        self.assertIn("Файл library.json не найден", str(context.exception))

    def test_read_json_invalid_format(self):

        with open(self.path_file, 'w', encoding='utf-8') as file:
            file.write("Передается строка")

        with self.assertRaises(ValueError) as context:
            self.library.read_data_from_json(self.path_file)

        self.assertIn("Ошибка при чтении данных из файла", str(context.exception))