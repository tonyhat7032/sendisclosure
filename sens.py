#!/usr/bin/python
import optparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
parser = optparse.OptionParser()
parser.add_option("-f", dest="Path", help="Enter the path/filename of links:")
parser.add_option("-p", dest="keys", help="Enter the path/filename for playload:")
parser.add_option("-o", dest="out", help="Enter the path/filename for output:")
(options, argumnets) = parser.parse_args()
if not options.Path:
    parser.error("Enter the file path which contains links:")
elif not options.keys:
    parser.error("Enter the file path which contains playloads:")

start = time.time()

f = open(options.Path, "r")
p = open(options.keys, "r")
line1 = f.readlines()
line2 = p.readlines()

targets = []
output = options.out


def playloads():
    for k in line1:
        url = k.rstrip()
        for j in line2:
            playload = j.rstrip()
            target = url + '/' + playload
            targets.append(target)


playloads()


def status(url):
    response = requests.get(url)
    status_code = response.status_code
    print(status_code, "--------->", url)
    if status_code == 200:
        print(url, file=open(output, "a"))


processes = []
with ThreadPoolExecutor(max_workers=10) as executor:
    for i in targets:
        processes.append(executor.submit(status, i))

for future in as_completed(processes):
    future.result()
    
    
end = time.time()
timetaken = (end - start)/60

print('Time taken =', timetaken, 'minutes')
