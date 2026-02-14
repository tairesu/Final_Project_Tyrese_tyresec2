from yardsearcher.utils.base import YardSearch
import json


class Pnp(YardSearch):
    """
        Scraper class for Joliet U pull it 
    """
    def __init__(self, query="", params={}):
        super().__init__(query)
        self.base_url = "https://www.picknpull.com/api/vehicle/search"
        self.inventory_headers = ('barCodeNumber','vin','year','make','model','row','largeImage','dateAdded')
        self.base_params = {
            "distance":"10",
            "language":"english",
            "zip":"60501",
            "makeId":"",
            "modelId":"",
            "year":"",
        } if params == {} else params

    def get_api_json(self):
        response = self.session.get(self.base_url, headers=self.base_headers, params=self.base_params, timeout=5)
        response.raise_for_status()
        # Pnp's api returns a list with 1 dictionary
        return response.json()[0]

    def handle_queries(self):
        api_json = self.get_api_json()
        vehicles = api_json.get('vehicles') 
        for vehicle in vehicles:
            super().add_result(self.clean_result(vehicle))

    def clean_result(self, dirty_vehicle)-> dict:
        """
            Strip unnecessary keys from dirty vehicle (dict from api)
        """
        assert dirty_vehicle.keys() >= set(self.inventory_headers)
        return {key:dirty_vehicle[key] for key in self.inventory_headers}

    def results_as_list(self):
        return self.results

if __name__ == "__main__":
    scraper = Pnp()
    scraper.parse_api_json()
    #cProfile.run('scraper.fetch_results("2001-2005 honda civic, 02-05 chevrolet tahoe")')
