# README - 'waybackSpider'

This tool queries `web.archive.org` (waybackmachine) for the snapshot links of an archived URL.

Take into consideration: the wayback machine is rather slow, the queries of the links alone may take some time (depending on the snapshots taken)

**Reminder**: This script DOES NOT crawl the archived versions of the pages, just their links!

## installation

- no additional requirements needed

## Versions

There is a singlethread version and a multithread version.

## usage

```bash
# would query waybackmachine for the archived version of the specified URL in the year 2020
python spider.py -u https://www.rki.de/SharedDocs/FAQ/NCOV2019/gesamt.html -y 2020

# to display the available cli params
python spider.py --help 
```

## Requests used for spider

```python
# Request for year
# https://web.archive.org/__wb/calendarcaptures/2?url=https://www.rki.de/SharedDocs/FAQ/NCOV2019/gesamt.html&date=2022&groupby=day

# request per day of year
# https://web.archive.org/__wb/calendarcaptures/2?url=https://www.rki.de/SharedDocs/FAQ/NCOV2019/gesamt.html&date=20200417

# final url for snapshot
# https://web.archive.org/web/20211031010304/https://www.rki.de/SharedDocs/FAQ/NCOV2019/gesamt.html
```
