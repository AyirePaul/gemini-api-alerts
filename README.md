# API Alerting Tool

## How to run
Ensure python and jq is installed on your system (see [Dependencies](#dependencies)), and your terminal is in the script directory.
Run the following to see allowed commands.
```shell
python apiAlerts.py -h
```

### Example Usage
Run `All` trading pairs
```shell
python apiAlerts.py -c All -d 1.5
```

Run on `btcusd` pair
```shell
python apiAlerts.py -c btcusd -d 1.5
```

## Running via docker
Build the image
```shell
docker build -t api-alerts . 
```

Display the help page
```shell
docker run -it api-alerts
```

Run `All` trading pairs
```shell
 docker run -it api-alerts -c All  
```

Run on `btcusd` pair
```shell
 docker run -it api-alerts -c btcusd  
```

## Dependencies
You will need `requests` and `jq` on your environment to run this script.

### Installing Dependencies
```shell
pip install requests jq
```

## Further Improvements
1. I could check the trading_pair passed in against the symbols endpoint for better error messages
2. I could improve overall handling and outputs.
3. Add a command (symbols) to print out supported trading pairs.

## Approach
I follow a pretty straight forward path to solving. 
1. Get the arguments, set appropriate defaults.
2. If `All` currency, I get list of currencies to process;
3. On each currency, I fetch the ticker information, calculate the values needed for the output
4. Using logging, send out an alert

### Issue faced
I faced some issues piping to jq. I had used "print" in some area for debugging and this made jq to fail each time it got the said output.


## Time taken
It took me about 2 hours to write the solution. Additional 1 hour to document and create a dockerfile.