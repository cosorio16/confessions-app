from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from myapp.models import usuario, Confesion
from myapp.forms import LoginForm, Mensaje
from django.contrib.auth.decorators import login_required
from uuid import uuid4
# Create your views here.


def Home(request):
    print(request.method)
    return render(request, 'home.html')


def logIn(request):
    if request.method == 'GET':
        return render(request, 'logIn.html', {'form': LoginForm()})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            # Crear el objeto usuario
            user = usuario.objects.create(name=username)

            # Guardar el enlace único del usuario en la sesión
            request.session['enlace'] = str(user.enlace)

            return redirect('cnfs')

    else:
        form = LoginForm()

    return render(request, 'logIn.html', {'form': form})


def cnfs(request):
    if request.method == 'POST':
        form = Mensaje(request.POST)
        if form.is_valid():
            mensaje = form.cleaned_data['mensaje']

            # Obtén el enlace único del usuario de la sesión
            enlace = request.session.get('enlace')

            # Obtén el objeto de usuario correspondiente al enlace único
            try:
                user = usuario.objects.get(enlace=enlace)

            except usuario.DoesNotExist:
                # Manejar el caso cuando el enlace no existe
                return render(request, 'home.html')

            # Crea la instancia de la confesión y asígnala al usuario correspondiente
            Confesion.objects.create(mensaje=mensaje, usuario=user)

            return redirect('perfil', enlace=str(user.enlace))
    else:
        form = Mensaje()

    # Filtra las confesiones por el usuario correspondiente
    enlace = request.session.get('enlace')
    confesiones = Confesion.objects.filter(usuario__enlace=enlace)

    return render(request, 'confesiones.html', {'form': form, 'confesiones': confesiones, 'enlace': enlace})


def perfil(request, enlace):
    user = usuario.objects.get(enlace=enlace)
    if request.method == 'POST':
        form = Mensaje(request.POST)
        if form.is_valid():
            mensaje = form.cleaned_data['mensaje']
            Confesion.objects.create(mensaje=mensaje, usuario=user)
    try:
        user = usuario.objects.get(enlace=enlace)
    except usuario.DoesNotExist:
        # Manejar el caso cuando el enlace no existe
        return render(request, 'home.html')

    # Obtén todas las confesiones asociadas al usuario
    confesiones = Confesion.objects.filter(usuario=user)

    form = Mensaje

    return render(request, 'perfil.html', {'user': user, 'confesiones': confesiones, 'form': form, 'nombre': user.name})
