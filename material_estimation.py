import math

class Lengths:
    def use_standard(piece, standard, precision, ceil=True):
        if ceil == True:
            length = math.ceil(piece / standard)
            offcut = round(standard - (piece % standard), precision)
            return length, offcut
        else:
            length = int(piece // standard)
            remain = round(piece % standard, precision)
            return length, remain

    def use_offcut(piece, offcuts, precision):
        use = False
        if len(offcuts) == 0:
            pass
        else:
            offcuts = sorted(offcuts)
            for offcut in offcuts:
                if offcut >= piece:
                    offcuts.remove(offcut)
                    offcut = round(offcut - piece, precision)
                    if offcut > 0:
                        offcuts.append(offcut)
                    use = True
                    break
        return offcuts, use

    def estimate(pieces, standard, offcuts, precision):
        length = 0

        while len(pieces) != 0:
            
            piece = pieces[0] # Try largest piece
            offcuts, use = Lengths.use_offcut(piece, offcuts, precision)

            if use == True:
                pieces.remove(piece)

            else:
                piece = pieces[-1] # Try smallest piece
                offcuts, use = Lengths.use_offcut(piece, offcuts, precision)

                if use == True:
                    pieces.remove(piece)

                else:
                    piece = pieces[0] # Retuen to largest piece
                    length_, offcut = Lengths.use_standard(piece, standard, precision, ceil=True)
                    length += length_
                    pieces.remove(piece)

                    if offcut > 0:
                        offcuts.append(offcut)
            pieces = sorted(pieces, reverse=True)
            offcuts = sorted(offcuts)
        return length, offcuts
    
    def __init__(self, pieces, standard, offcuts=[], precision=2):
        
        self.pieces = sorted(pieces, reverse=True)
        self.standard = standard
        self.lengths, self.offcuts = Lengths.estimate(self.pieces[:], self.standard, offcuts[:], precision)


class Rectangle:
    def check_sides(sheet, standard, precision=2):
        check0 = (sheet[0] // standard[0]) * (sheet[1] // standard[1])
        check1 = (sheet[0] // standard[1]) * (sheet[1] // standard[0])
        dict_ = {check0: 0, check1:1}
        idx = dict_[min([check0, check1])]
        # print(check0)
        # print(check1)
    
        if check0 == check1:

            rem0 = [standard[0]-round(sheet[0] % standard[0], precision), standard[1]-round(sheet[1] % standard[1], precision)]
            rem1 = [standard[1]-round(sheet[0] % standard[1], precision), standard[0]-round(sheet[1] % standard[0], precision)]
        
            bools = [True if 0 in rem else False for rem in [rem0, rem1]]
            
            if bools.count(True) == 1: 
                idx = bools.index(True)
            else:
                sum_ = sum(rem0), sum(rem1)
                # print(sum_) 
                idx = sum_.index(min(sum_))  
           
        return idx
        
    def __init__(self, dimensions, standard, precision=2):
        self.extras = 0
        self.dimensions = dimensions

        idx_min = Rectangle.check_sides(self.dimensions, standard, precision=precision)  
        
        if idx_min == 0:
            self.standard = standard
        else:
            self.standard = standard[::-1]

        idx_max = abs(1-idx_min)
        self.idx_min = idx_min
        self.idx_max = idx_max
        
        side0 = Lengths([self.dimensions[idx_max]], self.standard[idx_max], precision=precision)
        self.side0 = side0.lengths
        offcut = side0.offcuts[0]

        if self.standard[idx_min] >= self.dimensions[idx_min]:
            if self.dimensions[idx_min] == 0:
                self.side1 = 0
            else:
                self.side1 = 1
        else:
            side1 = Lengths.use_standard(self.dimensions[idx_min], self.standard[idx_min], precision=precision, ceil=False)
            self.side1 = side1[0]
            side1_remain = side1[1]
            # print(self.side1)
            # print(side1_remain)
            
            if side1_remain > 0:
                if offcut >= side1_remain:
                    dim_max = self.dimensions[idx_max]
                    div = offcut // side1_remain
                    runs, leftover = Lengths.use_standard(dim_max, self.standard[idx_min], ceil=False, precision=precision)
                    if runs > (div * self.side1):
                        # print('here')
                        rec = Rectangle([side1_remain, leftover], self.standard, precision=precision)
                        # print('here')
                        # print(f"{rec.side0} * {rec.side1}")
                        self.extras += rec.side0 * rec.side1
                else:
                    # print("here too")
                    rec = Rectangle([side1_remain, self.dimensions[idx_max]], self.standard)
                    # print(rec.side0, rec.side1)
                    self.extras += rec.side0 * rec.side1
        # print(self.side0, self.side1)               
        self.sheets = (self.side0 * self.side1) + self.extras