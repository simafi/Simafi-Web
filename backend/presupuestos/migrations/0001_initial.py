from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contabilidad", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Fondo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio")),
                ("codigo", models.CharField(max_length=20, verbose_name="Código")),
                ("nombre", models.CharField(max_length=200, verbose_name="Nombre")),
                ("descripcion", models.TextField(blank=True, null=True, verbose_name="Descripción")),
            ],
            options={
                "db_table": "presu_fondo",
                "verbose_name": "Fondo",
                "verbose_name_plural": "Fondos",
                "ordering": ["codigo"],
                "unique_together": {("empresa", "codigo")},
            },
        ),
        migrations.CreateModel(
            name="CuentaPresupuestaria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio")),
                ("codigo", models.CharField(max_length=40, verbose_name="Código presupuestario")),
                ("nombre", models.CharField(max_length=200, verbose_name="Nombre")),
                ("tipo", models.CharField(choices=[("INGRESO", "Ingreso"), ("EGRESO", "Egreso")], max_length=10, verbose_name="Tipo")),
                ("rubro_tributario", models.CharField(blank=True, max_length=20, null=True, verbose_name="Rubro tributario")),
                ("cuenta_contable", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="cuentas_presupuestarias", to="contabilidad.cuentacontable", verbose_name="Cuenta contable")),
            ],
            options={
                "db_table": "presu_cuenta_presup",
                "verbose_name": "Cuenta Presupuestaria",
                "verbose_name_plural": "Cuentas Presupuestarias",
                "ordering": ["codigo"],
                "unique_together": {("empresa", "codigo")},
            },
        ),
        migrations.CreateModel(
            name="OrdenPago",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio")),
                ("numero", models.CharField(max_length=30, verbose_name="Número")),
                ("fecha", models.DateField(verbose_name="Fecha")),
                ("favorecido", models.CharField(max_length=200, verbose_name="Favorecido")),
                ("concepto", models.TextField(verbose_name="Concepto")),
                ("estado", models.CharField(choices=[("BORRADOR", "Borrador"), ("APROBADA", "Aprobada"), ("PAGADA", "Pagada"), ("ANULADA", "Anulada")], default="BORRADOR", max_length=10)),
                ("total", models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ("ejercicio", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="ordenes_pago", to="contabilidad.ejerciciofiscal")),
            ],
            options={
                "db_table": "presu_orden_pago",
                "verbose_name": "Orden de Pago",
                "verbose_name_plural": "Órdenes de Pago",
                "ordering": ["-fecha", "-numero"],
                "unique_together": {("empresa", "numero")},
            },
        ),
        migrations.CreateModel(
            name="ProyectoInversion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio")),
                ("codigo", models.CharField(max_length=20, verbose_name="Código")),
                ("nombre", models.CharField(max_length=200, verbose_name="Nombre del proyecto")),
                ("descripcion", models.TextField(blank=True, null=True, verbose_name="Descripción")),
                ("centro_costo", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="proyectos_presupuesto", to="contabilidad.centrocosto", verbose_name="Centro de gasto (opcional)")),
                ("ejercicio", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="proyectos_inversion", to="contabilidad.ejerciciofiscal", verbose_name="Ejercicio fiscal")),
            ],
            options={
                "db_table": "presu_proyecto_inversion",
                "verbose_name": "Proyecto de Inversión",
                "verbose_name_plural": "Proyectos de Inversión",
                "ordering": ["codigo"],
                "unique_together": {("empresa", "ejercicio", "codigo")},
            },
        ),
        migrations.CreateModel(
            name="OrdenPagoDetalle",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("linea", models.IntegerField(default=1)),
                ("descripcion", models.CharField(blank=True, max_length=300, null=True)),
                ("monto", models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ("cuenta_presupuestaria", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="presupuestos.cuentapresupuestaria")),
                ("fondo", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="presupuestos.fondo")),
                ("orden_pago", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="detalles", to="presupuestos.ordenpago")),
                ("proyecto", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="presupuestos.proyectoinversion")),
            ],
            options={
                "db_table": "presu_orden_pago_det",
                "verbose_name": "Detalle de Orden de Pago",
                "verbose_name_plural": "Detalles de Orden de Pago",
                "ordering": ["orden_pago", "linea"],
                "unique_together": {("orden_pago", "linea")},
            },
        ),
        migrations.CreateModel(
            name="EjecucionPresupuestaria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
                ("empresa", models.CharField(max_length=10, verbose_name="Empresa/Municipio")),
                ("fecha", models.DateField(verbose_name="Fecha")),
                ("periodo", models.IntegerField(default=1, verbose_name="Período")),
                ("origen", models.CharField(choices=[("MANUAL", "Manual"), ("ORDEN_PAGO", "Orden de Pago"), ("CHEQUE", "Cheque"), ("CIERRE_CAJA", "Cierre de Caja")], default="MANUAL", max_length=20)),
                ("referencia", models.CharField(blank=True, max_length=60, null=True)),
                ("monto", models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ("cuenta_presupuestaria", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="presupuestos.cuentapresupuestaria")),
                ("ejercicio", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="ejecuciones_presup", to="contabilidad.ejerciciofiscal")),
                ("fondo", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="presupuestos.fondo")),
                ("proyecto", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="presupuestos.proyectoinversion")),
            ],
            options={
                "db_table": "presu_ejecucion",
                "verbose_name": "Ejecución Presupuestaria",
                "verbose_name_plural": "Ejecuciones Presupuestarias",
                "ordering": ["-fecha", "-id"],
            },
        ),
    ]

