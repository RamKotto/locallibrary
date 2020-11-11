from django.shortcuts import render
from django.http import HttpResponse
from .models import Genre, Language, Book, BookInstance, Author
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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

    #Добавляем счетчик посещения главной страницы пользователем
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    #Удаляем значение счетчика посещений
    #del request.session['num_visits']

    # Отрисовка HTML шаблона index.html с данными внутри переменной контекста context
    return render(request, 'index.html',
                  context = {
                             'num_books'               : num_books,
                             'num_instances'           : num_instances,
                             'num_instances_available' : num_instances_available,
                             'num_authors'             : num_authors,
                             'num_visits'              : num_visits,  # Счетчик посещения
                  })


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

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


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Модель для вывода списка книг, которые взял пользователь.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact = 'o').order_by('due_back')


class LoanedBooksListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """
    Модель для просмотра всех заимствованных книг, для библиотекарей
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    permission_required = ("catalog.can_mark_returned",)

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact = 'o').order_by('due_back')
