class A:
    def __init__(self):
        self.attribute = 1
        print("A's __init__")
    
    def method(self):
        print("A's method")

class B(A):
    def __init__(self):
        print("B's __init__")
    
    def method(self):
        print("B's method")

class C(A, B):
    def __init__(self):
        self.id = "benhur"
        super(C, self).__init__()
        print("C's __init__")
    
    def method(self):
        print("C's method")

# Create an instance of C
c = C()
c.method()
