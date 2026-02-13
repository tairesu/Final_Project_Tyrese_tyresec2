# Dev Journal



I want to alter the scraping process to reduce the number of requests.  
Instead of sending several requests to junkyards everytime the search button is clicked,  I'll cache the inventory data of each junkyard into a new model from one request.  

## Unreleased:

### Added
*	New API Endpoints for querying inventory data

### Changed

### Depracated 

### Fixed

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

## Thur Dec 25

I succesfully reduced the amount of requests to junkyard websites by creating a Django command (to be run by a scheduler) that caches inventory data into the internal database ( My God was it a challenge )

Of course I saw it through! Now this application can find 1000s of vehicles in less than 0.1 seconds

## Fri Dec 26 

After watching YT Combinator videos w/ my Bro, he volunteered to do a test run of the website as a client / customer. Here are the notes I've gathered: 

- UI unclear (not knowing what to type in main search)
- "Fetch Junkyard Inventories Fast" as a hero header is ambigous  
- donor car concept not clear
- The 'company' name is too... niche. Try Junkyard Car Lookup

**Avatar(s): Mechanical Newbie vs Mechanically Inclined**

First Set of Feedback: 

- 'Assumes map shows results of places matching search query (bc of markers)'
- 'FALSE HOPE WHEN 0 RESULTS. All these fancy feats and sh*t w/ 0 results'
- 'Generations would be cool or automatically giving similar cars automatically?'
- 'Cool, "this 0.0129 secs" is useless to the client'



!!!!!!!2012 toyota corolla test case didn't work !!!!!!!!!!

- 'why show row and space?' 
(*after searching 'honda civic'*)
- Lots of civics i understand but ..... 

	- 'Why spaces in 0' 
	- 'AvailableDate?? 
	- 2025-11-10 ?????????? '

- 'Whats the address of the junkyards?' 

- 'Cool if I could see the address or get direction in my maps'

These notes were the reason I:
- removed the useless sidebar & filter junkyards buttons(for MVP)
- altered the hero text to set the tone. 
- created a dynamic placeholder for main input box to show examples of valid queries 
