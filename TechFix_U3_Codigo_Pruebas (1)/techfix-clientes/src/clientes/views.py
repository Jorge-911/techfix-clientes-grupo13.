from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ClienteForm
from .models import Cliente
from .services import registrar_cliente, actualizar_cliente, puede_modificar

@login_required
@permission_required("clientes.view_cliente", raise_exception=True)
def inicio(request):
    consulta = request.GET.get("q", "").strip()
    clientes = Cliente.objects.order_by("nombres")
    if consulta:
        clientes = clientes.filter(identificacion=consulta)
    return render(request, "clientes/inicio.html", {"clientes": clientes, "q": consulta})

@login_required
@permission_required("clientes.view_cliente", raise_exception=True)
def detalle(request, pk):
    return render(request, "clientes/detalle.html", {"cliente": get_object_or_404(Cliente, pk=pk)})

@login_required
@permission_required("clientes.add_cliente", raise_exception=True)
def nuevo(request):
    form = ClienteForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        try:
            cliente = registrar_cliente(request.user, form.cleaned_data)
        except ValidationError as error:
            form.add_error(None, error)
        else:
            messages.success(request, "Cliente registrado correctamente")
            return redirect("clientes:detalle", pk=cliente.pk)
    return render(request, "clientes/form.html", {"form": form, "titulo": "Nuevo cliente"})

@login_required
def editar(request, pk):
    if not puede_modificar(request.user):
        return render(request, "clientes/denegado.html", status=403)
    cliente = get_object_or_404(Cliente, pk=pk)
    initial = {campo: getattr(cliente, campo) for campo in ClienteForm.base_fields}
    form = ClienteForm(request.POST if request.method == "POST" else None, initial=initial)
    if request.method == "POST" and form.is_valid():
        try:
            actualizar_cliente(request.user, pk, form.cleaned_data)
        except ValidationError as error:
            form.add_error(None, error)
        else:
            messages.success(request, "Cliente actualizado correctamente")
            return redirect("clientes:detalle", pk=pk)
    return render(request, "clientes/form.html", {"form": form, "titulo": "Editar cliente"})
