# data_pipeline/tests/plugins/helpers/lib/test_data_processors.py


from unittest import TestCase
from plugins.helpers.lib.data_processors import PortsItemProcessor


class PortsItemProcessorTest(TestCase):
    def setUp(self):
        processor = PortsItemProcessor()
        self.process_item = processor.process_item
        self.process_country_name = processor.process_country_name
        self.process_coordinates = processor.process_coordinates
        self.process_unlocode = processor.process_unlocode
        self.process_port_name = processor.process_port_name

    def test_ports_item_processor_process_item(self):
        """
        Test if process_item returns a transformed dictionary values.
        """
        dirty_data = {
            'coordinates': '\xa0',
            'countryName': '(GT)\xa0\xa0GUATEMALA\xa0\xa0\xa0\xa0',
            'portName': 'Villa Nueva\xa0',
            'unlocode': 'GT\xa0\xa0VIN\xa0'
        }
        expected_data = {
            'coordinates': 'missing_value',
            'countryName': 'Guatemala',
            'portName': 'Villa Nueva',
            'unlocode': 'GT VIN'
        }
        transformed_data = self.process_item(dirty_data)
        self.assertDictEqual(transformed_data, expected_data)

    def test_ports_item_processor_process_coordinates(self):
        """
        Test if process_coordinates returns the expected coordinates format.
        """
        coordinates1 = self.process_coordinates('\n1418N 09155W\xa0')
        coordinates2 = self.process_coordinates('1550N 08845W\xa0\xa0\t')
        self.assertEqual(coordinates1, '1418N 09155W')
        self.assertEqual(coordinates2, '1550N 08845W')

    def test_ports_item_processor_process_coordinates_missing_values(self):
        """
        Test if process_coordinates handles coordinates values correctly.
        """
        missing_value1 = self.process_coordinates('\xa0\xa0\t')
        missing_value2 = self.process_coordinates(None)
        self.assertEqual(missing_value1, 'missing_value')
        self.assertEqual(missing_value2, 'missing_value')

    def test_ports_item_processor_process_country_name(self):
        """
        Test if process_country_name returns the expected country name format.
        """
        country1 = self.process_country_name(
            '\t(GT)\xa0\xa0GUATEMALA\xa0\xa0\xa0\xa0'
        )
        country2 = self.process_country_name(
            '(GT)\xa0\xa0GUATEMALA\xa0\xa0\xa0\xa0\t'
        )
        self.assertEqual(country1, 'Guatemala')
        self.assertEqual(country2, 'Guatemala')

    def test_ports_item_processor_process_country_name_missing_value(self):
        """
        Test if process_country_name handles missing country name correctly.
        """
        missing_value1 = self.process_country_name('\xa0\xa0\xa0\xa0\t')
        missing_value2 = self.process_country_name(None)
        self.assertEqual(missing_value1, 'missing_value')
        self.assertEqual(missing_value2, 'missing_value')

    def test_ports_item_processor_process_port_name(self):
        """
        Test if process_port_name returns the expected port name format.
        """
        port_name1 = self.process_port_name('\tLa Aurora\xa0')
        port_name2 = self.process_port_name('Livingston \xa0\t')
        port_name3 = self.process_port_name('livingston \xa0\t')
        self.assertEqual(port_name1, 'La Aurora')
        self.assertEqual(port_name2, 'Livingston')
        self.assertEqual(port_name3, 'Livingston')

    def test_ports_item_processor_process_port_name_missing_value(self):
        """
        Test if process_port_name handles missing port names correctly.
        """
        missing_value1 = self.process_port_name('\xa0\t')
        missing_value2 = self.process_port_name(None)
        self.assertEqual(missing_value1, 'missing_value')
        self.assertEqual(missing_value2, 'missing_value')

    def test_ports_item_processor_process_unlocode(self):
        """
        Test if process_unlocode returns the expected unlocode format.
        """
        locode1 = self.process_unlocode('GT\xa0\xa0LAA\xa0\t')
        locode2 = self.process_unlocode('\tGT\xa0LIV\xa0')
        locode3 = self.process_unlocode('\tgt\xa0liV\xa0')
        self.assertEqual(locode1, 'GT LAA')
        self.assertEqual(locode2, 'GT LIV')
        self.assertEqual(locode3, 'GT LIV')

    def test_ports_item_processor_process_unlocode_missing_value(self):
        """
        Test if process_unlocode handles missing unlocode correctly.
        """
        missing_value1 = self.process_unlocode('\t\xa0')
        missing_value2 = self.process_unlocode(None)
        self.assertEqual(missing_value1, 'missing_value')
        self.assertEqual(missing_value2, 'missing_value')
