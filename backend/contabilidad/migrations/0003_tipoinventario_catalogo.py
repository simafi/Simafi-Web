# Catálogo TipoInventario por empresa. Los tipos del listado estándar quedan como referencia (codigo_legacy).

import django.db.models.deletion
from django.db import migrations, models

# Listado estándar heredado: se crean TODOS por empresa como referencia editable
LEGACY_TIPOS_REFERENCIA = [
    ("MATERIA_PRIMA", "Materia prima e insumos", 10),
    ("SUMINISTROS", "Suministros de oficina y operación", 20),
    ("REPUESTOS", "Repuestos y accesorios", 30),
    ("MERCADERIA", "Mercadería para reventa", 40),
    ("PRODUCTO_TERMINADO", "Producto terminado", 50),
    ("EMBALAJE", "Embalajes y envases", 60),
    ("SERVICIOS_ALMACENADOS", "Servicios almacenables / pendientes", 70),
    ("OTROS", "Otros / diversos", 90),
]

NOTAS_REF = (
    "Referencia del listado estándar original. Puede renombrar, desactivar o eliminar tipos que no apliquen "
    "(p. ej. ámbito municipal o empresa de agua)."
)


def forwards(apps, schema_editor):
    Inventario = apps.get_model("contabilidad", "Inventario")
    TipoInventario = apps.get_model("contabilidad", "TipoInventario")

    empresas = set(Inventario.objects.values_list("empresa", flat=True))
    # map (empresa, clave legacy) -> id de TipoInventario
    mapa = {}

    for emp in empresas:
        if not emp:
            continue
        for clave, nombre, orden in LEGACY_TIPOS_REFERENCIA:
            tipo, _ = TipoInventario.objects.get_or_create(
                empresa=emp,
                nombre=nombre,
                defaults={
                    "orden": orden,
                    "codigo_legacy": clave,
                    "notas": NOTAS_REF,
                    "is_active": True,
                },
            )
            # Si ya existía un registro homónimo sin codigo_legacy, completar referencia
            if not tipo.codigo_legacy:
                tipo.codigo_legacy = clave
                tipo.notas = tipo.notas or NOTAS_REF
                tipo.save(update_fields=["codigo_legacy", "notas"])
            mapa[(emp, clave)] = tipo.pk

    claves_validas = {c for c, _, _ in LEGACY_TIPOS_REFERENCIA}

    for inv in Inventario.objects.all():
        key = getattr(inv, "tipo_inventario", None)
        if key is None or (isinstance(key, str) and not key.strip()):
            key = "OTROS"
        else:
            key = str(key).strip()
        if key not in claves_validas:
            key = "OTROS"
        pk = mapa.get((inv.empresa, key)) or mapa.get((inv.empresa, "OTROS"))
        if pk:
            inv.tipo_catalogo_id = pk
            inv.save(update_fields=["tipo_catalogo_id"])


def backwards_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("contabilidad", "0002_inventario_tipo_nomenclatura"),
    ]

    operations = [
        migrations.CreateModel(
            name="TipoInventario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("created_by", models.CharField(blank=True, max_length=100, null=True, verbose_name="Creado por")),
                ("updated_by", models.CharField(blank=True, max_length=100, null=True, verbose_name="Actualizado por")),
                ("empresa", models.CharField(db_index=True, max_length=10, verbose_name="Empresa/Municipio")),
                ("nombre", models.CharField(max_length=120, verbose_name="Nombre del tipo")),
                (
                    "orden",
                    models.PositiveSmallIntegerField(
                        default=0,
                        help_text="Prioridad en listas y reportes (menor = primero).",
                        verbose_name="Orden",
                    ),
                ),
                (
                    "notas",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Opcional: ámbito de uso (municipal, saneamiento, etc.).",
                        verbose_name="Notas internas",
                    ),
                ),
                (
                    "codigo_legacy",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Clave del listado estándar anterior (p. ej. MATERIA_PRIMA); vacío si el tipo es totalmente nuevo.",
                        max_length=30,
                        verbose_name="Código de referencia (heredado)",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tipo de inventario (catálogo)",
                "verbose_name_plural": "Tipos de inventario (catálogo)",
                "db_table": "cont_tipo_inventario",
                "ordering": ["empresa", "orden", "nombre"],
                "unique_together": {("empresa", "nombre")},
            },
        ),
        migrations.AddField(
            model_name="inventario",
            name="tipo_catalogo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="inventarios",
                to="contabilidad.tipoinventario",
                verbose_name="Tipo de inventario",
            ),
        ),
        migrations.RunPython(forwards, backwards_noop),
        migrations.RemoveField(
            model_name="inventario",
            name="tipo_inventario",
        ),
        migrations.RenameField(
            model_name="inventario",
            old_name="tipo_catalogo",
            new_name="tipo_inventario",
        ),
    ]
