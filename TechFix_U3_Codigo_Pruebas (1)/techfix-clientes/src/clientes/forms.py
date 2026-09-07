from django import forms
from .services import validar_identificacion, validar_nombres, validar_correo

class ClienteForm(forms.Form):
    identificacion = forms.CharField(label="Identificación", max_length=50, required=False)
    nombres = forms.CharField(max_length=150, required=False)
    telefono = forms.CharField(label="Teléfono", max_length=30, required=False)
    correo = forms.CharField(max_length=254, required=False)
    direccion = forms.CharField(label="Dirección", max_length=250, required=False)

    def clean_identificacion(self):
        return validar_identificacion(self.cleaned_data.get("identificacion"))

    def clean_nombres(self):
        return validar_nombres(self.cleaned_data.get("nombres"))

    def clean_correo(self):
        return validar_correo(self.cleaned_data.get("correo"))
