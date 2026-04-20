# -*- coding: utf-8 -*-
from django import forms

from core.models import Municipio
from core.module_access import MODULOS_SISTEMA
from usuarios.models import Usuario, UsuarioAccesoModulo, UsuarioRol, Rol, Permiso


_WIDGET_TEXT = forms.TextInput(attrs={'class': 'form-control'})
_WIDGET_EMAIL = forms.EmailInput(attrs={'class': 'form-control'})
_WIDGET_SELECT = forms.Select(attrs={'class': 'form-control'})
_WIDGET_PWD = forms.PasswordInput(attrs={'class': 'form-control'}, render_value=False)
_WIDGET_TEXTAREA = forms.Textarea(attrs={'class': 'form-control', 'rows': 2})


class RolForm(forms.ModelForm):
    """Alta/edición de roles y permisos asociados (catálogo `Permiso`)."""

    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'permisos', 'is_active']
        labels = {
            'nombre': 'Nombre del rol',
            'descripcion': 'Descripción',
            'permisos': 'Permisos',
            'is_active': 'Activo',
        }
        widgets = {
            'nombre': _WIDGET_TEXT,
            'descripcion': _WIDGET_TEXTAREA,
            'permisos': forms.CheckboxSelectMultiple(),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permisos'].queryset = Permiso.objects.filter(is_active=True).order_by('modulo', 'nombre')
        self.fields['permisos'].required = False


def _campos_modulo():
    fields = {}
    for code, label in MODULOS_SISTEMA:
        fields[f'modulo_{code}'] = forms.BooleanField(
            required=False,
            label=f'Acceso a {label}',
        )
        fields[f'pwd_{code}'] = forms.CharField(
            required=False,
            label=f'Contraseña ({label})',
            widget=_WIDGET_PWD,
        )
    return fields


class UsuarioSistemaForm(forms.Form):
    usuario = forms.CharField(max_length=15, label='Usuario', widget=_WIDGET_TEXT)
    nombre = forms.CharField(max_length=100, required=False, label='Nombre completo', widget=_WIDGET_TEXT)
    email = forms.EmailField(required=False, label='Correo', widget=_WIDGET_EMAIL)
    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all().order_by('codigo'),
        required=False,
        label='Municipio',
        empty_label='— Sin municipio (solo superusuario global) —',
        widget=_WIDGET_SELECT,
    )
    is_active = forms.BooleanField(required=False, initial=True, label='Activo')
    es_superusuario = forms.BooleanField(
        required=False,
        label='Superusuario (puede dejar municipio vacío para alcance global y gestionar cualquier municipio)',
    )
    roles = forms.ModelMultipleChoiceField(
        queryset=Rol.objects.filter(is_active=True).order_by('nombre'),
        required=False,
        label='Roles asignados',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'rol-check'}),
    )
    password_acceso = forms.CharField(
        required=False,
        label='Contraseña del menú modular (login /login/)',
        widget=_WIDGET_PWD,
        help_text=(
            'Al crear usuario: obligatoria. Es la clave para entrar en el login principal con el mismo '
            'usuario y el municipio elegido (debe coincidir con el municipio asignado aquí).'
        ),
    )
    password_acceso_confirm = forms.CharField(
        required=False,
        label='Confirmar contraseña del menú modular',
        widget=_WIDGET_PWD,
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        for name, field in _campos_modulo().items():
            self.fields[name] = field
        if self.instance:
            self.fields['usuario'].disabled = True
            self.initial.setdefault('usuario', self.instance.usuario)
            self.initial.setdefault('nombre', self.instance.nombre)
            self.initial.setdefault('email', self.instance.email)
            self.initial.setdefault('municipio', self.instance.municipio_id)
            self.initial.setdefault('is_active', self.instance.is_active)
            self.initial.setdefault('es_superusuario', self.instance.es_superusuario)
            for code, _lbl in MODULOS_SISTEMA:
                has = UsuarioAccesoModulo.objects.filter(
                    usuario=self.instance,
                    codigo_modulo=code,
                    is_active=True,
                ).exists()
                self.initial[f'modulo_{code}'] = has
            ids = UsuarioRol.objects.filter(
                usuario=self.instance,
                is_active=True,
            ).values_list('rol_id', flat=True)
            self.initial['roles'] = list(ids)

    def clean_usuario(self):
        u = (self.cleaned_data.get('usuario') or '').strip()
        if not u:
            raise forms.ValidationError('Indique un nombre de usuario.')
        return u

    def clean(self):
        cleaned = super().clean()
        if not cleaned:
            return cleaned
        es_sup = cleaned.get('es_superusuario')
        mun = cleaned.get('municipio')
        usu = (cleaned.get('usuario') or '').strip()
        if self.instance and not usu:
            usu = (self.instance.usuario or '').strip()

        p_acc = (cleaned.get('password_acceso') or '').strip()
        p_cf = (cleaned.get('password_acceso_confirm') or '').strip()
        if not self.instance:
            if not p_acc:
                raise forms.ValidationError(
                    'Defina la contraseña de acceso al menú modular (página /login/). '
                    'Sin ella el usuario no podrá iniciar sesión con la clave que usted elija.'
                )
            if p_acc != p_cf:
                raise forms.ValidationError('La confirmación de la contraseña del menú modular no coincide.')
            if len(p_acc) < 4:
                raise forms.ValidationError('La contraseña de acceso debe tener al menos 4 caracteres.')
        elif p_acc or p_cf:
            if not p_acc or not p_cf:
                raise forms.ValidationError(
                    'Para cambiar la contraseña del menú modular, complete ambos campos o déjelos vacíos.'
                )
            if p_acc != p_cf:
                raise forms.ValidationError('La confirmación de la contraseña del menú modular no coincide.')
            if len(p_acc) < 4:
                raise forms.ValidationError('La contraseña de acceso debe tener al menos 4 caracteres.')

        if not es_sup and not mun:
            raise forms.ValidationError(
                'Los usuarios que no son superusuario deben tener un municipio asignado.'
            )

        if not self.instance:
            if es_sup and not mun:
                if usu and Usuario.objects.filter(empresa='', usuario=usu).exists():
                    raise forms.ValidationError(
                        'Ya existe un superusuario global con ese nombre de usuario.'
                    )
            elif mun and usu and Usuario.objects.filter(empresa=mun.codigo, usuario=usu).exists():
                raise forms.ValidationError('Ya existe un usuario con ese nombre en el municipio seleccionado.')
        else:
            if es_sup and not mun:
                if usu and Usuario.objects.filter(empresa='', usuario=usu).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError(
                        'Ya existe otro superusuario global con ese nombre de usuario.'
                    )
            elif mun and usu:
                if Usuario.objects.filter(empresa=mun.codigo, usuario=usu).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('Ya existe otro usuario con ese nombre en el municipio seleccionado.')

        if es_sup:
            return cleaned
        ok = False
        for code, _lbl in MODULOS_SISTEMA:
            if cleaned.get(f'modulo_{code}'):
                pwd = (cleaned.get(f'pwd_{code}') or '').strip()
                if pwd:
                    ok = True
                elif self.instance:
                    exists = UsuarioAccesoModulo.objects.filter(
                        usuario=self.instance,
                        codigo_modulo=code,
                        is_active=True,
                    ).exists()
                    if exists:
                        ok = True
                    else:
                        raise forms.ValidationError(
                            f'Indique contraseña para el módulo {code} o desmarque el acceso.'
                        )
                else:
                    raise forms.ValidationError(
                        f'Indique contraseña para el módulo {code} o desmarque el acceso.'
                    )
        if not ok:
            raise forms.ValidationError(
                'Un usuario que no es superusuario debe tener al menos un módulo con contraseña definida.'
            )
        return cleaned

    def _guardar_roles(self, user, asignado_por):
        if asignado_por is None:
            return
        selected = list(self.cleaned_data.get('roles') or [])
        selected_ids = {r.pk for r in selected}
        for ur in UsuarioRol.objects.filter(usuario=user):
            if ur.rol_id not in selected_ids:
                ur.is_active = False
                ur.save(update_fields=['is_active', 'updated_at'])
        for rol in selected:
            obj, created = UsuarioRol.objects.get_or_create(
                usuario=user,
                rol=rol,
                defaults={'asignado_por': asignado_por, 'is_active': True},
            )
            if not created:
                upd = []
                if not obj.is_active:
                    obj.is_active = True
                    upd.append('is_active')
                if obj.asignado_por_id != asignado_por.pk:
                    obj.asignado_por = asignado_por
                    upd.append('asignado_por')
                if upd:
                    upd.append('updated_at')
                    obj.save(update_fields=upd)

    def save(self, asignado_por=None):
        data = self.cleaned_data
        municipio = data.get('municipio')
        es_sup = data.get('es_superusuario', False)
        if es_sup and not municipio:
            mun_fk = None
            emp = ''
        else:
            mun_fk = municipio
            emp = municipio.codigo if municipio else ''

        if self.instance:
            user = self.instance
            user.nombre = data.get('nombre') or ''
            user.email = data.get('email') or ''
            user.municipio = mun_fk
            user.empresa = emp
            user.is_active = data.get('is_active', True)
            user.es_superusuario = data.get('es_superusuario', False)
            p_new = (data.get('password_acceso') or '').strip()
            if p_new:
                user.password = p_new
            user.save()
        else:
            user = Usuario(
                usuario=data['usuario'].strip(),
                nombre=data.get('nombre') or '',
                email=data.get('email') or '',
                municipio=mun_fk,
                empresa=emp,
                password=(data.get('password_acceso') or '').strip(),
                is_active=data.get('is_active', True),
                es_superusuario=data.get('es_superusuario', False),
            )
            user.save()

        self._guardar_roles(user, asignado_por)

        if user.es_superusuario:
            UsuarioAccesoModulo.objects.filter(usuario=user).update(is_active=False)
            return user

        for code, _lbl in MODULOS_SISTEMA:
            want = data.get(f'modulo_{code}')
            pwd = (data.get(f'pwd_{code}') or '').strip()
            acc = UsuarioAccesoModulo.objects.filter(usuario=user, codigo_modulo=code).first()
            if not want:
                if acc:
                    acc.is_active = False
                    acc.save(update_fields=['is_active', 'updated_at'])
                continue
            if pwd:
                if acc:
                    acc.password = pwd
                    acc.is_active = True
                    acc.save()
                else:
                    UsuarioAccesoModulo.objects.create(
                        usuario=user,
                        codigo_modulo=code,
                        password=pwd,
                    )
            elif acc and acc.is_active:
                pass
            else:
                pass
        return user
