from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from catastro.models import BDCata1, TasasMunicipales
from tributario.models import PlanArbitrio, Tarifas


class AjaxCalcularTasasMunicipalesIntegration(TestCase):
    """
    Verifica la automatización de tasas municipales cuando se cambia el número
    de viviendas, cuartos o apartamentos y se requiere usar planarbitio.
    """

    def setUp(self):
        self.client = Client()
        session = self.client.session
        session['catastro_empresa'] = '0301'
        session.save()

        self.clave = 'H0001'
        BDCata1.objects.create(
            empresa='0301',
            cocata1=self.clave,
            bvl2tie=Decimal('0'),
            mejoras=Decimal('0'),
            detalle=Decimal('0'),
            cultivo=Decimal('0'),
            declarado=Decimal('0'),
            vivienda=Decimal('0'),
            cuartos=Decimal('0'),
            apartamentos=Decimal('0'),
        )

        Tarifas.objects.create(
            empresa='0301',
            rubro='T0002',
            cod_tarifa='002',
            ano=Decimal('2026'),
            descripcion='Viviendas 2026',
            valor=Decimal('160'),
            tipo='V',
        )

        PlanArbitrio.objects.create(
            empresa='0301',
            rubro='T0002',
            cod_tarifa='002',
            tipocat='1',
            ano=Decimal('2026'),
            codigo='01',
            minimo=Decimal('0'),
            maximo=Decimal('99999999'),
            valor=Decimal('160'),
        )

        TasasMunicipales.objects.create(
            empresa='0301',
            clave=self.clave,
            rubro='T0002',
            cod_tarifa='002',
            valor=Decimal('0'),
        )

    def test_calcular_tasas_con_dos_viviendas_actualiza_tasas(self):
        response = self.client.get(
            reverse('catastro:ajax_calcular_tasas_municipales'),
            data={
                'empresa': '0301',
                'clave': self.clave,
                'num_viviendas': '2',
                'num_cuartos': '0',
                'num_apartamentos': '0',
                'avaluo_total': '100000',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'), msg=data.get('message'))

        tasa = TasasMunicipales.objects.get(
            empresa='0301',
            clave=self.clave,
            rubro='T0002',
            cod_tarifa='002',
        )
        self.assertEqual(tasa.valor, Decimal('320.00'))
