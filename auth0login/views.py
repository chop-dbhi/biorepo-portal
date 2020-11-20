from django.shortcuts import render, redirect


def index(request):
    user = request.user
    if user.is_authenticated:
        return redirect(dashboard)
    else:
        return render(request, 'index.html')
