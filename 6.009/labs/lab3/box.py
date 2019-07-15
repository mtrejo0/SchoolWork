def sign(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1
def bounding_box(p,box):
    print(box.sorted())
    

    pass # Your code here
print(bounding_box((1,1),[(0, 0), (5, 0), (5, 5), (0, 5)]))