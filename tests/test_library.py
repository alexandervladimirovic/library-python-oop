import unittest

from library import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = Library()

    def test_add_book(self):

        self.library.add_book("Великий Гэтсби", "Ф. Скотт Фицджеральд", 1925)

        self.assertEqual(self.library.books[0].title, "Великий Гэтсби")
        self.assertEqual(self.library.books[0].author, "Ф. Скотт Фицджеральд")
        self.assertEqual(self.library.books[0].year, 1925)

    def test_add_books(self):

        self.library.add_book("Великий Гэтсби", "Ф. Скотт Фицджеральд", 1925)
        self.library.add_book("1984", "Джордж Оруэлл", 1949)

        self.assertEqual(len(self.library.books), 2)
        self.assertEqual(self.library.books[1].title, "1984")

#  ______________________________________________________________________________  #

