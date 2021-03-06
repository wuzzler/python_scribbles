#/usr/bin/env python3

import argparse
import requests

archiveURL = 'https://web.archive.org/__wb/calendarcaptures/2?url='
snapshotBaseURL = 'https://web.archive.org/web/'

def getSnapshotLinks(targetUrl, years):
    snapshotLinks = []

    # make request for snapshots per day on year
    for y in years:
        print('[ i ] Processing year: {}'.format(y))
        res = requests.get('{}{}&date={}&groupby=day'.format(archiveURL, targetUrl, y))

        if res.status_code != 200:
            print('[ E ] Error on request, http: {}'.format(res.status_code))

        # request snapshots per day from previous request
        print('[ i ] I count {} days with snapshots'.format(len(res.json()['items'])))
        for day in res.json()['items']:
            try:
                r = requests.get('{}{}&date={}{:04d}'.format(archiveURL, targetUrl, y, day[0]), timeout=5)
            
                # check snapshot time per day
                for snapshot in r.json()['items']:
                    finalURL = '{}{}{:04d}{:06d}/{}'.format(snapshotBaseURL, y, day[0], snapshot[0], targetUrl)
                    snapshotLinks.append((finalURL, y, day[0], snapshot[0]))
            except Exception as e:
                print('[ e ] Error on url: {}'.format('{}{}&date={}{:04d}'.format(archiveURL, targetUrl, y, day[0])))
    
    return snapshotLinks


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--URL', help = 'Archived page to fetch', required=True)
    parser.add_argument('-y', '--year', type = int, help = 'Year to fetch', required=True)
    parser.add_argument('-s', '--streak', type = int, help = 'How many years to fetch, if more than just one')
    args = parser.parse_args()

    # calc years from parameters
    years = [x for x in range(args.year, args.year+args.streak+1 if args.streak else args.year+1)]

    result = getSnapshotLinks(args.URL, years)

    print(result)
