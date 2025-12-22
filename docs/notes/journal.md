## 

I want to alter the scraping process to reduce the number of requests.  
Instead of sending several requests to junkyards everytime the search button is clicked,  I'll cache the inventory data of each junkyard into a new model from one request.  

Next Steps:

1) ~~Building a `Vehicles` Model to store vehicle data from every junkyard~~ . 
2) Altering base scraper class to insert results into that model 
3) Building a JSONResponse view (currently @ */api/search/<str:query>* url pattern )
4) Altering `results_view`'s to fetch and handle that JSON  

## Sat Dec 20 

- geocode 2.4.1 installed

I'm giving the yard models a magic method that returns a tuple of latitude and longitude decimal values. The goal is to make these values accessible in the templates and views. [This](https://geopy.readthedocs.io/en/stable/#nominatim) is the official geopy documentation

The `results_view` starts the multi-scraping process, and compiles the results into a list of dictionaries named `fetched_yard_data`. Then the **results template** loops through that list, adding markers (w/ tooltips) to the Leafly JS map. 

**Implementing geopy would require that I set JS level variables to the returned tuple before adding the markers.** 


## Mon Dec 22

I'm taking on the task `2)Altering the base scraper class`. My plan of attack is to build a script that'll be scheduled to execute @ 2:30 am on my buddy's server. 

Let's test some things

1. Make `management/commands/refresh_inventories.py`
2. Import models & scrapers
3. Run each scraper w/ empty query
4. Clear models if results
5. Loop through results and insert into Vehicles 


