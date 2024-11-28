import os
import sys
import json
import uuid
import unittest
from io import StringIO

from library import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):

        self.library = Library()
        self.library.add_book("451 градус по Фаренгейту", "Рэй Брэдбери", 1953)

        self.book_id = next(iter(self.library.books))
    def test_add_book(self):

        book = list(self.library.books.values())[0]

        self.assertEqual(book.title.strip(), "451 градус по Фаренгейту")
        self.assertEqual(book.author.strip(), "Рэй Брэдбери ")
        self.assertEqual(book.year, 1953)

    def test_add_books(self):

        self.library.add_book("Великий Гэтсби", "Ф. Скотт Фицджеральд", 1925)

        self.assertEqual(len(self.library.books), 2)
        book = list(self.library.books.values())[1]
        self.assertEqual(book.title, "Великий Гэтсби")

    #  ______________________________________________________________________________  #

    def test_remove_book(self):

        book_id = next(iter(self.library.books.values())).id

        self.library.remove_book(book_id)

        self.assertEqual(len(self.library.books), 0)

    def test_not_found_remove_book(self):

        invalid_id = str(uuid.uuid4())

        with self.assertRaises(ValueError):
            self.library.remove_book(invalid_id)


#  ______________________________________________________________________________  #


class TestLibrarySearch(unittest.TestCase):

    def setUp(self):

        self.library = Library()
        self.library.add_book("451 градус по Фаренгейту", "Рэй Брэдбери", 1953)
        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.add_book("Великий Гэтсби", "Ф. Скотт Фицджеральд", 1925)
        self.library.add_book("Великий Гэтсби", "Ф. Скотт Фицджеральд", 1925)

    def test_by_title(self):

        results = self.library.search_books(title="Великий Гэтсби")
        result = self.library.search_books(title="451 градус по Фаренгейту")

        self.assertEqual(len(results), 2)
        self.assertEqual(len(result), 1)

    def test_by_author(self):

        results = self.library.search_books(author="Ф. Скотт Фицджеральд")
        result = self.library.search_books(author="Джордж Оруэлл")

        self.assertEqual(len(results), 2)
        self.assertEqual(len(result), 1)

    def test_by_year(self):

        results = self.library.search_books(year=1925)
        result = self.library.search_books(year=1949)

        self.assertEqual(len(results), 2)
        self.assertEqual(len(result), 1)

    def test_comb(self):

        results = self.library.search_books(title="1984", author="Джордж Оруэлл")
        result = self.library.search_books(author="Рэй Брэдбери", year=1953)

        self.assertEqual(len(results), 1)
        self.assertEqual(len(result), 1)

    def test_invalid_key(self):

        with self.assertRaises(ValueError):
            self.library.search_books(genre="Роман")

    def test_no_result(self):

        result = self.library.search_books(title="Мы")
        results = self.library.search_books(author="Евгений Замятин")

        self.assertEqual(len(result), 0)
        self.assertEqual(len(results), 0)


#  ______________________________________________________________________________  #


class TestLibraryAll(unittest.TestCase):

    def setUp(self):

        self.library = Library()

    def test_empty_library(self):

        expected_output = "Библиотека пуста\n"

        current_output = StringIO()
        sys.stdout = current_output
        self.library.all_books()
        sys.stdout = sys.__stdout__

        self.assertEqual(current_output.getvalue(), expected_output)

    def test_all_books(self):

        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.add_book("Мы", "Евгений Замятин", 1920)

        current_output = StringIO()
        sys.stdout = current_output
        self.library.all_books()
        sys.stdout = sys.__stdout__
        output_lines = current_output.getvalue().splitlines()

        self.assertEqual(
            output_lines[0],
            "ID                                   | Название             | Автор                | Год    | Статус    ",
        )
        self.assertEqual(
            output_lines[1],
            "--------------------------------------------------------------------------------------------",
        )
        self.assertEqual(len(output_lines), 4)

        self.assertIn("1984", output_lines[2])
        self.assertIn("Джордж Оруэлл", output_lines[2])
        self.assertIn("Мы", output_lines[3])
        self.assertIn("Евгений Замятин", output_lines[3])


#  ______________________________________________________________________________  #


class TestUpdateStatus(unittest.TestCase):

    def setUp(self):
        
        self.library = Library()

        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.add_book("Мы", "Евгений Замятин", 1920)

        self.book_id = next(iter(self.library.books)).id

    def test_update(self):

        self.library.update_status(self.book_id, "Выдана")

        updated_book = next(iter(self.library.books.values())).id
        
        self.assertEqual(updated_book.status, "Выдана")

    def test_invalid_update(self):

        with self.assertRaises(ValueError) as context:
            self.library.update_status(self.book_id, "Потеряна")

        self.assertIn("Недопустимый статус", str(context.exception))


#  ______________________________________________________________________________  #

class TestJsonLibrary(unittest.TestCase):

    def setUp(self):

        self.library = Library()
        self.test_file = "test_library.json"

        self.library.add_book("1984", "Джордж Оруэлл", 1949)
        self.library.add_book("Мы", "Евгений Замятин", 1920)

    def tearDown(self):

        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_write_data_to_json(self):

        self.library.write_data_to_json(self.test_file)

        self.assertTrue(os.path.exists(self.test_file))

        with open(self.test_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["title"], "1984")
        self.assertEqual(data[1]["title"], "Мы")

    def test_read_data_from_json(self):

        books_data = [
            {
                "id": str(uuid.uuid4()),
                "title": "451 градус по Фаренгейту",
                "author": "Рэй Брэдбери",
                "year": 1953,
                "status": "В наличии",
            }
        ]
        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump(books_data, file, indent=4, ensure_ascii=False)

        self.library.read_data_from_json(self.test_file)

        self.assertEqual(len(self.library.books), 3)

        import_book = list(self.library.books.values())[-1]

        self.assertEqual(import_book.title, "451 градус по Фаренгейту")
        self.assertEqual(import_book.author, "Рэй Брэдбери")
        self.assertEqual(import_book.year, 1953)
        self.assertEqual(import_book.status, "В наличии")

    def test_invalid_json(self):

        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write("invalid json")

        with self.assertRaises(ValueError):
            self.library.read_data_from_json(self.test_file)

    def test_write_empty_json(self):

        empty_library = Library()
        empty_library.write_data_to_json(self.test_file)

        with open(self.test_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(len(data), 0)