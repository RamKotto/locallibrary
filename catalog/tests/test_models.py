from django.test import TestCase
from catalog.models import *
import datetime


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name = 'Max', last_name='Payne')

    def test_first_name_label(self):
        # Получаем объект автора по ID
        author = Author.objects.get(id = 1)
        # Получаем отображаемое название поля 'first_name' через options
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id = 1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id = 1)
        field_length = author._meta.get_field('first_name').max_length
        self.assertEqual(field_length, 100)

    def test_author_object_name(self):
        author = Author.objects.get(id = 1)
        expected_object_name = f'{author.first_name} {author.last_name}'
        self.assertEqual(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id = 1)
        self.assertEqual(author.get_absolute_url(), '/catalog/authors/1')


class BookInstanceModelTest(TestCase):

    def setUp(self):
        # # Создаем "язык"
        self.language = Language.objects.create(name = 'English')
        # # Создаем жанры для книги
        # genre_1 = Genre.objects.create(name = 'Fantasy')
        # genre_2 = Genre.objects.create(name = 'Drama')
        # # Создаем автора для книги
        self.author = Author.objects.create(first_name = 'Max', last_name='Payne')
        # # Создаем книгу
        self.book = Book.objects.create(title = 'Warcraft III',
                                        author = self.author,
                                        summary = 'The Book about Warcraft',
                                        isbn = '111111-111111',
                                        language = self.language)
        # # т.к. Жанр это m2m field, добавляем его отдельно
        # book.genre.add(1, 2)
        # book.save()
        # # Создаем физичесике копии книги:
        BookInstance.objects.create(book = self.book, imprint = 'Blizzard')
        BookInstance.objects.create(book = self.book, imprint = 'Blizzard')

    def test_book_inst_count(self):
        query = BookInstance.objects.all()
        expected_count = query.count()
        self.assertEqual(expected_count, 2)

    def test_book_inst_unique_uuid(self):
        query = list(BookInstance.objects.all())
        self.assertTrue(query[0].id != query[1].id)

    def test_book_inst_is_overdue(self):
        query = list(BookInstance.objects.all())
        book_inst_1 = query[0]
        book_inst_2 = query[1]
        book_inst_1.status = 'o'
        book_inst_2.status = 'o'
        book_inst_1.due_back = datetime.date.today() - datetime.timedelta(weeks = 1)
        book_inst_2.due_back = datetime.date.today() + datetime.timedelta(weeks = 1)
        self.assertTrue(book_inst_1.is_overdue)
        self.assertFalse(book_inst_2.is_overdue)







#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  ПРИМЕР:
# class YourTestClass(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass
#
#     def setUp(self):
#         print("setUp: Run once for every test method to setup clean data.")
#         pass
#
#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)
#
#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(False)
#
#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
