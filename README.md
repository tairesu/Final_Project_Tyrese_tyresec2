# YardHounds

## Overview

## Core Features 

## Tech Stack

- Python (Django):
- SQLite3:
- Bootstrap: 
- Git: version control

## Usage 

## Challenges / Tradeoffs

### yardsearcher.models.Vehicle

Junkyards do not track the same details for the vehicles in their inventory.  Only a few may include the VINs, colors, or actual images of their vehicles, but most agree that year, make, model, and yard ids are critical details for operation. 

I've decided to build a single Vehicle Model that stores all details (leaving fields blank if needed). I could have built models for each junkyard that stored inventory-specific details, but my approach will make referencing vehicles in other entities easier, and support future crowdsourcing efforts at `completing` inventories.  

## License / Credits