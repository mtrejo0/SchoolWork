.section ".text.init"
    .globl sort

/* Python code for reference
# p is an integer array
# n is the number of elements in p: n == len(p)
def sort(p, n):
    swapped = True
    while (swapped):
        swapped = False           # Pass starts
        for i in range(n - 1):    # i from 0 to n - 2
            if (p[i] > p[i + 1]):
                (p[i], p[i + 1]) = (p[i + 1], p[i]) # swap
                swapped = True
        n -= 1                    # Pass ends
    # Elements in p are in ascending order now
*/







sort:
    
    li      t0, 1       // swapped = t0 = 1 
    mv      t3,a0       // index of first element of array
    
    addi    t2,a1,-1    // t2= n-1
while:
    mv      t3,a0       // index of first element of array
    beqz    t0, done    // if t0==0 false so break
    li      t0,0    // swapped = 0 = false
    li      t1,0 // i = x6 = 0
    lw      t4, 0(t3)   // load ith element into t4

loop:
    lw      t4, 0(t3)
    addi    t3, t3, 4   // ith +1 element index


    lw      t5, 0(t3)   // p[i+1]

   
    ble     t4,t5, cont]
switch:

    mv      t6, t4 // temp = p[i]
    mv      t4, t5 // p[i]=p[i+1]
    mv      t5, t6 // p[i+1] = temp

    sw      t5, 0(t3) // saves p[i+1]

    

    sw      t4, -4(t3) // saves p[i]

    

    li      t0,1 // swapped = 1


cont:
    addi    t1,t1,1 // i++

    

    bne     t1,t2,loop // i!=n-1
    
    addi    t2,t2,-1 // n-=1

    j while

done:

    ret
