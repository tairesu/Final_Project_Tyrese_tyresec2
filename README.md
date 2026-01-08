# YardHounds

## Overview

The fragmented nature of junkyards made it difficult to find donor cars. It required browsing the online inventory searching tool, scrolling through the results (some irrelevant), taking personal notes, and repeating for other junkyards or vehicles.
As the family mechanic, and seller of rare/in-demand car parts, I needed to spend more time pulling the parts and not searching for them (especially if the weather didn't permit phone usage).   

So I built a CLI in Python that fetches multiple inventories from one query. The more I used it, the more I wanted to access it through a browser. Once a friend expressed interest as well, I integrated that scraper into this application.
This application combines these fetched online inventories into one inventory.  
 
## Core Features 

- Multi-yard Searching
- Query Formatting (Enables multi-vehicle searches, and conditions to be specified) 

## Tech Stack

- Python (Django): Web Framework; Dynamically renders content to pages; Integrates original scraper;  
- SQLite3: DB
- ~~Bootstrap~~ Tailwind: Good looks/feel (UI); Replicable; 
- Git: Version Control

## Usage 

## Challenges / Tradeoffs

### Model Design

Junkyards do not track the same details for the vehicles in their inventory. A few may include the VINs, colors, or actual images of their vehicles, but most agree that year, make, model, and yard ids are critical details for operation. 

I've decided to build a single MModel that allows those junkyard-specific fields to be blank. I could have built models for each junkyard's inventory, but my approach will make referencing vehicles easier from other models, and support future crowdsourcing efforts at "completing"  inventories.  
