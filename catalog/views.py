import datetime
from django.contrib import messages
from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
# Create your views here
@login_required
def index(request):
    """View function for home page of site."""
    subject = 'Thank you for registering to our site' 
    message = 'it means a world to us'
    email_from = '116220522@umail.ucc.ie'
    recipient_list = [ '116220522@umail.ucc.ie', ]
    send_mail(subject, message, email_from, recipient_list)

    # Generate counts of some of the main project
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1  

    context = {
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_visits': num_visits,
            }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

#class LoginRequiredMixin
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LibrarianSetBookListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all the books on loan to librarians."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 3
    permission_required = 'catalog.can_mark_returned'
    #redirect_field_name = '/login/' 
    #login_url = '/login/'
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

    #def handle_no_permission(self):
        # add custom message
        #messages.error(self.request, 'You have no permission')
        #return super(LibrarianSetBookListView, self).handle_no_permission()

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method =='POST':

        # Create a form instance and populate it with data from the request
        # (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid.
        if form.is_valid():
            # Process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # Rediect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

     # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today()+ datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    context = {
            'form': form,
            'book_instance': book_instance,
    }
    return render(request, 'catalog/book_renew_librarian.html', context=context)

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books') 
    permission_required = 'catalog.can_mark_returned'
