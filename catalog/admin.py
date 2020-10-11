from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# Register your models here.

#admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)

# Define the admin class 
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)



# Add inline eaditing: add BookInstance information inline to Book
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0 # set extra instances to zero


# Register the Admin classes for Book using decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
   list_display = ('title', 'author', 'display_genre')
   inlines = [BooksInstanceInline]
# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
   list_display = ('id', 'book', 'status',  'borrower', 'imprint', 'due_back')
   list_filter = ('status', 'due_back')
   fieldsset = (
           (None, {'fields': ('book', 'imprint', 'id')}),
           ('Availability', {'fields': ('status', 'borrower', 'due_back')}),
           )
