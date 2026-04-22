from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from tributario_app.views import diag_bienes_inmuebles


class DiagBienesInmueblesTests(SimpleTestCase):
    @patch("tributario_app.views.connection")
    def test_diag_view_returns_json_without_db(self, mock_connection):
        # Simular cursor/DB sin realmente crear BD de tests (migraciones fallan en Postgres por collation).
        cur = MagicMock()
        cur.fetchone.side_effect = [[None]] * 50
        mock_connection.cursor.return_value.__enter__.return_value = cur

        request = self.client.get("/tributario/__diag/bienes-inmuebles/").wsgi_request
        resp = diag_bienes_inmuebles(request)
        self.assertEqual(resp.status_code, 200)
        payload = resp.json()
        self.assertTrue(payload.get("ok"))
        self.assertIn("catastro_import", payload)
        self.assertIn("db", payload)

