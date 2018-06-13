#config 置信度阈值
SUPPORT_RATE_THRESHOLD = 0.4

# 判断 b 列表中是否包含 a 列表的所有元素
def containes(a,b):
    try:
        for i in a:
            # print("target: ",i)
            if b.index(i)>=0:
                continue 
                # print("finded :",i," continue")
        return True
    except ValueError as e:
        # print("some error occured")
        # print(e.value)
        return False


def apriori(Lpre,raw):
    # find big L
    rows = len(raw)
    bigLpre = list()
    print("L pre: ",Lpre)
    for element in Lpre: # calculate support rate
        count = 0
        for row in raw:
            if containes(element,row):
                count += 1
        sr = count/rows
        print("Support Rate of ",element," is : ",sr)
        if(sr >= SUPPORT_RATE_THRESHOLD):
            bigLpre.append(element)

    print("big L pre: ",bigLpre)

    # collect k+1 L
    k = len(bigLpre[0])
    Lnext = list()
    
    if k==1:
        for i in range(0,len(bigLpre),1):
            for j in range(i+1,len(bigLpre),1):
                Lnext.append([bigLpre[i],bigLpre[j]])
        return Lnext
    elif k > 1:
        for i in range(0,len(bigLpre),1):
            for j in range(i+1,len(bigLpre),1):
                if bigLpre[i][0:k-1] == bigLpre[j][0:k-1] and bigLpre[i][k-1] != bigLpre[j][k-1]:
                    # 构建新项
                    # newelement = list(bigLpre[i])
                    newelement = [el for el in bigLpre[i]]
                    newelement.append(bigLpre[j][k-1])
                    # print("new element: ",newelement)
                    Lnext.append(newelement)
        print(Lnext)
        return Lnext
    else:
        return None


# main
def main():
    datafile = open('data.txt')
    rawdata = list()

    L1 = set()
    for line in datafile: # 提取第一项集,并保存原始数据表
        elements = [i.strip('\n') for i in line.split(' ')]
        rawdata.append(elements)
        for i in elements:
            L1.add(i)

    L1 = list(L1)
    L1.sort()

    # apriori
    L = apriori(L1,rawdata)
    print("L 2: ",L)
    L = apriori(L,rawdata)
    print("L 3: ",L)


main()