import unittest
import uuid

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





