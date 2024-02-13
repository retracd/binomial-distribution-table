#Binomial Probability Distribution Table Generator; made this for calculating stuff in Statistics class faster
#Written by Brent Mayes, 2024

import math # for calculating factorials and square roots
from tabulate import tabulate, SEPARATING_LINE # for easy formatting of the data after calculations
import argparse # for adding CLI functionality

class BinomialProbability: # Binomial Distribution class for calculating a single P(x)
    def __init__(self, _n, _x, _p, _precision=None): # Constructor containing n (sample size), x (num S), p (percent success), q (percent failure)
        self.n = int(_n) # n
        self.x = int(_x) # x
        self.p = _p # p, probability of success
        self.q = 1 - _p # q, probability of failure
        if _precision is not None:
            self.precision = int(_precision) # precision of calculations (rounding)   
    
    def combinationCalc(self): # calculates C(n, x)
        self.c = math.factorial(self.n) / (math.factorial(self.x) * math.factorial(self.n - self.x))

    def binomialFormulaCalc(self): # using C(n, x) and other variables, calculates X~B(n, p) for P(X=x)
        if not hasattr(self, 'c'): # if C(n, x) wasn't yet calculated, calculate it
            self.combinationCalc()

        self.P = self.c * pow(self.p, self.x) * pow(self.q, self.n - self.x) # calculate P(x)

        if hasattr(self, 'precision'): #if precision was set, apply it
            self.P = round(self.P, self.precision)

class BinomialDistTable: # Binomial Dist. Table class which utilizes multiple BinomialProbability classes
    def __init__(self, _n, _p, _precision=None): # x not needed because table generates BinomialProbability for every x, 0 thru n
        self.n = int(_n) # n
        self.p = _p # p, probability of success
        self.q = 1 - _p # q, probability of failure
        if _precision is not None:
            self.precision = int(_precision) # precision of calculations (rounding)

    def binomialProbabilityDistributionTableCalc(self): # creates n objects of class BinomialProbability to calculate the multiple P(x)'s
        if hasattr(self, 'precision'): # if precision was set, pass it...
            self.BPDTable = [BinomialProbability(self.n, i, self.p, self.precision) for i in range(self.n + 1)]
        else: # ...otherwise, don't
            self.BPDTable = [BinomialProbability(self.n, i, self.p) for i in range(self.n + 1)]
        for bp in self.BPDTable: # calling the binomialFormulaCalc() function for each BinomialProbability object
            bp.binomialFormulaCalc()

    def measuresOfSpreadCalc(self): # a measure of spread calculator which uses the list of BinomialProbabilities to calculate...
        self.mean = self.n * self.p
        self.variance = self.n * self.p * self.q
        self.standardDeviation = math.sqrt(self.variance)
        
    def displayBPDTable(self): # extracts the data from the list of objects and then formats it for CLI display
        if not hasattr(self, 'BPDTable'): # if the table was not yet calculated, calculate it
            self.binomialProbabilityDistributionTableCalc()
        # VVV zips together the set of x values (0 thru n) along with the respective Binomial Probability for that x
        self.displayTable = list(zip(xTable := [i for i in range(self.n + 1)], PTable := [bp.P for bp in self.BPDTable]))
        self.displayTable.append(SEPARATING_LINE) # adds a sepearting line for use with the tabulate() function
        self.displayTable.append(("Total", sum(PTable))) # adds a row which displays the total (this is theoretically always 1.0 but sometimes rounding can vary it just slightly)
        print() # adds a new line
        print(tabulate(self.displayTable, headers=['x', 'P(x)'], tablefmt="simple")) # generates the table

    def displayMeasuresofSpread(self): # separate function to display the measures of spread
        if not hasattr(self, 'mean'): # if the measures of spread were not yet calculated, calculate them
            self.measuresOfSpreadCalc()
        
        print() # prints new line + the 3 measures of spread
        print(f"E(x) = μ = {self.mean} AU")
        print(f"σ²       = {self.variance} AU²")
        print(f"σ        = {self.standardDeviation} AU")

def parseArgs(): # QoL function which groups all argparse library of functions together, defines arguments and options which need to be passed to the script
    parser = argparse.ArgumentParser(description="Calculates and outputs a Binomial Probability Distribution Table and several measures of spread when supplied with a sample size and success percentage.")
    parser.add_argument("n", type=int, help="n, sample size")
    parser.add_argument("p", type=float, help="p, probability of success, 0 < p < 1")
    parser.add_argument("--precision", type=int, help="(optional) decimal precision to round to", default=None)
    parser.add_argument("-t", "--only-table", action="store_true", help="only displays table")
    parser.add_argument("-m","--only-mos", action="store_true", help="only displays the measures of spread")
    return parser.parse_args()

def main():
    args = parseArgs() # fetches arguments passed to script, argparse catches if any are missing

    if args.only_table and args.only_mos: # double checks to make sure both mutually exclusive flags are not called
        raise Exception("--only-table and --only-mos are mutually exclusive")

    BPDTable = BinomialDistTable(args.n, args.p, args.precision) # after arguments checks are passed, variables are passed and...

    if args.only_table: # ... either the table ...
        BPDTable.displayBPDTable()
    elif args.only_mos: # ... or just the measures of spread ...
        BPDTable.displayMeasuresofSpread()
    else: # ... or both, are then calculated and displayed to the user
        BPDTable.displayBPDTable()
        BPDTable.displayMeasuresofSpread()

if __name__ == "__main__":
    main()