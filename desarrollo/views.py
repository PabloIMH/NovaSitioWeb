from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')  # Mantener el home como estaba

# Vista personalizada para el login
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirigir según el tipo de usuario
            if user.is_superuser or user.is_staff:
                return redirect('/admin/')  # Redirige al panel de administración
            else:
                 return redirect('/cliente/')  # Redirige a la página del cliente
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista para la página del cliente
@login_required
def cliente_view(request):
    return render(request, 'cliente.html')  # Página para los usuarios clientes
