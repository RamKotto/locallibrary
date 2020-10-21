from django.contrib import admin
from .models import Genre, Language, Book, BookInstance, Author

admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)


# Inlines of Book for Author
class BookInline(admin.TabularInline):
    model = Book
    extra = 0 # Hide empty Book tables in Author


# Define the admin class:
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]


# Register the Admin class with the associated model:
admin.site.register(Author, AuthorAdmin)


# Inlines of BookInstance for Book
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0 # Hide empty BookInstance tables in Book


# Register the admin class for Book using the decorator:
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline] # Inlines of BookInstance for Book

# Register the admin class for BookInstance using the decorator:
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')

    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields' : ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields' : ('status', 'due_back')
        }),
    )
