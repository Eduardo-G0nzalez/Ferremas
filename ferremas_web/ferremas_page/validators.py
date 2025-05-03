import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordComplejidadValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("La contraseña debe tener al menos 8 caracteres."),
                code='password_too_short',
            )

        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra mayúscula."),
                code='password_no_upper',
            )

        if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\/\-=]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un carácter especial."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe tener al menos 8 caracteres, una letra mayúscula y un carácter especial."
        )
