# binomial-distribution-table
CLI-accessible Python script which, when passed proper arguments, calculates and displays a binomial distribution table.

Taken directly from terminal:
 py  python .\binomial_distribtuion_table.py -h
usage: binomial_distribtuion_table.py [-h] [--precision PRECISION] [-t] [-m] n p

Calculates and outputs a Binomial Probability Distribution Table and several measures of spread when supplied with a sample size and success percentage.

positional arguments:
  n                     n, sample size
  p                     p, probability of success, 0 < p < 1

options:
  -h, --help            show this help message and exit
  --precision PRECISION
                        (optional) decimal precision to round to
  -t, --only-table      only displays table
  -m, --only-mos        only displays the measures of spread
