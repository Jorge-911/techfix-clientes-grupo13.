from unittest.mock import Mock
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import SimpleTestCase, TransactionTestCase, TestCase
from django.urls import reverse
from clientes import dao, services
from clientes.models import Cliente

DATOS = {
    "identificacion": "TEST-CLI-001",
    "nombres": "Ana Prueba",
    "telefono": "0990000001",
    "correo": "ana.prueba@example.com",
    "direccion": "Calle de Prueba 100",
}

def usuario_autorizado():
    usuario = get_user_model().objects.create_user(username="operador_prueba")
    usuario.user_permissions.set(Permission.objects.filter(
        content_type__app_label="clientes",
        codename__in=["add_cliente", "change_cliente", "view_cliente"],
    ))
    return usuario

class ValidacionesTest(SimpleTestCase):
    def test_cp_u01_identificacion_vacia(self):
        with self.assertRaisesMessage(ValidationError, "La identificación es obligatoria"):
            services.validar_identificacion("   ")

    def test_cp_u02_nombres_vacios(self):
        with self.assertRaisesMessage(ValidationError, "Los nombres son obligatorios"):
            services.validar_nombres("")

    def test_cp_u03_correo_invalido(self):
        with self.assertRaisesMessage(ValidationError, "Ingrese un correo electrónico válido"):
            services.validar_correo("ana.prueba@")

    def test_cp_u04_normalizacion(self):
        self.assertEqual(services.validar_identificacion("  TEST-CLI-001  "), "TEST-CLI-001")

    def test_cp_u05_permiso_denegado(self):
        usuario = Mock(is_authenticated=True)
        usuario.has_perm.return_value = False
        self.assertFalse(services.puede_modificar(usuario))
        usuario.has_perm.assert_called_once_with("clientes.change_cliente")

class PersistenciaClientesTest(TransactionTestCase):
    def setUp(self):
        self.usuario = usuario_autorizado()

    def test_cp_i01_persistir_y_recuperar_cliente(self):
        """CP-I01 crítico: servicio + DAO + ORM + base real de pruebas."""
        cantidad_inicial = Cliente.objects.count()
        creado = services.registrar_cliente(self.usuario, DATOS.copy())
        pk_original = creado.pk
        del creado
        recuperado = dao.buscar_por_identificacion(DATOS["identificacion"])
        self.assertIsNotNone(recuperado.pk)
        self.assertEqual(recuperado.pk, pk_original)
        self.assertEqual(Cliente.objects.count(), cantidad_inicial + 1)
        self.assertEqual(Cliente.objects.filter(identificacion=DATOS["identificacion"]).count(), 1)
        for campo, esperado in DATOS.items():
            with self.subTest(campo=campo):
                self.assertEqual(getattr(recuperado, campo), esperado)

    def test_cp_i02_duplicado(self):
        services.registrar_cliente(self.usuario, DATOS.copy())
        cantidad = Cliente.objects.count()
        duplicado = {**DATOS, "identificacion": "  TEST-CLI-001  ", "nombres": "Cambio indebido"}
        with self.assertRaisesMessage(ValidationError, services.DUPLICADO):
            services.registrar_cliente(self.usuario, duplicado)
        self.assertEqual(Cliente.objects.count(), cantidad)
        recuperado = dao.buscar_por_identificacion(DATOS["identificacion"])
        for campo, esperado in DATOS.items():
            self.assertEqual(getattr(recuperado, campo), esperado)

    def test_cp_i03_actualizacion_autorizada(self):
        creado = services.registrar_cliente(self.usuario, DATOS.copy())
        cantidad = Cliente.objects.count()
        services.actualizar_cliente(self.usuario, creado.pk, {"telefono": "0990000002"})
        recuperado = dao.buscar_por_identificacion(DATOS["identificacion"])
        self.assertEqual(recuperado.pk, creado.pk)
        self.assertEqual(Cliente.objects.count(), cantidad)
        for campo, esperado in {**DATOS, "telefono": "0990000002"}.items():
            self.assertEqual(getattr(recuperado, campo), esperado)

class SeguridadHTTPTest(TestCase):
    """Comprobaciones adicionales; no sustituyen aceptación en navegador."""
    def test_post_sin_permiso_no_modifica(self):
        propietario = usuario_autorizado()
        cliente = services.registrar_cliente(propietario, DATOS.copy())
        limitado = get_user_model().objects.create_user(username="limitado")
        self.client.force_login(limitado)
        respuesta = self.client.post(reverse("clientes:editar", args=[cliente.pk]), {**DATOS, "telefono": "0990000002"})
        self.assertContains(respuesta, "No tiene permiso para modificar clientes", status_code=403)
        cliente.refresh_from_db()
        self.assertEqual(cliente.telefono, DATOS["telefono"])
        with self.assertRaises(PermissionDenied):
            services.actualizar_cliente(limitado, cliente.pk, {"telefono": "0990000002"})

    def test_flujo_http_autorizado(self):
        usuario = usuario_autorizado()
        self.client.force_login(usuario)
        respuesta = self.client.post(reverse("clientes:nuevo"), DATOS, follow=True)
        self.assertContains(respuesta, "Cliente registrado correctamente")
        cliente = Cliente.objects.get(identificacion=DATOS["identificacion"])
        respuesta = self.client.get(reverse("clientes:inicio"), {"q": DATOS["identificacion"]})
        self.assertEqual(list(respuesta.context["clientes"]), [cliente])
        respuesta = self.client.post(reverse("clientes:editar", args=[cliente.pk]), {**DATOS, "telefono": "0990000002"}, follow=True)
        self.assertContains(respuesta, "Cliente actualizado correctamente")
        respuesta = self.client.get(reverse("clientes:detalle", args=[cliente.pk]))
        self.assertContains(respuesta, "0990000002")
