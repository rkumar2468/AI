import heapq

class PrioQueue:
    """
    Class: PrioQueue
    This class is a priority queue implementation based on the heap datastructure.

    Functions:
        push - works based on the priority given to the list.
        getMin - gives the root node of the heap, followed by rebuilding the heap.
        isEmpty - checks if the queue is empty.
        cleanQueue - empties the queue.
        isConfigPresent - Checks if the given configuration is present in the queue.

    """
    def __init__(self):
        self.queue = []
        # self.idx = 0

    def push(self, list, priority):
        dict = (priority, list)
        heapq.heappush(self.queue, dict)

    def getMin(self):
        return heapq.heappop(self.queue)

    def isEmpty(self):
        return (len(self.queue) == 0)

    def cleanQueue(self):
        self.queue = []

    def isConfigPresent(self, config):
        for list in self.queue:
            if config == list[1]:
                return True
        return False

# if __name__ == '__main__':
#     q = PrioQueue()
#     list1= [10, 11]
#     list2= [1, 10, 11]
#     q.push(list2,2)
#     q.push(list1,1)
#     print q.getMin()[1]