import os
import sys
import json
import uuid
import unittest
from io import StringIO

from library.library import Library
from library.book import Book


class TestReadJson(unittest.TestCase):

    def setUp(self):

        self.library = Library("test_library.json")

        self.library.file_path = "test_library.json" 

    def tearDown(self):
        
        if os.path.exists(self.library.file_path):
            os.remove(self.library.file_path)

    def test_read_success(self):
        
        books_data = [
            {
                "id": str(uuid.uuid4()),
                "title": "1984",
                "author": "Джордж Оруэлл",
                "year": 1949,
                "status": "В наличии"
            }
        ]

        with open(self.library.file_path, "w", encoding="utf-8") as file:
            json.dump(books_data, file, ensure_ascii=False, indent=4)

        
        self.library.read_data_from_json()

        self.assertEqual(len(self.library.books), 1) 
        book = next(iter(self.library.books.values()))
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "Джордж Оруэлл")

    def test_read_empty(self):
        
        with open(self.library.file_path, "w", encoding="utf-8") as file:
            file.write("")

        
        self.library.read_data_from_json()
        self.assertEqual(len(self.library.books), 0)

    def test_file_not_found(self):
        
        if os.path.exists(self.library.file_path):
            os.remove(self.library.file_path)

        
        self.library.read_data_from_json()
        self.assertEqual(len(self.library.books), 0)

    def test_invalid_json(self):
        
        with open(self.library.file_path, "w", encoding="utf-8") as file:
            file.write("Это строка, а не list[dict]")

        
        with self.assertRaises(ValueError):
            self.library.read_data_from_json()

class TestWriteJson(unittest.TestCase):

    def setUp(self):
        self.library = Library("test_library.json")
        self.library.file_path = "test_library.json"

        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.add_book("451° по Фаренгейту", "Рэй Брэдбери", 1953)

    def tearDown(self):
        
        if os.path.exists(self.library.file_path):
            os.remove(self.library.file_path)

    def test_write_success(self):
        
        self.library.write_data_to_json()

        
        self.assertTrue(os.path.exists(self.library.file_path))

        
        with open(self.library.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        exp_data = [book.to_dict() for book in self.library.books.values()]
        self.assertEqual(data, exp_data)

    def test_write_empty(self):
       
        self.library.books = {}  
        self.library.write_data_to_json()

        
        self.assertTrue(os.path.exists(self.library.file_path))

        
        with open(self.library.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data, [])


class TestAddBook(unittest.TestCase):

    def setUp(self):

        self.library = Library("test_library.json")

    def test_add_success(self):
        
        self.library.add_book("1984", "Джордж Оруэлл", 1949)

        
        self.assertEqual(len(self.library.books), 1)

        
        book = next(iter(self.library.books.values()))
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "Джордж Оруэлл")
        self.assertEqual(book.year, 1949)

    def test_add_invalid_title(self):
        
        with self.assertRaises(TypeError):
            self.library.add_book("", "Джордж Оруэлл", 1949)

    def test_add_invalid_author(self):
        
        with self.assertRaises(TypeError):
            self.library.add_book("1984", "", 1949)

    def test_add_invalid_year(self):
        
        with self.assertRaises(TypeError):
            self.library.add_book("1984", "Джордж Оруэлл", "1949")

    def test_add_empty_author(self):
        
        with self.assertRaises(TypeError):
            self.library.add_book("1984", None, 1949)

    def test_add_empty_title(self):
        
        with self.assertRaises(TypeError):
            self.library.add_book(None, "Джордж Оруэлл", 1949)

class TestRemoveBook(unittest.TestCase):

    def setUp(self):
        self.library = Library("test_library.json")
        
        self.book1 = Book("1984", "Джордж Оруэлл", 1949)
        self.library.books[self.book1.id] = self.book1

    def test_remove_success(self):
        
        init_len = len(self.library.books)
        
        
        self.library.remove_book(self.book1.id)

        
        self.assertEqual(len(self.library.books), init_len - 1)
        self.assertNotIn(self.book1.id, self.library.books)

    def test_remove_not_found(self):
        
        invalid_id = str(uuid.uuid4())

        with self.assertRaises(ValueError):
            self.library.remove_book(invalid_id)

    def test_remove_empty(self):
        
        empty_library = Library("test_library.json")

        with self.assertRaises(ValueError):
            empty_library.remove_book(self.book1.id)

class TestSearchBooks(unittest.TestCase):

    def setUp(self):
        self.library = Library("test_library.json")
        
        self.book1 = Book("1984", "Джордж Оруэлл", 1949)
        self.book2 = Book("451 градус по Фаренгейту", "Рэй Брэдбери", 1953)
        self.book3 = Book("Великий Гэтсби", "Ф. Скотт Фицджеральд", 1925)

        self.library.books[self.book1.id] = self.book1
        self.library.books[self.book2.id] = self.book2
        self.library.books[self.book3.id] = self.book3

    def test_search_title(self):
        
        result = self.library.search_books(title="1984")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "1984")

    def test_search_author(self):
        
        result = self.library.search_books(author="Рэй Брэдбери")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].author, "Рэй Брэдбери")

    def test_search_year(self):
        
        result = self.library.search_books(year=1949)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].year, 1949)

    def test_search_title_and_author(self):
        
        result = self.library.search_books(title="1984", author="Джордж Оруэлл")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "1984")
        self.assertEqual(result[0].author, "Джордж Оруэлл")

    def test_search_no_results(self):
        
        result = self.library.search_books(title="Над пропастью во ржи")
        self.assertEqual(len(result), 0)

class TestAllBooks(unittest.TestCase):

    def setUp(self):
        self.library = Library("test_library.json")

        self.book1 = Book("1984", "Джордж Оруэлл", 1949)
        self.book2 = Book("451 градус по Фаренгейту", "Рэй Брэдбери", 1953)

        self.library.books[self.book1.id] = self.book1
        self.library.books[self.book2.id] = self.book2

    def test_all_books(self):
        
        cap_output = StringIO()
        sys.stdout = cap_output

        self.library.all_books()

        
        output = cap_output.getvalue()
        sys.stdout = sys.__stdout__  

        self.assertIn("1984", output)
        self.assertIn("Джордж Оруэлл", output)
        self.assertIn("451 градус по Фаренгейту", output)
        self.assertIn("Рэй Брэдбери", output)

    def test_all_empty(self):
        
        empty_library = Library("empty_library.json")

        
        cap_output = StringIO()
        sys.stdout = cap_output

        empty_library.all_books()

        
        output = cap_output.getvalue()
        sys.stdout = sys.__stdout__  

        self.assertIn("Библиотека пуста", output)

class TestUpdateStatus(unittest.TestCase):

    def setUp(self):
        self.library = Library("test_library.json")
        
        self.book = Book("1984", "Джордж Оруэлл", 1949)
        self.library.books[self.book.id] = self.book

    def test_update_success(self):
        
        new_status = "Выдана"
        self.library.update_status(self.book.id, new_status)

        updated_book = self.library.books[self.book.id]
        self.assertEqual(updated_book.status, new_status.capitalize())

    def test_update_invalid(self):
        
        invalid_status = "В процессе"

        with self.assertRaises(ValueError) as context:
            self.library.update_status(self.book.id, invalid_status)

        self.assertIn("Недопустимый статус", str(context.exception))

    def test_update_status_book_not_found(self):
        
        non_existent_id = str(uuid.uuid4())
        new_status = "В наличии"

        with self.assertRaises(ValueError) as context:
            self.library.update_status(non_existent_id, new_status)

        self.assertIn(f"Книга с id {non_existent_id} не найдена", str(context.exception))


if __name__ == '__main__':
    unittest.main()