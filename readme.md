# TableauExport

## Summary

Project aims to help people to make query for a view and download that view as png, pdf or csv format.

### Release Notes

#### 1.0

It supports only Tableau Views to query or download. It requires a filter that contains filter name and value with semi colon seperated each line. It produces a PDF, PNG or CSV file for each queries. 

## Installation

**Docker must be installed on your operating system.**

* Clone project.

* Open a terminal/command line in the root folder of project.

* Type: ```docker build --tag tableauexport:1.0 .```

## Run

Prepare a input.txt file that contains a filter name and value for each line. For instance

```
UserName:muhammedfatih
UserName:cyildirim
UserName:yigiterol
FirmName:BranderBox
```

### Windows

* For powershell: ```docker run -it --rm -v ${PWD}:/app/ tableauexport:1.0 python /app/main.py --username login@emailaddress.fortableau -p PASSWORD --server https://TABLEAUSERVER --site YOURTABLEAUSITENAME --output-folder .\out --input-file .\input.txt --viewName YOURTABLEAUVIEWNAME --pdf```

* For command line: ```docker run -it --rm -v %cd%:/app/ tableauexport:1.0 python /app/main.py --username login@emailaddress.fortableau -p PASSWORD --server https://TABLEAUSERVER --site YOURTABLEAUSITENAME --output-folder .\out --input-file .\input.txt --viewName YOURTABLEAUVIEWNAME --pdf```

### Unix

* ```docker run -it --rm -v $(pwd):/app/ tableauexport:1.0 python /app/main.py --username login@emailaddress.fortableau -p PASSWORD --server https://TABLEAUSERVER --site YOURTABLEAUSITENAME --output-folder .\out --input-file .\input.txt --viewName YOURTABLEAUVIEWNAME --pdf```