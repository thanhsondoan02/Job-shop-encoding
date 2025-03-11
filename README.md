# Introduction
Solves Job-Shop Scheduling Problems by SAT encoding.

# Description

This repository solves some common Job-Shop Scheduling Problems by translating them into Boolean Satisfiability Problem (SAT) using the encoding method from M. Koshimura [[1](#ref1)]. For more detailed information, please refer to the [report](https://github.com/thanhsondoan02/Job-shop-encoding/blob/main/report/DoanThanhSon_report.pdf).

# Authors

Created by [Doan Thanh Son](https://github.com/thanhsondoan02), a student at VNU University of Engineering and Technology, as part of his graduation thesis project.

# Usage

## Installation

Before using, please clone this repo from Github.

```
git clone https://github.com/thanhsondoan02/Job-shop-encoding.git
```

After that, install python and all required libs.


## Find lower bound and upper bound
Encoding the problem with makespan 0 to get lower bound and upper bound:
```
python encode.py [problem name] 0
```
For example, to find lower bound and upper bound of problem Orb07:
```
python encode.py Orb07 0
```
The result is in orb07\Orb07_lower_upper.txt

## Find optimal makespan
With each makespan, solve the problem using this:
```
python encode.py [problem name] [makespan]
```
Solve a problem with multiple makespan:
```
python encode.py [problem name] [makespan1] [makespan2] [makespan3] ...
```
For example, solve problem La03 with makespan 596 & 597
```
python encode.py La03 596 597
```

## Find other schedules
Find other schedules in limit time using the following command:
```
python other_solution.py [problem name] [makespan] [limit time]
```
For example, find other schedules for problem FT06, with optimal makespan 56 with limit time of 60 seconds:
```
python other_solution.py FT06 56 60
```

# References
- <a id="ref1"></a>[1] M. Koshimura, H. Nabeshima, H. Fujita, and R. Hasegawa, “Solving open job
shop scheduling problems by sat encoding,” IEICE Transactions on Information
 and Systems, vol. E93.D, no. 8, pp. 2316–2318, 2010
