from django.shortcuts import render
from django.http import HttpResponse
from .models import Genre, Language, Book, BookInstance, Author
from django.views import generic


def index(request):
    '''
    Функция отображения для домашней страницы.
    '''
    # Генерация голичеств некоторых главных объектов сайта:
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count() # Метод all() применен по умолчанию

    # Отрисовка HTML шаблона index.html с данными внутри переменной контекста context
    return render(request, 'index.html',
                  context = {
                             'num_books'               : num_books,
                             'num_instances'           : num_instances,
                             'num_instances_available' : num_instances_available,
                             'num_authors'             : num_authors,
                  })


class BookListView(generic.ListView):
    model = Book
    
    # paginate_by = 10
    # template_name = 'books/my_arbitrary_template_name_list.html' # Имя нашего шаблона, и его расположение
    #
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war') # Возвращает книги со словом  'war' в названии
    #
    # def get_context_data(self, **kwargs):
    #     # Получаем базовую реализацию контекста
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Добавляем новую переменную
    #     context['some_data'] = 'This is some data'
    #     return context
