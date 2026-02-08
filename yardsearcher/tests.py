from django.test import TestCase
from yardsearcher.utils.queries import *


# Create your tests here.
class checkQueries(TestCase):
    def setUp(self):
        pass
    
    def runtest(self, test_queries, function)-> None:
        for (test_query, expected) in test_queries:
            msg = f"\nTest failed @ {test_query}. Expected {expected}\n"
            if type(expected) == AssertionError:
                with self.assertRaises(AssertionError):
                    function(test_query)
            else:
                self.assertEqual(function(test_query), expected, msg=msg)
            
    def test_is_year_present(self):
        function = is_year_present
        test_queries = [
            ("2005-2010 Honda", False),
            ("05 honda civic", True),
            ("civic", False),
            ("05 civic", True),
            ("2005 civic", True),
            ("civic 2005", True),
            ("honda civic 05", True),
            ("honda 05 civic", True),
            ("honda 2005-2010 civic", False),
            ("mazda 3", False),
            ("mazda mazda3", False),
            ("ford f-150", False),
            ("mazda cx-7 2005", True),
            ("2010 xc70", True),
            ("infiniti g35", False),
            ("g35 infiniti", False),
            ("bmw 328xi", False),
        ]
        self.runtest(test_queries,function)
        
            
    def test_is_year_range_present(self):
        function = is_year_range_present
        test_queries = [
            ("2005-2010 Honda", True),
            ("05 honda civic", False),
            ("civic", False),
            ("05 civic", False),
            ("2005 civic", False),
            ("civic 2005", False),
            ("honda civic 05-08", True),
            ("honda 05 civic", False),
            ("honda 2005-2010 civic", True),
            ("mazda 3", False),
            ("mazda mazda3", False),
            ("ford f-150", False),
            ("mazda cx-7 2005", False),
            ("2010 xc70", False),
            ("infiniti g35 2000-2006", True),
            ("g35 infiniti", False),
            ("bmw 328xi", False),
        ]
        self.runtest(test_queries,function)
    
    def test_parse_year(self):
        function = parse_car_year
        self.runtest(
            [
                ("2005-2010 Honda",AssertionError()),
                ("05 honda civic", "2005"),
                ("05 honda civic", "2005"),
                ("civic",AssertionError()),
                ("05 civic", "2005"),
                ("2005 civic", "2005"),
                ("civic 2005", "2005"),
                ("honda civic 05-08",AssertionError()),
                ("honda 05 civic", "2005"),
                ("honda 2005-2010 civic",AssertionError()),
                ("mazda 3",AssertionError()),
                ("mazda mazda3",AssertionError()),
                ("ford f-150",AssertionError()),
                ("mazda cx-7 2005", "2005"),
                ("2010 xc70", "2010"),
                ("infiniti g35 2000-2006",AssertionError()),
                ("g35 infiniti",AssertionError()),
                ("bmw 328xi",AssertionError()),
            ], function)