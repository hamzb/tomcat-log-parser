# tomcat-log-parser

## Requirements
Python 2.7

## How to run it
usage: parse-file.py [-h] --file FILEPATH

parses a tomcat log file for endpoints invocations and response times

optional arguments:
  -h, --help       show this help message and exit
  --file FILEPATH  Log file path
  
## Sample output
./parse-file.py --file "/home/hamzaboulaares/Documents2/projects/scripts/tomcat.log"
```
|URL                      |# invocations|Avg. response time|
|/status/details          |28           |852 ms            |
|/status                  |210          |163 ms            |
|/transactions            |3            |395 ms            |
```
