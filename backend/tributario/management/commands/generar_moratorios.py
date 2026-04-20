from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models


class Command(BaseCommand):
    help = (
        "Genera recargos e intereses moratorios de forma masiva por empresa.\n"
        "Pensado para ejecutarse como tarea programada:\n"
        "- BI: día 1 de cada mes\n"
        "- ICS: día 11 de cada mes\n"
        "Soporta --dry-run para validar sin afectar datos."
    )

    def add_arguments(self, parser):
        parser.add_argument("--empresa", default="ALL", help="Código de empresa (municipio) o ALL")
        parser.add_argument("--modulo", default="AMBOS", choices=["BI", "ICS", "AMBOS"], help="Qué módulo procesar")
        parser.add_argument("--fecha", default="", help="Fecha de ejecución (YYYY-MM-DD). Default: hoy.")
        parser.add_argument("--dry-run", action="store_true", help="No inserta, solo calcula")

    def handle(self, *args, **options):
        from core.models import Municipio
        from tributario.models import (
            RubroMoratorioConfig,
            TransaccionesBienesInmuebles,
            TransaccionesIcs,
        )

        empresa_opt = (options["empresa"] or "ALL").strip().upper()
        modulo = options["modulo"]
        dry_run = bool(options["dry_run"])
        fecha_opt = (options["fecha"] or "").strip()

        hoy = date.today()
        if fecha_opt:
            try:
                hoy = datetime.strptime(fecha_opt, "%Y-%m-%d").date()
            except Exception:
                raise SystemExit("Fecha inválida. Use formato YYYY-MM-DD.")

        if empresa_opt == "ALL":
            empresas = list(Municipio.objects.values_list("codigo", flat=True))
        else:
            empresas = [empresa_opt]

        self.stdout.write(self.style.WARNING(f"generar_moratorios fecha={hoy} modulo={modulo} empresas={len(empresas)} dry_run={dry_run}"))

        total_generados = 0
        total_empresas = 0

        for empresa in empresas:
            configs = RubroMoratorioConfig.objects.filter(empresa=empresa, activo=True)
            if modulo != "AMBOS":
                configs = configs.filter(aplica_modulo__in=[modulo, "AMBOS"])

            if not configs.exists():
                continue

            total_empresas += 1

            # Nota: este comando deja lista la alternativa "SIMAFI normal" para automatizar.
            # Para BI se puede usar `vencimiento` de `TransaccionesBienesInmuebles`.
            # Para ICS se usa `vencimiento` de `TransaccionesIcs`.
            #
            # Implementación BI (mínima y segura):
            if modulo in ("BI", "AMBOS"):
                total_generados += self._procesar_bi(
                    empresa=empresa,
                    hoy=hoy,
                    configs=list(configs.filter(aplica_modulo__in=["BI", "AMBOS"])),
                    TransaccionesBienesInmuebles=TransaccionesBienesInmuebles,
                    dry_run=dry_run,
                )

            if modulo in ("ICS", "AMBOS"):
                total_generados += self._procesar_ics(
                    empresa=empresa,
                    hoy=hoy,
                    configs=list(configs.filter(aplica_modulo__in=["ICS", "AMBOS"])),
                    TransaccionesIcs=TransaccionesIcs,
                    dry_run=dry_run,
                )

        self.stdout.write(self.style.SUCCESS(f"Empresas procesadas={total_empresas}. Registros generados (BI)={total_generados}"))

    def _procesar_bi(self, *, empresa: str, hoy: date, configs, TransaccionesBienesInmuebles, dry_run: bool) -> int:
        """
        Generación mínima para BI:
        - Para cada config (rubro moratorio -> rubro padre) busca cargos vencidos del rubro padre.
        - Inserta un cargo mensual en el rubro moratorio (operacion='D') para el mes/año actual.

        Nota: Para mantener idempotencia, evita duplicar por (empresa, cocata1, ano, mes, rubro).
        """
        generados = 0

        # Ejecutar solo el día 1 por defecto (alineado a requerimiento); si se corre manualmente,
        # igual operará sobre el mes/año de la fecha indicada.
        ano = hoy.year
        mes = hoy.month

        for cfg in configs:
            rubro_padre = (cfg.rubro_padre_codigo or "").strip().upper()
            rubro_mora = (cfg.rubro_codigo or "").strip().upper()

            if not rubro_padre or not rubro_mora:
                continue

            # Cargos vencidos del rubro padre
            vencidos = TransaccionesBienesInmuebles.objects.filter(
                empresa=empresa,
                rubro=rubro_padre,
                estado="A",
            ).exclude(vencimiento__isnull=True).filter(vencimiento__lt=hoy)

            # Para cada predio (cocata1) generar 1 cargo mensual moratorio si no existe
            for row in vencidos.values("cocata1").distinct():
                cocata1 = row["cocata1"]

                existe = TransaccionesBienesInmuebles.objects.filter(
                    empresa=empresa,
                    cocata1=cocata1,
                    ano=ano,
                    mes=mes,
                    rubro=rubro_mora,
                ).exists()
                if existe:
                    continue

                # Base: suma de cargos del rubro padre vencidos para ese predio
                base = (
                    TransaccionesBienesInmuebles.objects.filter(
                        empresa=empresa,
                        cocata1=cocata1,
                        rubro=rubro_padre,
                        estado="A",
                    )
                    .exclude(vencimiento__isnull=True)
                    .filter(vencimiento__lt=hoy)
                    .aggregate(total=models.Sum("monto"))
                    .get("total")
                    or Decimal("0.00")
                )

                tasa = Decimal(str(cfg.tasa_recargo_mensual or "0"))
                monto = (base * (tasa / Decimal("100"))).quantize(Decimal("0.01"))
                if monto <= 0:
                    continue

                if dry_run:
                    generados += 1
                    continue

                with transaction.atomic():
                    TransaccionesBienesInmuebles.objects.create(
                        empresa=empresa,
                        cocata1=cocata1,
                        rubro=rubro_mora,
                        ano=ano,
                        mes=mes,
                        operacion="D",
                        monto=monto,
                        fecha=hoy,
                        vencimiento=hoy,  # cargo del mes
                        usuario="SISTEMA",
                        estado="A",
                    )
                    generados += 1

        return generados

    def _procesar_ics(self, *, empresa: str, hoy: date, configs, TransaccionesIcs, dry_run: bool) -> int:
        """
        Generación mínima para ICS:
        - Para cada config (rubro moratorio -> rubro padre) busca cargos vencidos del rubro padre.
        - Inserta 1 cargo mensual en el rubro moratorio (operacion='D') por negocio (rtm/expe) para el mes/año actual.

        Idempotencia: evita duplicar por (empresa, rtm, expe, ano, mes, rubro).
        """
        generados = 0
        ano = hoy.year
        mes = str(hoy.month).zfill(2)

        for cfg in configs:
            rubro_padre = (cfg.rubro_padre_codigo or "").strip().upper()
            rubro_mora = (cfg.rubro_codigo or "").strip().upper()
            if not rubro_padre or not rubro_mora:
                continue

            vencidos = TransaccionesIcs.objects.filter(
                empresa=empresa,
                rubro=rubro_padre,
            ).exclude(vencimiento__isnull=True).filter(vencimiento__lt=hoy).exclude(operacion='F')

            for row in vencidos.values("rtm", "expe").distinct():
                rtm = row["rtm"]
                expe = row["expe"]

                existe = TransaccionesIcs.objects.filter(
                    empresa=empresa,
                    rtm=rtm,
                    expe=expe,
                    ano=ano,
                    mes=mes,
                    rubro=rubro_mora,
                ).exists()
                if existe:
                    continue

                base = (
                    TransaccionesIcs.objects.filter(
                        empresa=empresa,
                        rtm=rtm,
                        expe=expe,
                        rubro=rubro_padre,
                    )
                    .exclude(vencimiento__isnull=True)
                    .filter(vencimiento__lt=hoy)
                    .aggregate(total=models.Sum("monto"))
                    .get("total")
                    or Decimal("0.00")
                )

                tasa = Decimal(str(cfg.tasa_recargo_mensual or "0"))
                monto = (base * (tasa / Decimal("100"))).quantize(Decimal("0.01"))
                if monto <= 0:
                    continue

                if dry_run:
                    generados += 1
                    continue

                with transaction.atomic():
                    TransaccionesIcs.objects.create(
                        idneg=0,
                        nodeclara="",
                        empresa=empresa,
                        rtm=rtm,
                        expe=expe,
                        ano=ano,
                        mes=mes,
                        operacion="D",
                        rubro=rubro_mora,
                        fecha=hoy,
                        vencimiento=hoy,
                        monto=monto,
                        tasa=Decimal("0.00"),
                        usuario="SISTEMA",
                        fechasys=datetime.now(),
                    )
                    generados += 1

        return generados

