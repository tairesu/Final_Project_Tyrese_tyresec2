from yardsearcher.utils.base import YardSearch
    
class LKQSearch(YardSearch):
    """
    Represents a search on the LKQ junkyard data
    
    Attributes:
        query (str): The raw search query in string form.
        results (list): Holds the inventory data.
        yard_info (dict): Metadata about the yard itself.
        base_url (str): URL holding the inventory data.
        headers (dict): Content headers for web scraping.
        params (dict):  URL parameters for requesting site data  
    """
    
    def __init__(self, query):
        """
        Initializes search instance
        
        Args: 
            querys (str): The raw search query 
        """
        super().__init__(query)
        selfname = "LKQ Blue Island"
        self.base_url = "https://www.lkqpickyourpart.com/DesktopModules/pyp_vehicleInventory/getVehicleInventory.aspx"
        self.base_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Referer": "https://www.lkqpickyourpart.com/inventory/blue-island-1582/",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9"
        }
        self.base_params = {}

    def fetch_inventory(self, store_id=1582, conditionals={}):
        page_number = 1
        #While valid page exists 
        while(self.is_page_valid(page_number, store_id, conditionals)):
            page_number += 1
        return self.results


    def is_page_valid(self, page_number,store_id, conditionals={}) -> bool:
        # Grabs all divs HTML 
        vehicle_cards = self.fetch_inventory_html(page_number, query, store_id, conditionals)
        return len(vehicle_cards) > 0


    def fetch_inventory_html(self, page_number,query,store_id, conditionals={}) -> list:
        self.params = {
            "page": page_number,
            "filter": query,
            "store": store_id
        }
        response = requests.get(self.base_url, headers=self.headers, params=self.params)
        soup = BeautifulSoup(response.text, "html.parser")
        vehicle_cards = soup.find_all(class_="pypvi_resultRow")
        if len(vehicle_cards) > 1:
            self.handle_vehicle_cards_html(vehicle_cards, conditionals)
        return vehicle_cards


    def handle_vehicle_cards_html(self, vehicle_cards=[], conditionals={}):
        for card in vehicle_cards:
            vehicle_data = self.extract_card_html(card)
            if self.satisfies_conditionals(vehicle_data, conditionals):
                self.results.append(vehicle_data)


    # Turns matching vehicle card HTML and formats the content into a dictionary
    def extract_card_html(self,card_html) -> dict:
        inventory_car = {}
        year_make_model = card_html.find(class_="pypvi_ymm").get_text(' ', strip=True)
        inventory_car['year'] = year_make_model.split(' ')[0]
        inventory_car['make'] = year_make_model.split(' ')[1]
        inventory_car['model'] = year_make_model.split(' ')[2]
        details = card_html.find_all(class_="pypvi_detailItem")
        #loop through each detail item (color, stock, available inventory_car, etc)
        for detail in details:
            items = detail.find_all('b')
            if len(items) > 1:
                for item in items:
                    field_name = item.get_text(strip=True).replace(':','').lower().strip()
                    inventory_car[field_name] = item.next_sibling.strip()
            elif len(items) == 1:
                field_name = items[0].get_text().replace(':','').lower().strip()
                item_value = items[0].next_sibling.strip()
                if('available' in field_name):
                    item_value = detail.find('time').get_text()
                inventory_car[field_name] = item_value
        return inventory_car


    def display_data(self):
        if len(self.results) == 0:
            return ''

        print('\n')
        print('|',self.yard_info['name'])
        print('\n')
        print('Year, Make, Model, Row, Space, Color, VIN, Stock#, EntryDate')
        for result in self.results:
            print(f"{result['year']}, {result['make']}, {result['model']}, {result['row']}, {result['space']}, {result['color']},{result['vin']}, {result['stock #']}, {result['available']}")
    

# Example usage:
if __name__ == '__main__':
    stop = False
    while(stop != True):
        query = input('\nEnter year, make, model: ')
        if query.strip().lower() in ['stop','halt','exit']:
            stop = True

        yardSearch = LKQSearch(query)
        yardSearch.display_data()


