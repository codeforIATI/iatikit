class PyandiSet:
    def where(self, **kwargs):
        self._wheres = dict(self._wheres, **kwargs)
        return self

    def __getitem__(self, index):
        for current_idx, item in enumerate(self):
            if current_idx == index:
                return item
        raise IndexError('index out of range')

    def __len__(self):
        total = 0
        for x in self:
            total += 1
        return total

    def count(self):
        return len(self)

    def first(self):
        for first in self:
            return first

    def all(self):
        return self.get()

    def get(self):
        return list(iter(self))

    def find(self, **kwargs):
        return self.where(**kwargs).first()
