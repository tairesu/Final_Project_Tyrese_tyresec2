from yardsearcher.utils.base import YardSearch


class Jup(YardSearch):
    """
        Scraper class for Joliet U pull it 
    """
    def __init__(self, query_str):
        super().__init__(query_str)
        self.name = "Joliet U-Pull It"
        self.elem_id = "jap"
        self.lat = 41.5225
        self.long = -88.0561
        super().appendLocation()
    
    # Override parent method
    def fetch_inventory(self,conditionals):
        make = conditionals['make'].upper()
        model  = conditionals['model'].upper()
        self.update_headers({"path": f"/inventory/?make={make}&model={model}"})
        # Jup requires make & model params
        super().set_url(f"https://www.jolietupullit.com/inventory/?make={make}&model={model}")
        inventory_html_soup = super().fetch_inventory()
        inventory_table_rows = self.extract_inventory_table_rows(inventory_html_soup)
        # extract vehicle data matching table rows conditionals  
        self.filter_inventory_table_rows(inventory_table_rows, conditionals)

    def extract_inventory_table_rows(self, inventory_soup):
        # Grab Jups inventory table (table#cars-table)
        inventory_table = inventory_soup.find(id="cars-table")
        # If the table doesn't exists
        if not inventory_table or not inventory_table.find(['td']):
            # Let it be known
            print(f"[!] Could not find results for {self.searched_query}")
            return ''

        # If inventory_headers (column names) arent set
        if self.inventory_headers == ():
            # Find all table headers w/i the inventory table 
            th_elems = inventory_table.find_all('th')
            # Extract the text from every table header element into a tuple
            inventory_headers = tuple([th.get_text(strip=True).lower() for th in th_elems])
            # Now set the inventory_headers to this tuple
            self.set_inventory_headers(inventory_headers)

        # Grab the table row elements of the inventory table (ignore the first row)
        inventory_table_rows = inventory_table.find_all('tr')[1:]
        return inventory_table_rows

    def filter_inventory_table_rows(self, inventory_table_rows, conditionals):
        for i, inventory_table_row in enumerate(inventory_table_rows):
            # Find every cell w/in this inventory_table_row
            td_elems = inventory_table_row.find_all('td')
            # Extract the text of each cell into a tuple
            inventory_vehicle = tuple([td.get_text(strip=True).lower() for td in td_elems])
            # If the vehicle tuple satisfies the conditionals 
            if super().satisfies_conditionals(inventory_vehicle, conditionals):
                self.add_result(inventory_vehicle)
