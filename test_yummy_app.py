import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service


# CAP DO 1: Bo test co ban
class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang co ban tinh tien don hang"""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


# CAP DO 2: Test apply_promo_code
class TestMediumLevel(unittest.TestCase):
    def test_promo_online_hop_le(self):
        app = YummyApp("online", 15)
        self.assertAlmostEqual(app.apply_promo_code(100000, "GIAM10"), 90000)

    def test_promo_offline(self):
        app = YummyApp("offline", 15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_promo_dac_biet_os15(self):
        app = YummyApp("online", 15)
        self.assertAlmostEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000)

    def test_promo_dac_biet_os14(self):
        app = YummyApp("online", 14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")


# CAP DO 3: Test get_nearby_restaurants (mock GPS)
class TestHardLevel(unittest.TestCase):
    def setUp(self):
        self.app = YummyApp()

    @patch('yummy_app.gps_service.get_current_location')
    def test_gps_trong_vung(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)
        self.assertEqual(len(self.app.get_nearby_restaurants()), 2)

    @patch('yummy_app.gps_service.get_current_location')
    def test_gps_ngoai_vung(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)
        self.assertEqual(self.app.get_nearby_restaurants(), [])

    @patch('yummy_app.gps_service.get_current_location')
    def test_gps_mat_tin_hieu(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError
        self.assertEqual(self.app.get_nearby_restaurants(),
                         "Khong the xac dinh vi tri.")


if __name__ == '__main__':
    unittest.main()
