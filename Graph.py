import sys, random
from PyQt5.QtCore import QPointF
import Constant
import numpy as np

class Top:
    # self, QPoint - top, int - num
    def __init__(self, point, num):
        self.top = point
        self.number = num
        self.list = [] # the adjacency list type - rib

    def info(self):
        print('Number of the top = ', end = ' ')
        print(self.getNumber(), end=' ')
        print(';', end=' ')

        for top in self.list:
            top.info()

    def getNumber(self):
        return self.number

    def add(self, top, param):
        rib = Rib(top, param)
        self.list.append(rib) # add the top to the adjacency list



    # pointPut - QPointF, the place of the pressing
    # is the point inside the circle
    def inside(self, pointPut):
        corX = pointPut.x()
        corY = pointPut.y()

        a = (corX - self.top.x())**2+(corY - self.top.y())**2
        b = Constant.rad**2
        if a<=b:
            return True
        else:
            return False

    def x(self):
        return self.top.x()

    def y(self):
        return self.top.y()

    def getEdge(self):
        return self.list

    def exsitRoad(self, top2):
        for rib in self.list:
            if rib.isTo(top2):
                return True

        return False


class Rib:

    def __init__(self, to, param):
        self.to = to
        self.param = param # parameters of the rib (weight, price)

    def info(self):
        print('Куда: ', end=' ')
        print(self.to.getNumber(), end=' ')
        print('; weihgt = ', end=' ')
        print(self.weight)

    def isTo(self, top):
        return top == self.to

class Graph:

    def __init__(self):
        self.listV = [] # type - top
        self.dist = []
        self.parent = []
        self.countTop = 0 # счетчик вершины
        self.matrix = np.zeros((50,50), dtype = Rib)  # матрица смежности

    def size(self):
        return len(self.listV)

    # метод добавлен
    def exsitRoad(self, top1, top2):
        if self.matrix[top1.getNumber()][top2.getNumber()] != 0:
            return True
        return False


    def add(self, top):
        self.countTop += 1 # увеличиваем количество вершин
        self.listV.append(top)

    def addConnection(self, top1, top2, param):
        start = top1.getNumber()
        end = top2.getNumber()
        self.matrix[start][end] = Rib(end, param) # добавляем связь
        print(self.matrix[start][end])
        self.matrix[end][start] = Rib(start, param)


    def getSetV(self):
        return self.listV

    def deystra(self, start):

        if len(self.dist) == 0:
            self.initData()
        self.dist[start] = 0
        self.parent[start] = -1
        v = start # type - Top


        while not self.isVisit[v]:
            self.isVisit[v] = True

            # следующие две строки правка, в оригинале только закоменченая была
            for top in range(self.countTop+1):
                if self.matrix[v][top] != 0:
                    rib = self.matrix[v][top]
            #for rib in self.listV[v-1].list:
                    sum = 0
                    for i in rib.param:
                        sum = sum + i
                    #to = rib.to.getNumber()
                    to = top
                    if(self.dist[to] > self.dist[v] + sum):
                        self.dist[to] = self.dist[v] + sum
                        self.parent[to] = v
            v = 1
            dist = 9999999
            i = 1
            while i <=self.size():
                if((not self.isVisit[i]) and (dist > self.dist[i])):
                    dist = self.dist[i]
                    v = i
                i = i+1

        print(self.dist)

# было self.parent
    # int, int, list
    def printPath(self, start, end, parent):
        tmp = []
        tmp.append(end)

        # or c == -1 в цикле было
        c = parent[end]
        while c != start:
            tmp.append(c)
            c = parent[c]
            if c == -1 or c == 0:
                tmp.clear()
                return tmp # size = 0

        tmp.append(start)
        tmp.reverse()
        print("Path:")
        print(tmp)

        return tmp

    def initData(self):
        self.isVisit = []
        self.dist = []
        self.parent = []
        self.isVisit.clear()
        self.dist.clear()
        self.parent.clear()

        # +1 so the counting began with 1 for top
        #for i in range(self.size()+1):
        for i in range(self.countTop+1):
            self.dist.append(999999999)
            self.parent.append(0)
            self.isVisit.append(False)

    # если к исходному графу добабляется вершина и повторно ищется путь, то массивы основные кроме listV надо очищать
    # method delete graph all
    def deleteAll(self):
        # два метода добавлены
        self.countTop = 0
        self.matrix = np.zeros((50,50), dtype = Rib)

        self.listV.clear()
        self.dist.clear()
        self.parent.clear()

    def delete(self, x): # type - Top, top which we want to remove
        for i in range(len(x.list)):
            rib = x.list[i]
            for rib2 in rib.to.list:
                if rib2.to == x:
                    rib.to.list.remove(rib2)

        x.list.clear()
        self.listV.remove(x)

    def bfs(self, st):
        parent = []
        start = st # int
        #self.isVisit = []
        if len(self.isVisit) == 0:
            for i in range(len(self.listV) + 1):
                self.isVisit.append(False)
        queue = [] # int

        for i in range(len(self.listV) + 1):
            #self.isVisit.append(False)
            parent.append(-1)

        parent[start] = -1
        queue.append(start)

        while len(queue) != 0:
            curTop = queue.pop(0) # 0
            self.isVisit[curTop] = True

            for rib in self.listV[curTop-1].list:
                if not self.isVisit[rib.to.getNumber()]:
                    self.isVisit[rib.to.getNumber()] = True
                    queue.append(rib.to.getNumber())
                    parent[rib.to.getNumber()] = curTop

        path = self.printPath(1, len(self.listV), parent)
        return path

    def countComponent(self):
        countCom = 0
        self.beginComponent = []
        self.isVisit = []
        for i in range(len(self.listV) + 1):
            self.isVisit.append(False)

        i = 1
        while i < len(self.listV)+1:
            if not self.isVisit[i]:
                self.bfs(i)
                countCom = countCom + 1
                self.beginComponent.append(i) # список хранит вершины, с который начинает комонента
            i = i + 1

        return countCom # количество компонентов связности