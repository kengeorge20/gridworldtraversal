class BinaryHeap:
    def __init__(self):
        self.heap = []

    def insert(self, item): # Inserts an item into the heap with tie-breaking.
        self.heap.append(item)
        self._percolate_up(len(self.heap) - 1)

    def pop(self): # Removes and returns the item of highest priority."""
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._percolate_down(0)
        return root

    def _percolate_up(self, index): # Percolate a node up the binary heap with tie-breaking.
        while (index - 1) // 2 >= 0:
            parent_idx = (index - 1) // 2
            if self.heap[index][0] < self.heap[parent_idx][0]:
                self.heap[index], self.heap[parent_idx] = self.heap[parent_idx], self.heap[index]
            elif self.heap[index][0] == self.heap[parent_idx][0] and self.heap[index][2] > self.heap[parent_idx][2]:
                self.heap[index], self.heap[parent_idx] = self.heap[parent_idx], self.heap[index]
            index = parent_idx

    def _percolate_down(self, index): # Percolate a node down the binary heap with tie-breaking."""
        while (index * 2 + 1) < len(self.heap):
            min_child = self._min_child(index)
            # Compare f-values first
            if self.heap[index][0] > self.heap[min_child][0]:
                self.heap[index], self.heap[min_child] = self.heap[min_child], self.heap[index]
            # If f-values are equal, prefer the node with the higher g-value (tie-breaking)
            elif self.heap[index][0] == self.heap[min_child][0] and self.heap[index][2] < self.heap[min_child][2]:
                self.heap[index], self.heap[min_child] = self.heap[min_child], self.heap[index]
            index = min_child

    def _min_child(self, index): # Find the index of the minimum child."""
        if (index * 2 + 2) > len(self.heap) - 1:
            return index * 2 + 1
        else:
            # Select the child with lower f-value or, if equal, the higher g-value
            if self.heap[index * 2 + 1][0] < self.heap[index * 2 + 2][0]:
                return index * 2 + 1
            elif self.heap[index * 2 + 1][0] == self.heap[index * 2 + 2][0]:
                if self.heap[index * 2 + 1][2] > self.heap[index * 2 + 2][2]:
                    return index * 2 + 1
                else:
                    return index * 2 + 2
            else:
                return index * 2 + 2