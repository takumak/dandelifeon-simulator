# dandelifeon-simulator

This simulates [Dandelifeon] and suggests a initial Cell layout.

[Dandelifeon]: https://ftb.fandom.com/wiki/Dandelifeon

## Usage

```bash
$ python test.py -k 20
...continues improve layout susggestion infinitely...
[Press Ctrl+C to stop iteration]
```

## Example result

```bash
$ python test.py -k 20 
gen0: score=0 mana=0 cycle=0 cost=0
gen1: score=310.0 mana=360.0 cycle=12 cost=5
0000000000000000000000000000000000000000000000000000000000000000000000001c000000000008800000000000000000000000000000000000000000000000000000000000000000000000
gen2: score=710.0 mana=780.0 cycle=17 cost=7
0000000000000000000000000000000000000000000000000000000000000000000800001c000000800008800000000000000000000000000000000000000000000000000000000000000000000000
gen3: score=1540.0 mana=1620.0 cycle=38 cost=8
0000000000000000000000000000000000000000000000000000000000000000000800001c000020800008800000000000000000000000000000000000000000000000000000000000000000000000
+-------------------------+ +-------------------------+
|                         | |                         |
|                         | |                         |
|                         | |                         |
|                         | |                   *  *  |
|                         | |                  ** *   |
|                         | |             *** *   *   |
|                         | |            *  ****      |
|                         | |            **** *       |
|                         | |            **           |
|                         | |            *   **       |
|                  *      | |                **       |
|                ***      | |             o*  *       |
|              *     *    | |               ******    |
|               *   *     | |                  *  **  |
|                         | |                  **     |
|                         | |                  **   * |
|                         | |                      ** |
|                         | |                  * **** |
|                         | |                 ****  * |
|                         | |              *   * ***  |
|                         | |              * **       |
|                         | |             *  *        |
|                         | |                         |
|                         | |                         |
|                         | |                         |
+-------------------------+ +-------------------------+
score=1540.0 mana=1620.0 cycle=38 cost=8
0000000000000000000000000000000000000000000000000000000000000000000800001c000020800008800000000000000000000000000000000000000000000000000000000000000000000000
```

* `score` -> Evaluation function result
* `mana` -> Mana production
* `cycle` -> Number of generations needed to finish lifegame
* `cost` -> Cell blocks needed

## Continue from previous results

```bash
$ python test.py -k 20 --init 0000000000000000000000000000000000000000000000000000000000000000000800001c000020800008800000000000000000000000000000000000000000000000000000000000000000000000
```

## Best results

* [1_143_22.txt](./example_best_results/1_143_22.txt) : `mana=36000`, `cycle=143`, `cost=22`
* [2_104_26.txt](./example_best_results/2_104_26.txt) : `mana=36000`, `cycle=104`, `cost=26`
