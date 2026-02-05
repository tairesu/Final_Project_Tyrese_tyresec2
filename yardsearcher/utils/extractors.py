def extract_row(self, result):
    """
    Returns the 'Row' value from a junkyard scraper's results attr
    """
    row = 0
    # Junkyards may name the 'row' attrtibute differently
    if 'row' in result.keys() and len(result['row']) > 0:
        row = result['row']  # Pyp
    elif 'vehicle row' in result.keys() and len(result['vehicle row']) > 0:
        row = result['vehicle row'] # Jup
    return int(row)

def extract_junkyard_identifier(self, result):
	junkyard_identifier = ""
	if 'stock#' in result.keys():
		junkyard_identifier = result['stock#']
	elif 'stock #' in result.keys():
		junkyard_identifier = result['stock #']
	return junkyard_identifier

def extract_color(self, result):
	color = ""
	if 'color' in result.keys():
		color = result['color']
	return color

def extract_space(self, result):
	space = 0
	if 'space' in result.keys() and len(result['space']) > 0:
		space = result['space']
	return space

def extract_date(self, result, date_format):
	date = ''
	if 'date set in yard' in result.keys():
		date = result['date set in yard']
	elif 'available' in result.keys():
		date = result['available'] 
	return datetime.strptime(date, date_format)

def extract_vin(self, result):
	vin = ""
	if 'vin' in result.keys():
		vin = result['vin']
	return vin