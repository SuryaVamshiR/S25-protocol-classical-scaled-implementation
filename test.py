import random
import numpy as np
n1=10000
n=100000
a=np.zeros((n),dtype=np.int64)    
def dist(a1,a2):#computes manhatten distance modded by 4
    d=0
    for i in range(6):
       d=d+abs(a1[i]-a2[i])%4 
    return d

def storagearr(a3,q,a):#stores all positions of a3 and returns the respective position of q
    s=np.zeros((10000),dtype=np.int64)
    k=0
    
    for i in range(n-6):
        v=0
        for j in range(6):
            if a3[j]==a[i+j]:
                continue
            else:
                v=1
                break
        if v==0:
             
             s[k]=i+6
             k=k+1
    return s[q]
def storagearr1(a3,q,a):#stores all positions of a3 and returns the number of elements
    s=np.zeros((10000),dtype=np.int64)
    k=0
    
    for i in range(n-6):
        v=0
        for j in range(6):
            if a3[j]==a[i+j]:
                continue
            else:
                v=1
                break
        if v==0:
        
             s[k]=i+6
             k=k+1
    return k

lrm=np.zeros((100,100),dtype=np.int64)
dum1=np.zeros((6),dtype=np.int64)
def LRM():#defines the dictionary
   
    k=0
    
   
    for dum1[0] in {1,3}: 
        for dum1[1] in {0,2}:
            for dum1[2] in {2,0}:
                for dum1[3] in {1,3}:
                    for dum1[4] in {1,3}:
                        for dum1[5] in {0,2}:
                          
                            for i7 in range(6):
                                
                                lrm[k][i7]=dum1[i7]
                            k=k+1
                                
    return k
          
def mind(mes):#returns the minimum distance between mes and some lrm[][]
   ldist=n
    
   for i in range(LRM()):
       d=0
       for j in range(6):
           d=d+np.abs(lrm[i][j]-mes[j])    
       if ldist>d:
           ldist=d
   return ldist
def messageallocator(q,r,s):#returns particular element in qmod
    qmod=np.zeros((n1,n1),dtype=np.int64)
    d=mind(q)
    w=0
    for i in range(LRM()):
        p=0
        
        for j in range(6):
            p=p+np.abs(lrm[i][j]-q[j])    
        if p==d:
            for k in range(6):
                qmod[w][k]=lrm[i][k]
            w=w+1
        else:
            continue
                
            
    return qmod[r][s]
    

def message2allocator(q):#returns the number of rows of qmod
    qmod=np.zeros((n1,n1),dtype=np.int8)
    d=mind(q)
    
    w=0
    for i in range(LRM()):
        p=0
        
        for j in range(6):
            p=p+np.abs(lrm[i][j]-q[j])    
        if p==d:
            for k in range(6):
                qmod[w][k]=lrm[i][k]
            w=w+1
        else:
            continue
                
            
    return w
def lrmcheck(q,state,p,m,n,o):#checks the closest instance to the given lrm in state
    k=np.zeros((n1,6),dtype=np.int32)
    q1=0
    for i in range(p):
        val=0
        for j in range(6):
            check=np.abs(q[j]-state[i][j])
            if check==2:    
                val=1    
        if val==0:
            for j in range(6):
                k[q1][j]=state[i][j]
            q1=q1+1
                
    
    if m==1:
     return q1  
    else:
     return k[n][o]
        
            
def main():# main function to execute and document results
    n=1000000000# file size
    averagel=0#for testing purpose
    trials=0#number of iterations of test
   
    a=np.zeros((n),dtype=np.int8)#initializing the file array
    
    for i in range(n):#assigning random numbers in range 0-3
        a[i]=random.randint(0,3)
    
    print("generated file-",a)#benchmark to test bottlenecks
    while trials<1:  
     c=np.zeros((6),dtype=np.int8)#initializing first message
     
     ac=np.zeros((4,6),dtype=np.int8)
     for i in range(6):
         a1=random.randint(0,10000)
         c[i]=a[a1+i]#assigning the message to c
         for j in range(4):
             ac[j][i]=c[i]
     mmi=random.randint(0,5)
     print("message 1 is-",c)
     for i in range(4):
         ac[i][mmi]=i#storing all attacker possibilities after 1st message
     print("ac",ac)
     print("c",c)
     apos=np.zeros((10000),dtype=np.int64)#initializing the position of attacker storage
     pos=np.zeros((10000),dtype=np.int64)#initializing the position storage array
     l=storagearr1(c,1,a)#finding number of positions containing c in file a
     al=np.zeros((4),dtype=np.int64)
     for i in range(4):
         al[i]=storagearr1(ac[i], 1, a)
     print("l",l,"al",al)
     
     al2=al[0]+al[1]+al[2]+al[3]
     for i in range(l):
        pos[i]=storagearr(c,i,a)#storing the position of instances
     for i in range(4):#storing position of instances of attacker
         for j in range(al[i]):
             apos[4*i+j]=storagearr(ac[i], j, a)
     print("positions of the messages are-",pos)
     averagel=averagel+l#for testing average number of iterations
     count=1#number of iterations needed to collapse to a single state
     print("begin cascading")
     while 1==1:#beginning of the collapsing sequence
      print("number of instances of message repeat is",l)
      state=np.zeros((n1,7),dtype=np.int64)#initializing the state array
      astate=np.zeros((n1,7),dtype=np.int64)#initializing attacker states
      for i in range(l):
         state[i][6]=pos[i]#storing the position along with the state found
         for j in range(6):
             state[i][j]=a[pos[i]+j]#assigning the message present after c
      print("states are-",state)
      if l==0:#safety break
          break
      for i in range(al2):
          astate[i][6]=apos[i]
          for j in range(6):
              astate[i][j]=a[apos[i]+j]
          
      k=random.randint(0,l-1)#selecting a random position from pos
      mes=np.zeros((6),dtype=np.int8)
      for i in range(6):
         mes[i]=state[k][i]#assigning the random message selected to mes
      b=message2allocator(mes)#stores number of lrms which are closest to mes
      print("message is-", mes)
      b1=random.randint(0,b-1)#chooses random lrm closest to message
      b2=np.zeros((6),dtype=np.int8)
      ab2=np.zeros((6),dtype=np.int8)
      ab3=np.zeros((6),dtype=np.int8)
      for i in range(6):
         b2[i]=messageallocator(mes, b1, i)#stores the lrm chosen in b1
         ab2[i]=b2[i]
         ab3[i]=b2[i]
      mmi=random.randint(0, 5)
      print("message sent to receiver is-",b2)
      if mmi in {0,3,4}:
          ab2[mmi]=1
          ab3[mmi]=3
      else:
          ab2[mmi]=0
          ab3[mmi]=2
      ap1=lrmcheck(ab2,astate,al2,1,1,1)
      ap2=lrmcheck(ab3,astate,al2,1,1,1)
      ap=ap1+ap2
     
      p=lrmcheck(b2,state,l,1,1,1)#checks state to return valid instance
      p1=np.zeros((n1,6),dtype=np.int64)
      atp1=np.zeros((n1,6),dtype=np.int64)
      for i in range(p):
         for j in range(6):
             p1[i][j]=lrmcheck(b2,state,l,0,i,j)#stores all valid states
      print("positions having valid instances is", p1)
      for i in range(ap):
         for j in range(6):
             if i<ap1:
              atp1[i][j]=lrmcheck(ab2,astate,al2,0,i,j)#stores all valid states
             else:
                 atp1[i][j]=lrmcheck(ab3,astate,al2,0,i-ap1,j)
      print(apos,astate)
      pos=np.zeros((10000),dtype=np.int64)#reallocating positions
      apos=np.zeros((10000),dtype=np.int64)#reallocating positions
      w1=0
      w2=0
      for j in range(p):
         
         for i in range(l):
         
             val=0
             for i1 in range(6): 
                 if state[i][i1]!=p1[j][i1]:#check to see if the state passed
                     val=1
             if val==0:
                 if state[i][6]<n and state[i][6]>0:#to prevent invalid positions
                  pos[w1]=state[i][6]+6#assigning new positions
                  w1=w1+1
      for j in range(ap):
         
         for i in range(al2):
         
             val=0
             for i1 in range(6): 
                 if astate[i][i1]!=atp1[j][i1]:#check to see if the state passed
                     val=1
             if val==0:
                 if astate[i][6]<n and astate[i][6]>0:#to prevent invalid positions
                  apos[w2]=astate[i][6]+6#assigning new positions
                  w2=w2+1
      
      l=w1
      al2=w2
      print(al2,l)
      count=count+1          
      if pos[1]==pos[2] or pos[1]==0:#chek for duplicate positions(needs more)
          trials=trials+1 
          break#break condition
      if w1>l:#divergence condition and printing message leading to error
           print(p, b2, p1)
           print("filtering did not succeed")
           trials=10000
           break
     
    print(averagel/100)
main()

           

    