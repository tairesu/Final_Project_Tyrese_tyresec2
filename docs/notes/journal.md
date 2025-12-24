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

1. ~~Make `management/commands/refresh_inventories.py`~~
2. ~~Import models & scrapers~~
3. ~~Run each scraper w/ empty query~~
4. Clear models if results
5. ~~Loop through results and insert into Vehicles~~

## Tue Dec 23

Steps 1 & 2 are complete. Step 4 would have been clearing the models but I will be "upserting" the data.
If a vehicle exists in the db with the same identifier & junkyard_id combo, don't create a new record. 

To do so, I had to set constraints on the models.

After that, I saw an opportunity to detect changes in the vehicles from the junkyards. Junkyards scrap vehicles and remove them from their public databases (`results` in `management/commands/refresh_inventories`) 


Here's my attempt: 

```
Vehicle.objects.exclude(~Q(junkyard_id=junkyard_id) & Q(junkyard_identifier__in=scraped_identifiers))
```

This attempt did not work because I did not consider its truth table.

To determine which vehicles are removed I'll use the two premises: 
- P = Vehicle belongs to junkyard that's being scraped
- Q = Vehicle exists in scraped results

My Original Query

P | Q | ~P| (~P & Q) | ~(~P & Q)
T | T | F | F | T
T | F | F | F | T
F | T | T | T | F
F | F | T | F | T

There were alot more truth outcomes than expected. I expect P= T and Q = F to be the only case where a delete is necesary

P | Q | ? | P & ~Q
T | T | do not delete | F
T | F | delete | T
F | T | do not delete | F
F | F | do not delete | F

There you have it folks, a new query: 

```
different_identifiers = Vehicle.objects.filter(Q(junkyard_id=junkyard_id) & ~Q(junkyard_identifier__in=scraped_identifiers) )
```


