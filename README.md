# graph-partitioning-problem-with-ILS
Artificial Intelligence Lab Project: resolving graph partitioning problem with ILS

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

## Use different graph instance
You can change default instance editing the `instance` variable inside the `main.py` file.

## Instances
* ELT_INSTANCE : `3elt.graph`, a large graph instance with 4720 nodes and 13722 edges
* ADD32_INSTANCE = `add32.graph`, a large graph instance with 4960 nodes and 9462 edges
* ADD20_INSTANCE = `add20.graph`, a large graph instance with 2395 nodes and 7462 edges
* TEST100_INSTANCE = `test.100.graph`, a small graph instance with 99 nodes and 258 edges
* TEST_INSTANCE = `test.graph`, a small graph instance with 16 nodes and 32 edges

## Results
For any run, a new original and final graph image will be generated.
At the end of the defined runs (10), a performance file will show:
* best solution (min cut-size)
* mean solution
* standard deviation