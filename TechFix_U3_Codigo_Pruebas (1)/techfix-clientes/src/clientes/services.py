from django.core.exceptions import PermissionDenied, ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from . import dao
from .models import Cliente

DUPLICADO = "Ya existe un cliente con esta identificación"

def validar_identificacion(valor):
    valor = (valor or "").strip()
    if not valor:
        raise ValidationError("La identificación es obligatoria")
    return valor

def validar_nombres(valor):
    valor = (valor or "").strip()
    if not valor:
        raise ValidationError("Los nombres son obligatorios")
    return valor

def validar_correo(valor):
    valor = (valor or "").strip()
    if valor:
        try:
            validate_email(valor)
        except ValidationError:
            raise ValidationError("Ingrese un correo electrónico válido")
    return valor

def puede_modificar(usuario):
    return bool(usuario.is_authenticated and usuario.has_perm("clientes.change_cliente"))

def _validar(cliente):
    cliente.identificacion = validar_identificacion(cliente.identificacion)
    cliente.nombres = validar_nombres(cliente.nombres)
    cliente.correo = validar_correo(cliente.correo)
    otros = Cliente.objects.filter(identificacion=cliente.identificacion).exclude(pk=cliente.pk)
    if otros.exists():
        raise ValidationError(DUPLICADO)
    cliente.full_clean(validate_unique=False)

def registrar_cliente(usuario, datos):
    if not usuario.is_authenticated or not usuario.has_perm("clientes.add_cliente"):
        raise PermissionDenied("No tiene permiso para registrar clientes")
    cliente = Cliente(**datos)
    try:
        with transaction.atomic():
            _validar(cliente)
            return dao.guardar(cliente)
    except IntegrityError:
        if Cliente.objects.filter(identificacion=cliente.identificacion).exists():
            raise ValidationError(DUPLICADO)
        raise

def actualizar_cliente(usuario, pk, datos):
    if not puede_modificar(usuario):
        raise PermissionDenied("No tiene permiso para modificar clientes")
    try:
        with transaction.atomic():
            cliente = Cliente.objects.select_for_update().get(pk=pk)
            for campo in ("identificacion", "nombres", "telefono", "correo", "direccion"):
                if campo in datos:
                    setattr(cliente, campo, datos[campo])
            _validar(cliente)
            return dao.guardar(cliente)
    except IntegrityError:
        if Cliente.objects.filter(identificacion=cliente.identificacion).exclude(pk=pk).exists():
            raise ValidationError(DUPLICADO)
        raise
