import unittest

from library import Book

class TestBook(unittest.TestCase):

    def setUp(self):
        self.book = Book("Великий Гэтсби", "Ф. Скотт Фицджеральд", 1925)

    def test_init(self):
        self.assertEqual(self.book.title, "Великий Гэтсби")
        self.assertEqual(self.book.author, "Ф. Скотт Фицджеральд")
        self.assertEqual(self.book.year, 1925)
        self.assertEqual(self.book.status, "В наличии")
        self.assertIsInstance(self.book.id, str)

    def test_repr(self):

        repr_out = repr(self.book)

        self.assertIn("ID:", repr_out)
        self.assertIn("Великий Гэтсби", repr_out)
        self.assertIn("Ф. Скотт Фицджеральд", repr_out)
        self.assertIn("1925", repr_out)
        self.assertIn("В наличии", repr_out)

    def test_eq(self):

        book1 = self.book
        book2 = Book("1984", "Джордж Оруэлл", 1949)
        self.assertFalse(book1 == book2)

        book3 = Book("Великий Гэтсби", "Ф. Скотт Фицджеральд", 1925)
        self.assertFalse(book1 == book3)

        book5 = book1
        self.assertTrue(book1 == book5)

