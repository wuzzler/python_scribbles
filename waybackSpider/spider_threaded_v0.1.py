#/usr/bin/env python3

import argparse
import requests
import queue
import threading

archiveURL = 'https://web.archive.org/__wb/calendarcaptures/2?url='
snapshotBaseURL = 'https://web.archive.org/web/'

def getDayLinks(targetUrl, years):
    dayLinks = []

    # make request for snapshots per day on year
    for y in years:
        print('[ i ] Processing year: {}'.format(y))
        res = requests.get('{}{}&date={}&groupby=day'.format(archiveURL, targetUrl, y))

        if res.status_code != 200:
            print('[ E ] Error on request, http: {}'.format(res.status_code))

        # request snapshots per day from previous request
        print('[ i ] I count {} days with snapshots'.format(len(res.json()['items'])))
        for day in res.json()['items']:
            dayURL = '{}{}&date={}{:04d}'.format(archiveURL, targetUrl, y, day[0])
            dayLinks.append((dayURL, y, day[0]))
    
    return dayLinks

def getSnapshotLinks(qin, qout, targetUrl):
    while not qin.empty():
        url = qin.get()

        # TryCatch because this was prone to errors (timeouts mostly)
        try:
            res = requests.get(url[0], timeout=35)

            for r in res.json()['items']:
                finalURL = '{}{}{:04d}{:06d}/{}'.format(snapshotBaseURL, url[1], url[2], r[0], targetUrl)
                qout.put(finalURL)
            q.task_done()

        except Exception as e:
            print('[ e ] Url failed')
            print(type(e))

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--URL', help = 'Archived page to fetch', required=True)
    parser.add_argument('-y', '--year', type = int, help = 'Year to fetch', required=True)
    parser.add_argument('-s', '--streak', type = int, help = 'How many years to fetch, if more than just one')
    args = parser.parse_args()

    # calc years from parameters
    years = [x for x in range(args.year, args.year+args.streak+1 if args.streak else args.year+1)]

    # get dayLinks on one thread - this is 'fast&stable'
    result = getDayLinks(args.URL, years)

    # multithreading rest meaning get all links of all snapshots on the different days!
    q = queue.Queue(maxsize=0)
    qres = queue.Queue(maxsize=0)
    threadCtr = 10

    # add the daylinks into the queue
    list = [q.put(link) for link in result]

    print('[ i ] Spawning threads')
    threads = []
    for i in range(threadCtr):
        thread = threading.Thread(name=i, target=getSnapshotLinks, args=(q, qres, args.URL))
        threads += [thread]
        thread.setDaemon(True)
        thread.start()
    
    q.join()

    # extract the snapshot links from the queue
    x = []
    while qres.qsize():
        x.append(qres.get())

    print(x)
