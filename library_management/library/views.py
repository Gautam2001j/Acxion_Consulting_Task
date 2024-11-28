from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Transaction,Membership, BookMovie, UserManagement
from .forms import BookIssueForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'signin.html'

    def get_redirect_url(self):
        # Redirect to admin dashboard if the user is an admin
        if self.request.user.is_superuser:
            return reverse_lazy('admin_dash')  # Name of the admin dashboard URL
        # Redirect to user dashboard if the user is not an admin
        else:
            return reverse_lazy('user_dash')

# Check if the user is an admin
def is_admin(user):
    return user.is_authenticated and user.is_superuser

# Dashboard view for admin
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dash.html')

# Add Membership
@user_passes_test(is_admin)
def maintenance_view(request):
    # Restrict access to admin users only
    # if not request.user.is_staff:  # Ensure only admin users can access this view
    #     return HttpResponseForbidden("You are not authorized to access this page.")

    if request.method == "POST":
        action = request.POST.get("action")

        # Process Add Membership
        if action == "add_membership":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            contact_name = request.POST.get("contact_name")
            contact_address = request.POST.get("contact_address")
            aadhar_card_number = request.POST.get("adhar_card_number")
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            membership_duration = request.POST.get("membership")

            Membership.objects.create(
                first_name=first_name,
                last_name=last_name,
                contact_name=contact_name,
                contact_address=contact_address,
                aadhar_card_number=aadhar_card_number,
                start_date=start_date,
                end_date=end_date,
                membership_duration=membership_duration,
            )
            return redirect("maintenance_view")  # Redirect after successful form submission

        # Process Update Membership
        elif action == "update_membership":
            membership_number = request.POST.get("membership_number")
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            membership_extension = request.POST.get("membership_extension")
            remove_membership = request.POST.get("remove_membership")

            try:
                membership = Membership.objects.get(membership_number=membership_number)
                membership.start_date = start_date
                membership.end_date = end_date
                if remove_membership == "yes":
                    membership.delete()
                else:
                    membership.save()
            except Membership.DoesNotExist:
                pass  # Handle membership not found if needed

            return redirect("maintenance_view")

        # Process Add Book/Movie
        elif action == "add_book_movie":
            book_or_movie = request.POST.get("book_or_movie")
            book_movie_name = request.POST.get("book_movie_name")
            date_of_procurement = request.POST.get("date_of_procurement")
            quantity_copies = request.POST.get("quantity_copies")

            BookMovie.objects.create(
                book_or_movie=book_or_movie,
                name=book_movie_name,
                date_of_procurement=date_of_procurement,
                quantity_copies=quantity_copies,
            )
            return redirect("maintenance_view")

        # Process Update Book/Movie
        elif action == "update_book_movie":
            serial_no = request.POST.get("serial_no")
            book_or_movie = request.POST.get("book_or_movie")
            status = request.POST.get("status")
            date = request.POST.get("date")

            try:
                book_movie = BookMovie.objects.get(serial_no=serial_no)
                book_movie.book_or_movie = book_or_movie
                book_movie.status = status
                book_movie.date_of_procurement = date
                book_movie.save()
            except BookMovie.DoesNotExist:
                pass  # Handle book/movie not found if needed

            return redirect("maintenance_view")

        # Process Add or Update User Management
        elif action == "add_user" or action == "update_user":
            name = request.POST.get("name")
            is_new_user = request.POST.get("new_user") == "new_user"
            status = request.POST.get("status") == "on"
            admin = request.POST.get("admin") == "on"

            if is_new_user:
                UserManagement.objects.create(name=name, status=status, admin=admin)
            else:
                try:
                    user = UserManagement.objects.get(name=name)
                    user.status = status
                    user.admin = admin
                    user.save()
                except UserManagement.DoesNotExist:
                    pass  # Handle user not found if needed

            return redirect("maintenance_view")

    # Render the form page
    return render(request, "maintanence.html")


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        is_admin = request.POST.get('is_admin', False)

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)
        if is_admin:
            user.is_staff = True  # Admin users will have staff status
            user.is_superuser = True  # Optional: Make them superusers
        user.save()

        messages.success(request, 'Account created successfully!')
        return redirect('signin')

    return render(request, 'signup.html')


# Sign In View
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:  # Redirect based on admin or user
                return redirect('/admin-dash')  # Replace with your admin URL
            return redirect('/user_dashboard')  # Replace with your user dashboard URL
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')

    return render(request, 'signin.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def admin_dashboard(request):
    # Check if the user is an admin
    if request.user.is_superuser:
        return render(request, 'admin_dash.html')  # Admin dashboard page

@login_required
def user_dashboard(request):
    return render(request, 'user_dash.html')


def issue_book(request):
    if request.method == 'POST':
        form = BookIssueForm(request.POST)
        if form.is_valid():
            book = get_object_or_404(Book, id=form.cleaned_data['book_id'])
            if book.is_available:
                book.is_available = False
                book.save()
                Transaction.objects.create(
                    book=book,
                    user=request.user,
                    issue_date=form.cleaned_data['issue_date'],
                    return_date=form.cleaned_data['return_date']
                )
                return redirect('success_page')
    else:
        form = BookIssueForm()
    return render(request, 'issue_book.html', {'form': form})
