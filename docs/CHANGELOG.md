# Changelog 

## [Unreleased]

### Added 
*	Added API endpoints to show inventory data
*	Support for sorting inventory data 
*   Support for visualizing inventory data (Vegalite) 
*   Support for fetching and displaying images of junkyard vehicles

### Fixed 
*	Popup button no longer protrudes parent container

### Changed
* 	

### Deprecated
*	No longer using queries to filter website data in scrapers

## [v.1.0.3] - 02/13/2026 

### Added 
*	Configured scraper for Pick-n-pull Summit to handle their vehicle API data 
*   Added Pick-n-pull summit to `known_yards`

### Fixed 
*	Searching for vehicle by year ('2017','07') shows vehicles

### Changed
* 	Updated `yardsearcher.utils.extractors' functions to accomodate Pnp - Summit's api json keys 
*   Updated `refresh_inventories` command to raise ValueError on unsuccessful formatting
*   Set regex expressions as variables for readability purposes


### Deprecated
*	

### Security 
*	


## [v.1.0.2] - 02/12/2026 

### Added 
*	Added "No results found" graphic 
*	Changelog

### Fixed 
*	

### Changed
* 	Map marker popup button colors to primary orange
* 	Reduced font sizes to balance inventory results 
* 	Uppercase the make & model inventory columns
*	Updated vehicle entry dates to "x months/days ago"

### Deprecated
*	

### Security 
*	

## [v.1.0.1] - 

### Added 
*	Added unit tests to rapidly test query parser functions
*	Added function that can grab year prefix from a query ("99 civic"-> "19") 

### Fixed 
*	Removed unclosed "script" tag below footer

### Changed
* 	Reinforced query parser/extractor functions to accept unformatted queries
*	Removed unused templates

### Deprecated
*	

### Security 
*	
## [v.1.0.0] -

