import unittest

from library.book import Book

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

    def test_to_dict(self):

        tested_dict = {
            "id": self.book.id,
            "title": "Великий Гэтсби",
            "author": "Ф. Скотт Фицджеральд",
            "year": 1925,
            "status": "В наличии"
        }

        book_to_dict = self.book.to_dict()

        self.assertEqual(book_to_dict, tested_dict)


    def test_to_dict_miss(self):

        self.book.status = None

        tested_dict = {
            "id": self.book.id,
            "title": "Великий Гэтсби",
            "author": "Ф. Скотт Фицджеральд",
            "year": 1925,
            "status": None
        }

        book_to_dict = self.book.to_dict()

        self.assertEqual(book_to_dict, tested_dict)

if __name__ == '__main__':
    unittest.main()
