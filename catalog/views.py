from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Genre, Language, Book, BookInstance, Author
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime
from .forms import RenewBookForm


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


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    Вьюшка для обновления даты возврата книги.
    С использованием form.
    """
    book_inst = get_object_or_404(BookInstance, pk = pk)

    # if this is a POST request
    if request.method == 'POST':

        # create a form instance
        form = RenewBookForm(request.POST)

        #check if the form is valid
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new url
            return HttpResponseRedirect(reverse('borrowed-books'))

    # if this is a GET, create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks = 3)
        form = RenewBookForm(initial = {'renewal_date' : proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html',
                  {'form' : form, 'bookinst' : book_inst})


# Ниже предоставлены 3 вьюшки, с помощью которых можно избежать отдельного создания форм
# Create and Update будут искать шаблон model_name_form.html
# Delete будет искать model_name_confirm_delete.html
# Это можно переопределить с помощью поля 'template_name_suffix'
class AuthorCreate(CreateView):
    model = Author   # Модель, поля которой нам нужны (что мы и будем создавать)
    fields = '__all__'   # Добавляем все поля модели
    initial = {'date_of_birth' : '18.11.1990',}  # Данные, которые будут предложены


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name',
              'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')   # Редирект, после удаления автора


class BookCreate(CreateView):
    model = Book
    fields = '__all__'


# Аналогично Author
class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
