# Dev Journal
## 2/14/26

### Objective
*   Enable sorting inventory data by columns (Year, make, date, etc). 

### Building the Internal API to sort inentory tables

I do not want a refresh to occur because it may disrupt the user's experience. For this reason, JS will be used to dynamically *sort* a table( of choice ) by a column (of set{'year','make','model','entryDate','row'}) 

I'll use JS to fetch data from an internal API and repopulate the DOM instead of undergoing extensive JS work to search the DOM, capture the values, sort the values, and so on.

The former would require:

1. creating a JSONResponse view of results (w/ support for q, yardId, sortBy, orderBy params )
2. introducing JS function that gets triggered by clicking any `<th>` element. It will:
    - make a call to the internal API (**will need q, yardId, sortBy, order params**)
    - (if status ok & results exists) 
        - remove children of clicked **table.tbody**
        - map results list to table row elements 
        - append those table row nodes to clicked table.tbody
        - toggle icon


#### Keep in mind

*   Not all `<th>` elements will be sortable. 
*   `<Vehicle>` instances may have blank or default values for certain fields

#### Creating the JSONResponse View

The 4 parameters must be present for the SortTable API to work (for now). I use assert statements behind a try block and handle assertione errors if the parameters are invalid. 
With the parameters, I construct a query for the database like the one in `results_view`, The difference here is that I add onto that query to filter cars by `junkyard_id`. 

I filter the db with this newly prepped query, then sort the returned data using Django's built-in `order_by` method.  The last two parameters (order & sortBy ) will be combined into a sting and passed into order_by. 

With the newly sorted queryset, the last thing to do is format this. Here I turn the Vehicle instances into a dict for JSON to serialize (Can't serialize querysets). 

##### Expected JSON Output (Bare minimum for sort table feature)
```
{
    "query": "00-07 civic",
    "sortBy": "entryDate",
    "order": "",
    "yardId": 17,
    num_vehicles: 32,
    "vehicles": [
        {
            "year": "2007",
            "make": "Honda",
            "model": "Civic",
            "vin": "",
            "photo": "",
            "space": "",
            "entryDate": "3 months ago",
            "row":75,
        }, ...{},
    ],
}
```
#### 


## 2/13/26


Day 2 of adding Pick n Pull Summit to Scraphounds. Thankful for their api

v1.0.2 is configured to scrape data from a url when the refresh_inventories command is run. The command is not used to having JSON handed to it so easily.

Typically, a scraper subclass's `inventory_headers` tuple is set after extracting the text from the appropriate \<th> tags...  With Pnp's API, there's no need to scrape anything! 

I can manually set the `Pnp().inventory_headers` to these keys from the api:
*   barCodeNumber (unique identifier)
*   vin
*  year
*   make
*   model
*   largeImage (in case Scraphounds support vehicle images in the future)
*   dateAdded
 
 Now I can easily clean the vehicle dictionaries (that come back from this API) by extracting **ONLY** the key value pairs with keys that exist in `inventory_headers`

 Unlike other junkyard specific scraper classes, this scraper class doesn't need to use `Yardsearch.results_as_list()` the same. When the vehicle dictionaries are cleaned, they are immediately appended to the `results` attribute. 

 In `yardsearcher.utils.known_yards` I'll manually fill in details like class to use, lat, long, and request params to register Pick n Pull Summit to Scraphounds. 

 I suspect this class's `handle_queries` method to fail when called in `yardsearcher.management.commands.refresh_inventories` because there are no *queries* to pass as a parameter. (Older versions used to pass queries to return matching vehicles from websites ). To prevent this, I will override the parent `handle_queries` method to: 
 1. Fetch all inventory results 
 2. Format each result (removing irrelevant keys from API dictionary)
 3. Append to `results` attribute

 The final step is testing the `refesh_inventory` command & adjusting `yardsearcher.utils.extractors` to account for the different key names that Pick n Pull use ( Pnp uses "dateAdded" for dates; LKQ uses "date available" for dates)

## 2/12/26

I'll be adding Pick n Pull Summit to Scraphounds. ~~I originally intented to scrape their inventory data~~, then  I found their internal api that just returns it

|Properties | Values|
|:------|:------|
|~~Inventory URL~~| ~~https://www.picknpull.com/check-inventory/vehicle-search?distance=10&zip=60501~~|
|API URL| https://www.picknpull.com/api/vehicle/search?&makeId=&modelId=&year=&distance=10&zip=60501&language=english |
|Inventory Table| \<table _ngcontent-gog-c26="" class="table pnpDataTable table-striped table-hover"> |
|Inventory Tablerows  | table.pnpDataTable tbody tr |
|Inventory Tabledata  | table.pnpDataTable tbody tr td.hidden-xs|
|Results headers  | table.pnpDataTable thead tr |


#### Snippet of DOM:
<table>
<thead _ngcontent-gog-c26="" class="hidden-xs"><tr _ngcontent-gog-c26=""><th _ngcontent-gog-c26="" data-field="ThumbNail" class="photo-column hidden-xs"><div _ngcontent-gog-c26="" class="th-inner">Photo</div><div _ngcontent-gog-c26="" class="fht-cell"></div></th><th _ngcontent-gog-c26="" data-field="Year" class="hidden-xs vehicle-year"><div _ngcontent-gog-c26="" class="th-inner sortable both">Year</div><div _ngcontent-gog-c26="" class="fht-cell"></div></th><th _ngcontent-gog-c26="" data-field="Make" class="hidden-xs"><div _ngcontent-gog-c26="" class="th-inner">Make</div><div _ngcontent-gog-c26="" class="fht-cell"></div></th><th _ngcontent-gog-c26="" data-field="Model" class="hidden-xs"><div _ngcontent-gog-c26="" class="th-inner">Model</div><div _ngcontent-gog-c26="" class="fht-cell"></div></th><th _ngcontent-gog-c26="" data-field="Row" class="hidden-xs"><div _ngcontent-gog-c26="" class="th-inner sortable both">Row</div><div _ngcontent-gog-c26="" class="fht-cell"></div></th><th _ngcontent-gog-c26="" data-field="DateAdded" class="hidden-xs set-date"><div _ngcontent-gog-c26="" class="th-inner sortable both">Set Date</div><div _ngcontent-gog-c26="" class="fht-cell"></div></th></tr></thead>
<tr _ngcontent-gog-c26="" data-index="0"><td _ngcontent-gog-c26="" class="photo-column">
<img _ngcontent-gog-c26="" src="https://cdn.row52.com/images/e7af07b7-119d-443a-95c6-715aa49343fb.JPG" alt="1988 Oldsmobile Ninety Eight"></td><!----><!----><td _ngcontent-gog-c26="" class="hidden-xs vehicle-year">1988</td><td _ngcontent-gog-c26="" class="hidden-xs">Oldsmobile</td><td _ngcontent-gog-c26="" class="hidden-xs">Ninety Eight</td><td _ngcontent-gog-c26="" class="hidden-xs">15</td><td _ngcontent-gog-c26="" class="hidden-xs set-date">02/06/2026</td><td _ngcontent-gog-c26="" class="visible-xs" style="text-decoration:line-through;position:absolute"><div _ngcontent-gog-c26="" class="compactTitle" >1988 Oldsmobile Ninety Eight</div><div _ngcontent-gog-c26="">Row 15</div><div _ngcontent-gog-c26="">Set: 02/06/2026</div></td></tr>
</table>

```
<!--Snippet Code-->

<tr _ngcontent-gog-c26="" data-index="0">
    <td _ngcontent-gog-c26="" class="photo-column">
        <img _ngcontent-gog-c26="" src="https://cdn.row52.com/images/e7af07b7-119d-443a-95c6-715aa49343fb.JPG" alt="1988 Oldsmobile Ninety Eight">
    </td>
    <!---->
    <!---->
    <td _ngcontent-gog-c26="" class="hidden-xs vehicle-year">
        1988
    </td>
    <td _ngcontent-gog-c26="" class="hidden-xs">
        Oldsmobile
    </td>
    <td _ngcontent-gog-c26="" class="hidden-xs">
        Ninety Eight
    </td>
    <td _ngcontent-gog-c26="" class="hidden-xs">
        15
    </td>
    <td _ngcontent-gog-c26="" class="hidden-xs set-date">
        02/06/2026
    </td>

    <!-- Will not be needing td.visible-xs -->
    <td _ngcontent-gog-c26="" class="visible-xs">
        <div _ngcontent-gog-c26="" class="compactTitle">
            1988 Oldsmobile Ninety Eight
        </div>
        <div _ngcontent-gog-c26="">
            Row 15
        </div>
        <div _ngcontent-gog-c26="">
            Set: 02/06/2026
        </div>
    </td>
</tr>
```

#### Key Observations:
*   Table data has no identifying attributes (id, name, etc)
*   Not all vehicles have thumbnails
*   I don't need the td element with the `td.visible-xs` class.

## ??? 

I want to alter the scraping process to reduce the number of requests.  
Instead of sending several requests to junkyards everytime the search button is clicked,  I'll cache the inventory data of each junkyard into a new model from one request.  


1) ~~Building a `Vehicles` Model to store vehicle data from every junkyard~~ . 
2) Altering base scraper class to insert results into that model 
3) Building a JSONResponse view (currently @ */api/search/<str:query>* url pattern )
4) Altering `results_view`'s to fetch and handle that JSON  

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

## Thur Dec 25

I succesfully reduced the amount of requests to junkyard websites by creating a Django command (to be run by a scheduler) that caches inventory data into the internal database ( My God was it a challenge )

Of course I saw it through! Now this application can find 1000s of vehicles in less than 0.1 seconds


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

## Mon Dec 22

I'm taking on the task `2)Altering the base scraper class`. My plan of attack is to build a script that'll be scheduled to execute @ 2:30 am on my buddy's server. 

Let's test some things

1. ~~Make `management/commands/refresh_inventories.py`~~
2. ~~Import models & scrapers~~
3. ~~Run each scraper w/ empty query~~
4. Clear models if results
5. ~~Loop through results and insert into Vehicles~~

## Sat Dec 20 

- geocode 2.4.1 installed

I'm giving the yard models a magic method that returns a tuple of latitude and longitude decimal values. The goal is to make these values accessible in the templates and views. [This](https://geopy.readthedocs.io/en/stable/#nominatim) is the official geopy documentation

The `results_view` starts the multi-scraping process, and compiles the results into a list of dictionaries named `fetched_yard_data`. Then the **results template** loops through that list, adding markers (w/ tooltips) to the Leafly JS map. 

**Implementing geopy would require that I set JS level variables to the returned tuple before adding the markers.** 
