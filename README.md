## How this works 

OSDAT(Open Soource Digital Asset Tracing)was developed as an analytical tool to track bitcoin transactions. The code has 3 main scripts which are parser.py, webscraping.py and MVP.py.  We are taking the parsed bitcoin data, putting it into a parser and analysing it and matching it with addresses that we webscared from bitcoin explorer. This helps us know which addresses must've been malicious when we trace the trail back. The data of the bitcoin transaction and the abused addresses are all uploaded on a database in elasticsearch which we access to do the analytics

## Workflow of OSDAT

The codebase consists of 3 scripts -
1. webscraping.py
2. parser.py
4. MVP.py

### web_scraping.py
This script web scrapes the abused addresses from Bitcoin Abuse and Wallet Explorer. The input to the script is the number of pages you want to scrape from Bitcoin Abuse and Wallet Explorer. And the output contains a list of abused addresses which are stored in a database in elasticsearch

### parser.py 
This script takes in all the btc .dat files and parsers them to get transaction data of the blocks. This script then uploads the parsed data into the elasticsearch database.

### MVP.py
This is the MVP code for tracing the addresses. We now have 3 files in elasticsearch - 

These files are given as raw input to the MVP script.
Steps to follow to trace the address:
1. Input the Bitcoin address you wish to trace
2. Mention the number of hops you want to go back
3. The system checks if the given input (address) matches any of the output columns (addresses).
4. If it finds any, it will go back to the inputs column and repeat the process again and again till there’s no more connection between the given address and the outputs. At the same time we also check if the address is present in the bitcoin abuse list or not. If an address is found in the bitcoin abuse list, the code terminates there, giving the output as the abused address and the amount of bitcoin transacted.

### Running the code 

python3 main.py on the terminal 

NOTE: This code is a work in progress since many more developments will be performed on top of it.
