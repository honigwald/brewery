# implemenation of linked list
class List:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    def append(self, data):
        new = Node(data)
        if self.head == None:
            self.head = new
        else:
            current = self.head
            while current.next != None:
                current = current.getNext();
            current.setNext(new)

    def printList(self):
        current = self.head
        print "+-+-+-+-+-+-+-+"
        print "| Linked List |"
        print "+-+-+-+-+-+-+-+"
        while current != None:
            print "ID: %s\t Data: %s\t Next: %s" % (current, current.getData(), current.next)
            current = current.getNext()

    def getLength(self):
        length = 0
        current = self.head
        while current != None:
            length = length + 1
            current = current.getNext()
        return length

class Node:
    def __init__(self, data):
        self.data = data
        self.wait = False
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setNext(self, next):
        self.next = next
