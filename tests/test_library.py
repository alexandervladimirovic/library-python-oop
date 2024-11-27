import sys
import uuid
import unittest
from io import StringIO

from library import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):

        self.library = Library()
        self.library.add_book("451 градус по Фаренгейту", "Рэй Брэдбери", 1953)

    def test_add_book(self):

        self.assertEqual(self.library.books[0].title, "451 градус по Фаренгейту")
        self.assertEqual(self.library.books[0].author, "Рэй Брэдбери")
        self.assertEqual(self.library.books[0].year, 1953)

    def test_add_books(self):

        self.library.add_book("Великий Гэтсби", "Ф. Скотт Фицджеральд", 1925)

        self.assertEqual(len(self.library.books), 2)
        self.assertEqual(self.library.books[1].title, "Великий Гэтсби")

#  ______________________________________________________________________________  #

    def test_remove_book(self):

        book_id = self.library.books[0].id

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
        result = self.library.search_books(title="451 градус по Фаренгейту")

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

        self.assertEqual(output_lines[0], "ID                                   | Название             | Автор                | Год    | Статус    ")
        self.assertEqual(output_lines[1], "--------------------------------------------------------------------------------------------")
        self.assertEqual(len(output_lines), 4)
        
        self.assertIn("1984", output_lines[2])
        self.assertIn("Джордж Оруэлл", output_lines[2])
        self.assertIn("Мы", output_lines[3])
        self.assertIn("Евгений Замятин", output_lines[3])
    
