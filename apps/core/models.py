from django.db import models


class ContactMessage(models.Model):
    name = models.CharField("Nombre", max_length=120)
    email = models.EmailField("Correo")
    message = models.TextField("Mensaje")
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField("Atendido", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"

    def __str__(self):
        return f"{self.name} <{self.email}>"
