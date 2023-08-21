from django.shortcuts import redirect


def redirect_authenticated_user(func):
    """ Decorator to redirect authenticated users away from auth pages."""
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return func(request, *args, **kwargs)
    return wrapper_func
