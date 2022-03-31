class Range:
    def __init__(self, start: int, end: int):
        self.start_ = start
        self.end_ = end

    def start(self):
        return self.start_

    def end(self):
        return self.end_

    def __iter__(self):
        return iter(range(self.start_, self.end_))
