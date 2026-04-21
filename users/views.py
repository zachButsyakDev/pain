from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import SignUpForm


# main function, handles signup page
def signup(request):

    # If user is already logged in, send them to home page
    if request.user.is_authenticated:
        return redirect('home')

    # If the form was submitted (POST request)
    # handle submitted form ( username, password, etc.)
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        # Check if the form data is valid (password match, valid email)
        if form.is_valid():
            user = form.save()  # Create the user in the database

            login(request, user)  # Automatically log them in

            # Show success message
            messages.success(request, 'Your account was created successfully.')

            return redirect('home')  # Send them to home page

        else:
            # Show error message if something is wrong
            messages.error(request, 'Please correct the errors below.')

    else:
        # If it's a GET request, just show an empty form
        form = SignUpForm()

    # Render the signup page and pass the form to it
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')