from .models import Cliente

def guardar(cliente):
    cliente.save()
    return cliente

def buscar_por_identificacion(identificacion):
    return Cliente.objects.get(identificacion=identificacion)
