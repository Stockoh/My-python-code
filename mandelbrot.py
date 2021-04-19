import math
import math_2 as mt
import matplotlib.pyplot as plt
import itertools_2 as it
diag=lambda za:math.sqrt(za.imag*za.imag+za.real*za.real)

def mandelbrot(func=lambda x,c:(x*x)+c,n=1):
    L=[[0]*(10*(10**n)-1) for i in range(-10*(10**n),5*(10**n))]
    for y in range(-5*(10**n),5*(10**n)-1):
        y2=y/(5*(10**n)-1)
        for x in range(-10*(10**n),5*(10**n)-1):
            x2=x/(5*(10**n)-1)
            z=complex()
            c=complex(x2,y2)
            v=True
            for t in range(5):
                z=func(z,c)
                
                q=diag(z)
                q2=q*2
                if q>2 or (q!=q):
                    L[x+(10*(10**n))][y+(5*(10**n))]=t
                    v=False
                    break
            if v:
                L[x+(10*(10**n))][y+(5*(10**n))]=t
        #print()
	
    plt.imshow(L)
    plt.xticks([])
    plt.yticks([])
    plt.show()
mandelbrot(n=3)





