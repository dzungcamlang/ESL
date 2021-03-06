'''
Created on 2014-5-26

@author: xiajie
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def discriminant(x, u, thegma, pi):
    inthegma = np.linalg.inv(thegma)
    return np.transpose(x).dot(inthegma).dot(u) - 0.5*np.transpose(u).dot(inthegma).dot(u) + np.log(pi)

def classify(x, U, T, P, K):
    dmax = -999999999
    index = 99
    for i in range(K):
        dis = discriminant(x, U[i], T, P[i])
        if dis > dmax:
            dmax = dis
            index = i
    return index

def cal_mean(data_set, K):
    means = np.zeros((K,len(data_set[0][0])))
    for k in range(K):
        means[k] = np.mean(data_set[k], axis=0)
    return means

def cal_thegma(data_set, means, K, N):
    p = len(means[0])
    thegma = np.zeros((p,p))
    for k in range(K):
        g = np.zeros((p,p))
        for i in range(len(data_set[k])):
            x = data_set[k][i]
            diff = x - means[k]
            g += np.outer(diff, diff)/(N-K)
        thegma += g
    return thegma

def cal_pi(data_set, K, N):
    pi = np.zeros(K)
    for k in range(K):
        pi[k] = len(data_set[k])/float(N)
    return pi

def simulate_data():
    data_set = []
    centers = [(2.,2.),(3.5,0.),(0.5,0.)]
    cov = [[1.,.5],[.5,1.]]
    for k in range(len(centers)):
        center = centers[k]
        data = np.zeros((30, 2))
        for i in range(30):
            x = np.random.multivariate_normal(center, cov, 1)
            data[i] = x
        data_set.append(data)
    return data_set, 90

def cook_data(data_set):
    data = np.zeros((len(data_set)*len(data_set[0]),2))
    classes = np.zeros(len(data))
    idx = 0
    for i in range(len(data_set)):
        for j in range(len(data_set[i])):
            data[idx] = data_set[i][j]
            classes[idx] = i
            idx += 1
    return data, classes

def draw(data, classes, means, thegma, pi, resolution):
    mycm = mpl.cm.get_cmap('Paired')
    
    one_min, one_max = data[:, 0].min()-0.1, data[:, 0].max()+0.1
    two_min, two_max = data[:, 1].min()-0.1, data[:, 1].max()+0.1
    xx1, xx2 = np.meshgrid(np.arange(one_min, one_max, (one_max-one_min)/resolution),
                     np.arange(two_min, two_max, (two_max-two_min)/resolution))
    
    inputs = np.c_[xx1.ravel(), xx2.ravel()]
    z = []
    for i in range(len(inputs)):
        z.append(classify(inputs[i], means, thegma, pi, 3))
    result = np.array(z).reshape(xx1.shape)
    plt.contourf(xx1, xx2, result, cmap=mycm)
    
    plt.scatter(data[:, 0], data[:, 1], s=50, c=classes, cmap=mycm)
    
    plt.show()

if __name__ == '__main__':
    K = 3
    data_set, N = simulate_data()
    data, classes = cook_data(data_set)
    pi = cal_pi(data_set, K, N)
    means = cal_mean(data_set, K)
    thegma = cal_thegma(data_set, means, K, N)
    #print thegma
    draw(data, classes, means, np.array(thegma), pi, 200.)
    