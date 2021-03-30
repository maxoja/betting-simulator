from ..enums import PosType


def slice_frame_from_back(df, size, shift_end=0, buffer=0):
    if shift_end < 0 or size+buffer+shift_end >= len(df):
        return None
        
    start = (-size-shift_end-buffer)
    end = len(df)-shift_end
    return df[start:end]


def slice_frame_from_front(df, size, shift_front=0, buffer=0):
    start = shift_front - buffer
    end = shift_front + size

    if start < 0 or end >= len(df):
        raise ValueError()

    return df[start:end]


class IndexRange:
    def __init__(self, start:int, exclusive_end:int):
        self.start = start
        self.end = exclusive_end

    def sliced_of(self, l):
        return l[self.start:self.end]

class Index:
    def __init__(self, irange:IndexRange, local_index:int):
        self.local = local_index
        if irange:
            self.glob = irange[0] + local_index
        else:
            self.glob = local_index

class EntryIndices:
    def __init__(self):
        self.__idx = []
        self.__type = []

    def append(self, i:Index, pos_type:PosType):
        self.__type.append(pos_type)
        self.__idx.append(i)

    def __getitem__(self, i):
        return self.__type[i], self.__idx[i]
    
    def size(self):
        return len(self.__idx)

