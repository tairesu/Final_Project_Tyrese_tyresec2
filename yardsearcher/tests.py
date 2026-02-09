from django.test import TestCase
from yardsearcher.utils.queries import *


class checkQueries(TestCase):
    def setUp(self):
        pass

    def runtest(self, test_queries, function) -> None:
        for test in test_queries:
            test_query = test["query"]
            expected = test["expected"]
            msg = f"\nTest failed @ {test_query}. Expected {expected}\n"
            # Use the proper assets based on *expected *
            if isinstance(expected, AssertionError):
                with self.assertRaises(AssertionError):
                    function(test_query)
            elif isinstance(expected, tuple):
                self.assertTupleEqual(function(test_query), expected, msg=msg)
            elif isinstance(expected, dict):
                self.assertDictContainsSubset(dictionary=function(test_query), subset=expected, msg=msg)
            else:
                self.assertEqual(function(test_query), expected, msg=msg)

    def test_is_year_present(self):
        function = is_year_present
        test_queries = [
            {"query": "2005-2010 Honda", "expected": False},
            {"query": "05 honda civic", "expected": True},
            {"query": "civic", "expected": False},
            {"query": "05 civic", "expected": True},
            {"query": "2005 civic", "expected": True},
            {"query": "civic 2005", "expected": True},
            {"query": "honda civic 05", "expected": True},
            {"query": "honda 05 civic", "expected": True},
            {"query": "honda 2005-2010 civic", "expected": False},
            {"query": "mazda 3", "expected": False},
            {"query": "mazda mazda3", "expected": False},
            {"query": "ford f-150", "expected": False},
            {"query": "mazda cx-7 2005", "expected": True},
            {"query": "2010 xc70", "expected": True},
            {"query": "infiniti g35", "expected": False},
            {"query": "g35 infiniti", "expected": False},
            {"query": "bmw 328xi", "expected": False},
        ]
        self.runtest(test_queries, function)

    def test_is_year_range_present(self):
        function = is_year_range_present
        test_queries = [
            {"query": "2005-2010 Honda", "expected": True},
            {"query": "05 honda civic", "expected": False},
            {"query": "civic", "expected": False},
            {"query": "05 civic", "expected": False},
            {"query": "2005 civic", "expected": False},
            {"query": "civic 2005", "expected": False},
            {"query": "honda civic 05-08", "expected": True},
            {"query": "honda 05 civic", "expected": False},
            {"query": "honda 2005-2010 civic", "expected": True},
            {"query": "2005-2010", "expected": True},
            {"query": "mazda 3", "expected": False},
            {"query": "mazda mazda3", "expected": False},
            {"query": "ford f-150", "expected": False},
            {"query": "mazda cx-7 2005", "expected": False},
            {"query": "2010 xc70", "expected": False},
            {"query": "infiniti g35 2000-2006", "expected": True},
            {"query": "g35 infiniti", "expected": False},
            {"query": "bmw 328xi", "expected": False},
        ]
        self.runtest(test_queries, function)

    def test_parse_year(self):
        function = parse_car_year
        test_queries = [
            {"query": "2005-2010 Honda", "expected": AssertionError()},
            {"query": "05 honda civic", "expected": "2005"},
            {"query": "98 honda civic", "expected": "1998"},
            {"query": "00 honda civic", "expected": "2000"},
            {"query": "82 honda civic", "expected": "1982"},
            {"query": "99 honda civic", "expected": "1999"},
            {"query": "25 honda civic", "expected": "2025"},
            {"query": "26 honda civic", "expected": "2026"},
            {"query": "27 honda civic", "expected": "1927"},
            {"query": "62 honda civic", "expected": "1962"},
            {"query": "civic", "expected": AssertionError()},
            {"query": "05 civic", "expected": "2005"},
            {"query": "2005 civic", "expected": "2005"},
            {"query": "civic 2005", "expected": "2005"},
            {"query": "honda civic 05-08", "expected": AssertionError()},
            {"query": "honda 05 civic", "expected": "2005"},
            {"query": "honda 2005-2010 civic", "expected": AssertionError()},
            {"query": "mazda 3", "expected": AssertionError()},
            {"query": "mazda mazda3", "expected": AssertionError()},
            {"query": "ford f-150", "expected": AssertionError()},
            {"query": "mazda cx-7 2005", "expected": "2005"},
            {"query": "2010 xc70", "expected": "2010"},
            {"query": "infiniti g35 2000-2006", "expected": AssertionError()},
            {"query": "g35 infiniti", "expected": AssertionError()},
            {"query": "bmw 328xi", "expected": AssertionError()},
        ]
        self.runtest(test_queries, function)

    def test_parse_year_range(self):
        function = parse_car_year_range
        test_queries = [
            {"query": "2005-2010 Honda", "expected": ("2005", "2010")},
            {"query": "honda civic 05-08", "expected": ("2005", "2008")},
            {"query": "honda 2005-2010 civic", "expected": ("2005", "2010")},
            {"query": "infiniti g35 94-25", "expected": ("1994", "2025")},
            {"query": "infiniti g35 94-26", "expected": ("1994", "2026")},
            {"query": "infiniti g35 2000-2006", "expected": ("2000", "2006")},
            {"query": "05 honda civic", "expected": AssertionError()},
            {"query": "civic", "expected": AssertionError()},
            {"query": "2005 civic", "expected": AssertionError()},
            {"query": "mazda 3", "expected": AssertionError()},
            {"query": "ford f-150", "expected": AssertionError()},
            {"query": "2010 xc70", "expected": AssertionError()},
        ]
        self.runtest(test_queries, function)

    def test_extract_conditionals(self):
        function = extract_conditionals
        test_queries = [
            {"query": "2005-2010 Honda", "expected": {"minYear": "2005", "maxYear": "2010", "make": "honda"}},
            {"query": "honda civic 05-08", "expected": {"minYear": "2005", "maxYear": "2008", "make": "honda", "model": "civic"}},
            {"query": "honda 2005-2010 civic", "expected": {"minYear": "2005", "maxYear": "2010", "make": "honda", "model": "civic"}},
            {"query": "infiniti g35 2000-2006", "expected": {"minYear": "2000", "maxYear": "2006", "make": "infiniti", "model": "g35"}},
            {"query": "05 honda civic", "expected": {"year": "2005", "make": "honda", "model": "civic"}},
            {"query": "2005 civic", "expected": {"make": "civic", "year": "2005"}},
            {"query": "mazda 3", "expected": {"make": "mazda", "model": "3"}},
            {"query": "ford f-150", "expected": {"make": "ford", "model": "f-150"}},
            {"query": "2010-2020", "expected": {"minYear": "2010", "maxYear": "2020"}},
            {"query": "2010 xc70", "expected": {"year": "2010", "make": "xc70"}},
            {"query": "chevrolet 90-06 tahoe", "expected": {"minYear": "1990", "maxYear": "2006", "make": "chevrolet", "model": "tahoe"}},
        ]
        self.runtest(test_queries, function)
