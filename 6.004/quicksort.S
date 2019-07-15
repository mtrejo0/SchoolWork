.section ".text.init"
    .globl sort

/* Python code for reference
# p is an integer array
# n is the number of elements in p: n == len(p)
def sort(p, n):
    quicksort(p, 0, n - 1)

def quicksort(p, start, end):      # Sort elements from p[start] to p[end]
    if (start < end):
        q = partition(p, start, end)
        quicksort(p, start, q - 1)
        quicksort(p, q + 1, end)

def partition(p, start, end):      # Divide p[start:end] into two subarrays, one with all
    pivot = p[end]                 # elements smaller or equal to a pivot value (the last
    i = start                      # value of input array), and another with all elements
    for j in range(start, end):    # larger than the pivot. Returns the index of the pivot.
        if (p[j] <= pivot):
            (p[i], p[j]) = (p[j], p[i]) # swap
            i += 1
    (p[i], p[end]) = (p[end], p[i]) # swap
    return i
*/
sort:

    
    addi sp,sp,-4
    sw ra,0(sp)     //save ra
    
    mv t0,a1        
    li t1,2 
    sll t0,t0,t1
    add a1,a0,t0
    addi a1,a1,-4

    jal quicksort

     lw ra,0(sp)
    addi sp,sp,4


    ret

quicksort:

    bge a0,a1,done // 

        addi sp,sp,-12
        sw ra,0(sp) 
        sw a0,4(sp) //  start
        sw a1,8(sp) //  end

        
    jal partition

        mv a3, a0
        addi a1,a3,-4 // q-1
        lw a0,4(sp) //end

    jal quicksort


        addi a0, a3, 4 // q+1
        lw a1,8(sp) // end


    jal quicksort


    lw ra,0(sp) //  q
    
    addi sp,sp,12

    done:
        ret


partition:


    lw t0,0(a1) // pivot = p[end]
    mv t1,a0 // i = start
    mv t2,a0 // j = start
    for:
        lw t3,0(t2) // p[j]
        blt t0,t3, nle
            lw t4, 0(t1) // swap
            sw t3, 0(t1)
            sw t4, 0(t2)
            addi t1,t1,4 // i++
            
        nle:
        addi t2,t2,4 // j++
    blt t2,a2,for

    lw t3,0(t1) // swap
    lw t4,0(a1)
    sw t3,0(a1)
    sw t4,0(t1)

    mv a0,t1 // return i

    ret 
