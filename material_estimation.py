import math

class Linear_Estimate:
    def __init__(self, dividend, divisor, precision=3, cover_all=True):
        self.dividend = dividend
        self.divisor = divisor
        self.lengths = int(self.dividend // self.divisor)
        self.uncovered = round(self.dividend % self.divisor, precision)
        self.offcut = 0
        if cover_all:
            if self.uncovered > 0:
                self.lengths += 1
                self.offcut = round(self.divisor - self.uncovered, precision)
                self.uncovered = 0

class Area_Estimate:
    def compute(dividend, divisor):
        side0 = Linear_Estimate(dividend[0], divisor[0], cover_all=False)
        if side0.lengths == 0:
            side0 = Linear_Estimate(dividend[0], divisor[0])
            
        side1 = Linear_Estimate(dividend[1], divisor[1], cover_all=False)
        if side1.lengths == 0:
            side1 = Linear_Estimate(dividend[1], divisor[1])

        sheets = side0.lengths * side1.lengths
        area = (side0.uncovered * (dividend[1]-side1.uncovered)) + (side1.uncovered * dividend[0])
        extra_sheets = math.ceil(area / (divisor[0]*divisor[0]))
        return sheets + extra_sheets
    
    def __init__(self, dividend, divisor, precision=3):
        self.sheets = min(Area_Estimate.compute(dividend, divisor), 
                          Area_Estimate.compute(dividend, divisor[::-1]))
