#_*_ coding:utf8 _*_
from math import log
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签



def is_binary_channel_matrix_symmetric(bc_matrix):
    '''
    判断二元信道是否对称，是返回True，否返回False。
    '''
    a = sorted(bc_matrix[0]) #排列矩阵第一行
    b = sorted(bc_matrix[1])
    c = sorted(Y_over_X[:][0]) #排列矩阵第一列
    d = sorted(Y_over_X[:][1])
    return ((a == b) & (c == d)) #同时比较行和列


def calculate_BSCchannel_capacity(P):
    '''
    计算信道容量。
    输入P为数组，返回对应的BSC信道容量的数组。
    输入P为数值，返回BSC信道容量数值。
    '''
    C = []
    try: #如果P是数组
        for p in P:
            if (p != 0) & ((1-p) != 0):
                c = 1 + (1-p)*log(1-p,2) + p*log(p,2)
            else :
                c = 1
            C.append(c)
        return C
    except: #如果P是一个值
        p = P
        if (p != 0) & ((1-p) != 0):
            c = 1 + (1-p)*log(1-p,2) + p*log(p,2)
        else :
            c = 1
        return c



def entropy_my(x):
    '''
    计算信源熵
    '''
    HX = 0
    for i in x:
        if i != 0:
            HX += i*log(i,2)

        else:
            HX += 0
    return -HX

    
def average_mutual_information(X,Y_over_X):
    '''
    求平均互信息。
    输入信源概率分布和信道转移概率。
    返回平均互信息。
    '''
    w = X[0]
    p = Y_over_X[0][1]
    pY0 = w*(1-p) + (1-w)*p
    pY1 = (1-w)*(1-p) + w*p
    Y = [pY0,pY1] #求信宿概率分布
    HY = entropy_my(Y) #求信宿熵H(Y)
    if (p != 0) & ((1-p) != 0):
        Hp = -((1-p)*log(1-p,2) + p*log(p,2))
    else:
        Hp = 0


    IXY = HY - Hp #求平均互信息

    return IXY,HY,Hp


#初始化数据
w = 2/3.
X = [w,1-w] #信源概率分布
p = 0.2
Y_over_X = [[1-p,p],[p,1-p]] #信道转移概率矩阵
if is_binary_channel_matrix_symmetric(Y_over_X): #判断二元信道对称性，如果对称，则继续计算
    print "Binary channel matrix is symmetric."
    C1 = calculate_BSCchannel_capacity(p) #计算当前BSC信道容量
    print "BSC channel capacity is {0:.2f}".format(C1)
    P = [i/float(100) for i in range(0,101,1)] #让P取值为0到1，步长为0.01
    C2 = calculate_BSCchannel_capacity(P) #计算P从0到1变化时，对应的BSC信道容量

    plt.plot(P,C2)
    plt.title(u"当p从0到1之间变化时的信道容量曲线")
    plt.xlabel("p")
    plt.ylabel("C(bit/symbol)")
    plt.show()

    print
    IXY1,HY,Hp = average_mutual_information(X,Y_over_X)#求平均互信息
    print 'Average mutual information is {0:.2f}'.format(IXY1)
##画固定信源分布时的平均互信息曲线

    print
    print



    IXY2 = []
    for k in P:

        Y_over_X2 = [[1-k,k],[k,1-k]]
        ixy,hy,hp = average_mutual_information(X,Y_over_X2)
        IXY2.append(ixy)

    plt.plot(P,IXY2)
    plt.title(u"固定信源分布，当p从0到1之间变化时的平均互信息曲线")
    plt.xlabel("p")
    plt.ylabel("I(X;Y)")
    plt.show()
    print "当固定信源的概率分布时，则平均互信息I(X;Y)是信道特性p的下凸函数。"
    print "当p = 0.5时，I(X;Y) = 0。"
    print "当p = 0 或 p = 1时， I(X;Y) = H(w) = H(X) , 此时H(X)为{0:.2f}".format(entropy_my(X))






##画固定信道时的平均互信息
    print
    print


    W = [i/float(100) for i in range(0,101,1)] #让W取值为0到1，步长为0.01
    IXY2 = []
    for v in W:
        X2 = [v,1-v]
        ixy,hy,hp = average_mutual_information(X2,Y_over_X)
        IXY2.append(ixy)

    plt.plot(W,IXY2)
    plt.title(u"固定信道，当w从0到1之间变化时的平均互信息曲线")
    plt.xlabel("w")
    plt.ylabel("I(X;Y)")
    plt.show()
    print "当信道固定，即p为一个固定常数时，可得出I(X;Y)是信源分布的上凸函数。"
    print "当w = 0或w = 1时，I(X;Y)为0。"
    print "此时H(p)为{0:.2f}，当w = 0.5时，I(X;Y)为 1-H(p)即为 {1:.2f}".format(hp, 1-hp)

else:
    print "Binary channel matrix is not symmetric."
