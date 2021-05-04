# Knapsack CS106

## Installation
Python >= ```3.8```
```bash
pip3 install -r requirements.txt
```

## Download data
```bash
bash download_data.sh
```

Unzip folder named ```kplib``` contains data from [here](https://github.com/likr/kplib)

## Run
Test case results are saved in ```TestResults``` folder. The name of each subdirectory represents the budget of the calculation performed. 

*For example:* ```300_s``` stands for computation budget is 300 seconds.


```bash
python3 main.py -o 1 : Run OR Tools 
                   2 : Run Genetic Algorithm
```