
def minFunc(numVar, stringIn):
    brack_minterms=stringIn.find(')')
    minterms=stringIn[1:brack_minterms]
    string = minterms.split(',')
    string = list(map(int, string))
    length=len(string)
    group = [[] for x in range(numVar+1)]

    for i in range(length):
        string[i]= bin(string[i])[2:]
        if len(string[i]) < numVar:
            for j in range(numVar - len(string[i])):
                string[i] = '0'+ string[i]

        index = string[i].count('1')
        group[index].append(string[i])

    all_group = []
    unmatched = []
 
    while (len(group)!=0):
        all_group.append(group)
        next_group, unmatched = combinePairs(group,unmatched)
        group = removeRedundant(next_group)
    
    s = ''
    for i in unmatched:
        s+=AlphabetsFromBinary(i) + ","

    Table = [[0 for x in range(length)] for x in range(len(unmatched))]

    for i in range(length):
        for j in range (len(unmatched)):
            if compBinarySame(unmatched[j], string[i]):
               Table[j][i] = 1
    #prime contains the index of the prime implicant terms
    primes = findMinVal(Table, unmatched)
    primes = removeRedundant(primes)

    for prime in primes:
        s=''
        for i in range(len(unmatched)):
            for j in prime:
                if j == i:
                    s+=AlphabetsFromBinary(unmatched[i])+'+'
        stringOut=s[:(len(s)-1)]
    return stringOut


#compare two binary strings, check where there is one difference
def compareBinary(s1,s2):
    pos = 0
    count = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            pos = i
            count+=1       
    if count != 1:
        return(False, None)
    else:
        return (True, pos)


#combine pairs and make new group
def combinePairs(group, unmatched):
    l = len(group)-1
    check_list = []
    next_group = [[] for x in range(0,l)]
    for i in range(0,l):
        for e1 in group[i]:
            for e2 in group[i+1]:
                b, pos = compareBinary(e1, e2)
                if b == True:
                    check_list.extend((e1,e2))
                    q=0
                    if(q==0):
                        new_ele = list(e1)
                        new_ele[pos] = '*'
                        new_ele = "".join(new_ele)
                        next_group[i].append(new_ele)

    for i in group:
        for j in i:
            if j not in check_list:
                unmatched.append(j)
    return(next_group,unmatched)


#remove redundant lists in 2d list
def removeRedundant(next_group):
    new_group = []
    for j in next_group:
        new=[]
        for i in j:
            if i not in new:
                new.append(i)
        new_group.append(new)
    return(new_group)


#print the binary code to letter
def AlphabetsFromBinary(s):
    n = 0
    end = ''
    ch = 'w'
    Flag = False

    for i in range(len(s)):
        if Flag != True:
            if s[i] == '0':
                end+=ch +'\''
            elif s[i] == '1':
                end+= ch
        if Flag != False:
            if s[i] == '1':
                end+= ch + str(n)
            elif s[i] == '0':
                end+= ch + str(n) + '\''
            n+=1

        if(ch==122 and Flag != True):
            ch = 65
        elif Flag != True:
            ch = chr(ord(ch)+1)
        elif(ch ==90):
            ch = 97
            Flag = True
    return(end)


#compare if the number is same as implicant term
def compBinarySame(term,number):
    for i in range(len(term)):
        if term[i] != '*':
            if term[i] != number[i]:
                return False
    return(True)


#remove redundant in 1d list
def removeRedundantList(list):
    new_list = []
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list


#find essential prime implicants ( col num of ones = 1)
def findPrime(Table):
    prime = []
    for col in range(len(Table[0])):
        count = 0
        pos = 0
        for row in range(len(Table)):
            if Table[row][col] == 1:
                count += 1
                pos = row

        if count == 1:
            prime.append(pos)
    return prime


def checkAllZero(Table):
    for i in Table:
        for j in i:
            if j != 0:
                return False
    return True


#multiply two terms 
def multiplication(list1, list2):
    list_final = []
    if len(list1)==0:
        return list2
    elif len(list1) == 0 and len(list2)== 0:
        return list_final
    elif len(list1)==0:
        return list2
    elif len(list2)==0:
        return list1
    else:
        for i in list1:
            for j in list2:
                if i != j:
                    list_final.append(sorted(list(set(i+j))))
                else:
                    list_final.append(sorted(i))
        return list(list_final for list_final,_ in itertools.groupby(list_final))


#Petrick's Method
def PetrickMethod(Table):
    P = []
    for col in range(len(Table[0])):
        p =[]
        for row in range(len(Table)):
            if Table[row][col] == 1:
                p.append([row])
        P.append(p)

    for l in range(len(P)-1):
        P[l+1] = multiplication(P[l],P[l+1])

    P = sorted(P[len(P)-1],key=len)
    final = []

    min=len(P[0])
    for i in P:
        if len(i) == min:
            final.append(i)
        elif(len(i)!=min):
            break
        else:
            break
    return(final)


#Table = n*n list
def findMinVal(Table, unmatched):
    P_final = []
    essential_prime = findPrime(Table)
    essential_prime = removeRedundantList(essential_prime)

    if len(essential_prime)>0:
        s = ''
        for i in range(len(unmatched)):
            for j in essential_prime:
                if j == i:
                    s+=AlphabetsFromBinary(unmatched[i])+','
                elif j!=i:
                    break

    for i in range(len(essential_prime)):
        for col in range(len(Table[0])):
            if Table[essential_prime[i]][col] == 1:
                for row in range(len(Table)):
                    Table[row][col] = 0

    if checkAllZero(Table) == True:
        P_final = [essential_prime]
    else:
        P = PetrickMethod(Table)

        P_cost = []
        for prime in P:
            count = 0
            for i in range(len(unmatched)):
                for j in prime:
                    if j == i:
                        count+= cal_efficient(unmatched[i])
            P_cost.append(count)

        for i in range(len(P_cost)):
            if P_cost[i] == min(P_cost):
                P_final.append(P[i])
        for i in P_final:
            for j in essential_prime:
                if j not in i:
                    i.append(j)
    return(P_final)


#calculate the number of literals
def cal_efficient(s):
    count = 0
    i=0
    while(i<len(s)):
        if s[i] != '*':
            count+=1
    return(count)



n = int(input("Enter the number of queries: "))

for i in range(n):
    v = int(input("\nNo. of variables: "))
    s = input("Function [eg: (0,2,5,7,8,10,13,15)]: ")
    print("Simplified Expression:", minFunc(v,s))





