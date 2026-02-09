import re
import time
import datetime

def get_year_prefix(car_year):
    if len(car_year) == 4:
        return ""
    
    current_year = str(datetime.date.today().year)
    current_prefix = current_year[0:2]
    current_suffix = current_year[2:]
    prior_prefix = str(int(current_prefix) - 1)[0:2]
    return current_prefix if int(car_year) <= int(current_suffix) else prior_prefix 

def get_query_conditionals(query)-> list:
    """
        Extracts conditionals from queries
    """
    return [ extract_conditionals(vehicle_query) for vehicle_query in query.lower().split(",")]

def extract_conditionals(query="") -> dict:
    """
    honda -> make:honda
    honda civic -> make:honda,model:civic
    02 honda -> year:2002, make:honda
    
    """
    query = query.strip()
    conditionals = {'original_query': query}
    semantics = query.lower().split(" ") # Seperates via whitespaces
    
    if is_year_present(query):
        conditionals['year'] = parse_car_year(query)
        year = re.findall("^\d{2}\s|^\d{4}\s|\s\d{2}\s|\s\d{4}\s|\s\d{4}$|\s\d{2}$", query)[0].strip()
        semantics.pop(semantics.index(year))
    elif not is_year_present(query) and is_year_range_present(query):
        conditionals['minYear'], conditionals['maxYear'] = parse_car_year_range(query)
        year_range = re.findall("\d+\-\d+", query)[0]
        semantics.pop(semantics.index(year_range))
    
    # now that there are no more years or year ranges
    if len(semantics) > 1:
        conditionals['make'] = semantics[0]
        semantics.pop(0)
        conditionals['model'] = ' '.join(semantics) # the remaining strings
    elif len(semantics) == 1:
        conditionals['make'] = semantics[0]
        
    return conditionals

def is_year_present(query="") -> bool:
    # Does the query contains patterns '2004 ' or '08 ' 
    return True if re.findall(r"(^\d{2}\s)|(^\d{4}\s)|(\s\d{2}\s)|(\s\d{4}\s)|(\s\d{4}$)|(\s\d{2}$)", query) else False

def is_year_range_present(query="") -> bool:
    # Does the query contains patterns '2004-2012 ' or '02-11'
    return True if re.findall(r"^[0-9]{4}-[0-9]{4}\s|\s[0-9]{4}-[0-9]{4}|^[0-9]{2}-[0-9]{2}\s|\s[0-9]{2}-[0-9]{2}", query) else False

def parse_car_year(query="") -> str:
    """
    Strips a given query str of it's year
    parse_car_year('2004 Honda Civic') => '2004'
    """
    assert is_year_present(query)

    # Find the characters of query matching patterns '02' or '2004'
    car_year = re.findall(r"^\d{2}\s|^\d{4}\s|\s\d{2}\s|\s\d{4}\s|\s\d{4}$|\s\d{2}$", query)[0].strip()

    year_prefix = get_year_prefix(car_year)
    # Place the current year's prefix if car year had 2 characters (e.g: '01'->'2001')  
    return year_prefix + car_year 

def parse_car_year_range(query="") -> tuple:
    """
    Strips a given query str of minimum and maximum years

    parse_car_year_range('2004-2008 Honda Civic') => ('2004','2008')
    """
    assert is_year_range_present(query)
    range_str = re.findall(r"^[0-9]{4}-[0-9]{4}\s|\s[0-9]{4}-[0-9]{4}|^[0-9]{2}-[0-9]{2}\s|\s[0-9]{2}-[0-9]{2}", query.strip())[0]
    min_year = range_str.split('-')[0].strip()
    max_year = range_str.split('-')[1].strip()
    formatted_min_year = "20" + min_year if len(min_year) == 2 else min_year 
    formatted_max_year = "20" + max_year if len(max_year) == 2 else max_year 

    return (formatted_min_year,formatted_max_year)




