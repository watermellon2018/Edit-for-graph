import sys, random
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QMainWindow, QAction, qApp, QPushButton, QLabel, QTextEdit,
QLineEdit, QCheckBox, QDialog, QGridLayout, QToolBar)
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QBrush, QImage, QPainter, QPen
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt, QPointF, QRectF
from Graph import Top, Graph
import Constant, random

# генератор работает на списках. Не использовать! Do not use!
# подсчитать путь

class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.buildGUI()
        self.graph = Graph()
        self.countCity = 0
        self.countCom = 0
        self.isHandle = False
        self.countParam = 2
        self.selectedTop = [] # list for two connected tops type - Top

    def buildGUI(self):
        self.resize(1000, 750)

        self.image = QImage(2000, 2000, QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.brushSize = 2
        self.brushColor = Qt.blue

        self.initNeed() # инициализируем нужные настройки

        self.statusBar()
        self.createWidget()
        self.center()
        self.setWindowTitle('Нахождение кратчайшевого пути')
        self.setWindowIcon(QIcon('iconCat.png'))
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.show()

    def initNeed(self):
        painter = QPainter(self.image)
        painter.drawText(QPointF(10, 50), "Начальная вершина: ")
        painter.drawText(QPointF(10, 70), "Конечная вершина: ")


    def mousePressEvent(self, event):
        selected = False  # typ - boolean
        topCur = Top(event.pos(), self.graph.size() + 1)  # type - Top
        point = event.pos()  # type - QPointF
        painter = QPainter(self.image)

        for top in self.graph.getSetV():
            if top.inside(point):
                self.brushColor = Qt.red  # selected
                selected = True
                topCur = top
                if top in self.selectedTop:
                    self.brushColor = Qt.blue
                    self.selectedTop.remove(top)
                else:
                    self.selectedTop.append(top)  # add in selected list

                self.pen(painter)
                painter.drawEllipse(topCur.x() - Constant.rad / 2, topCur.y() - Constant.rad / 2, Constant.rad,
                                    Constant.rad)

                break

        if event.button() == Qt.LeftButton:

            # if not selected top, then draw
            if not selected:
                # create the top of the graph and installed of the color pen
                self.brushColor = Qt.blue
                self.graph.add(topCur)
                self.countCity = self.countCity + 1
                painter.drawText(point, str(topCur.getNumber()))
                self.pen(painter)
                painter.drawEllipse(topCur.x() - Constant.rad / 2, topCur.y() - Constant.rad / 2, Constant.rad,
                                    Constant.rad)

            # create the line
            if len(self.selectedTop) == 2:
                self.brushColor = Qt.green
                self.pen(painter)
                top1 = self.selectedTop.pop(1) # type - Top
                top2 = self.selectedTop.pop(0)

                # check for excisting the road
                #if not top1.exsitRoad(top2):
                if not self.graph.exsitRoad(top1, top2):
                    painter.drawLine(top1.x(), top1.y(), top2.x(), top2.y())

                    # target - add first top (top1) connected top (top2) in the list
                    # bilaterial
                    if self.isHandle:
                        self.instalParametDialog()
                        self.brushColor = Qt.black
                        self.pen(painter)
                        param = []
                        for k in range(self.countParam):
                            param.append(int(self.parametrs[k].text()))
                            painter.drawText(
                                QPointF((top1.x() + top2.x()) / 2 + 5, (top1.y() + top2.y()) / 2 - 5 + 20 * k),
                                self.parametrs[k].text())
                        # закомменчено для варианта работы со списокм смежности
                        #top1.add(top2, param)
                        #top2.add(top1, param)
                        self.graph.addConnection(top1, top2, param)

                    else:
                        param = []
                        for i in range(self.countParam):
                            param.append(random.randint(1,100))
                        # добавлено
                        self.graph.addConnection(top1, top2, param)
                        #top1.add(top2, param)
                        #top2.add(top1, param)

                        self.brushColor = Qt.black
                        self.pen(painter)
                        for k in range(self.countParam):
                            painter.drawText(QPointF((top1.x() + top2.x()) / 2 + 5, (top1.y() + top2.y()) / 2 - 5 + 20*k),
                                                     "p=" + str(param[k]))

                self.brushColor = Qt.blue;
                self.pen(painter)
                painter.drawEllipse(top1.x() - Constant.rad/2, top1.y() - Constant.rad/2, Constant.rad, Constant.rad)
                painter.drawEllipse(top2.x() - Constant.rad/2, top2.y() - Constant.rad/2, Constant.rad, Constant.rad)

        self.update()


    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.image.rect(), self.image, self.image.rect())

    def pen(self, painter):
        painter.setPen(
            QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))  # installed the pen

    def createWidget(self):
        exitAction = QAction(QIcon('iconCat.png'), '&Выход', self)  # create action, install icon, text and parent(where it is)
        exitAction.setShortcut('Ctrl+Q')  # hot keys
        exitAction.setStatusTip('Выйти из приложения')  # tip
        exitAction.triggered.connect(qApp.quit)


        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)


        createBut = QPushButton('Создать')
        createBut.setShortcut('Ctrl+N')
        createBut.setToolTip('Настройки для графа')
        runBut = QPushButton('Запуск') # graph is generated, find the path
        runBut.setShortcut('Ctrl+R')
        runBut.setToolTip('Найти путь')
        clear = QPushButton('Удалить')
        clear.setShortcut('Delete')
        clear.setToolTip('Очистить')
        infoBut = QPushButton("Инфо")
        infoBut.setShortcut('Ctrl+I')
        infoBut.setToolTip('Информация о программе')


        createBut.clicked.connect(self.on_click)
        runBut.clicked.connect(self.click_run) # start the work of the basic target program
        clear.clicked.connect(self.click_del)
        infoBut.clicked.connect(self.click_info)

        toolbar = self.addToolBar('Exit')
        # toolbar.addWidget(createBut) потом добавить обратно
        toolbar.addWidget(runBut)
        toolbar.addWidget(clear)
        toolbar.addWidget(infoBut)


    def drawPath(self, path, painter):
        #self.brushColor = Qt.red
        #painter = QPainter(self.image)
        self.pen(painter)

        for j in range(len(path)-1):
            top1 = self.graph.listV[path[j+1]-1]  # type - Top
            top2 = self.graph.listV[path[j]-1]
            painter.drawLine(top1.x(), top1.y(), top2.x(), top2.y())

        if len(path)!=0:
            start = path[0]
            end = path[len(path)-1]
            self.brushColor = Qt.black
            self.pen(painter)
            top = self.graph.listV[start-1]
            painter.drawEllipse(top.x() - Constant.rad/2, top.y() - Constant.rad/2, Constant.rad, Constant.rad)
            top = self.graph.listV[end-1]
            painter.drawEllipse(top.x() - Constant.rad/2, top.y() - Constant.rad/2, Constant.rad, Constant.rad)



        self.update()

    @pyqtSlot()
    def on_click(self):
        self.showdialog()

    @pyqtSlot()
    def clickSaveSettin(self):
        self.d.close()

    def handleInput(self, state):
        if state == Qt.Checked:
            self.isHandle = True
            #self.countParam = 0

    @pyqtSlot()
    def click_info(self):
        infoDialog = QDialog()
        aboutMe = QTextEdit(Constant.info)


        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(aboutMe, 0, 0)
        infoDialog.setLayout(grid)

        infoDialog.resize(200, 200)
        infoDialog.setWindowTitle("Input parametrs")
        infoDialog.setWindowModality(Qt.ApplicationModal)
        infoDialog.exec_()

    @pyqtSlot()
    def click_run(self):
        start = 1
        end = self.graph.size()

        if len(self.selectedTop) == 2:

            top1 = self.selectedTop.pop(1) # type - Top
            top2 = self.selectedTop.pop(0)
            start = top1.getNumber()
            end = top2.getNumber()

            if start > end:
                a = start
                start = end
                end = a

            self.graph.initData()
            self.graph.deystra(start)
            path = self.graph.printPath(start, end, self.graph.parent)  # last top

        else:
            self.graph.initData()
            # закоменченные строки это правка в оригинале были
            # countCom = self.graph.countComponent()
            # self.statusBar().showMessage(str(countCom))

            #self.graph.initData() # можно убрать в метое есть проверка нужна ли инициализация
            #for x in self.graph.beginComponent:
            self.graph.deystra(1)
            path = self.graph.printPath(start, end, self.graph.parent)  # last top



        if len(path) == 1 or len(path) == 0:
            print('Not path')
            self.statusBar().showMessage('Not path')
        else:
            self.brushColor = Qt.red
            painter = QPainter(self.image)
            painter.drawText(QPointF(160, 50), str(start))
            painter.drawText(QPointF(160, 70), str(end))
            self.drawPath(path,painter) # type - List<int>
            self.statusBar().showMessage(str(path)+" = "+str(self.graph.dist[self.graph.size()]))

    # TODO: найти пересекающиеся ребра и восстановить их
    @pyqtSlot()
    def click_del(self):
        if len(self.selectedTop) != 0:
            for x in self.selectedTop:
                self.brushColor = Qt.white
                painter = QPainter(self.image)
                self.pen(painter)
                #clear deleting top
                painter.drawEllipse(x.x() - Constant.rad/2, x.y() - Constant.rad/2, Constant.rad, Constant.rad)

                # clear conection lines
                for rib in x.list:
                    painter.drawLine(rib.to.x(), rib.to.y(), x.x(), x.y())

                    for k in range(self.countParam):
                        painter.eraseRect(QRectF((x.x() + rib.to.x()) / 2 + 5, (x.y() + rib.to.y()) / 2 - 15 , 50, 10*self.countParam))
                painter.eraseRect(QRectF(x.x()-15, x.y()-15, Constant.rad*2, Constant.rad*2))

                # restore adjacent circles
                self.brushColor = Qt.blue
                self.pen(painter)
                for rib in x.list:
                    painter.drawEllipse(rib.to.x() - Constant.rad / 2, rib.to.y() - Constant.rad / 2, Constant.rad, Constant.rad)
                    self.brushColor = Qt.black
                    self.pen(painter)
                    painter.drawText(QPointF(rib.to.x(), rib.to.y()), str(rib.to.getNumber()))

                self.graph.delete(x)
            self.selectedTop.clear()
        else:
            self.graph.deleteAll()
            self.image.fill(Qt.white)
            self.countCom = 0
            self.countCity = 0

        self.initNeed()
        self.update()


    @pyqtSlot()
    def clickOk(self):
        # at first draw tops
        self.d.close()
        if self.countCity == 0:
            self.countCity = 5
        if self.countCom == 0:
            self.countCom = 5
        if self.countParam == 0:
            self.countParam = 1
        if self.countCom > (self.countCity*(self.countCity-1))/2:
            self.statusBar().showMessage('Too many connections')
            return

        painter = QPainter(self.image)
        width = self.width()
        height = self.height()
        flagInside = False

        i = 0
        while i < self.countCity:
            pos = QPointF(random.randint(Constant.rad*2, width-Constant.rad*2), random.randint(Constant.rad*2, height-Constant.rad*2))
            for top in self.graph.getSetV():
                if top.inside(pos):

                    flagInside = True
                    break

            if not flagInside:
                top = Top(pos, self.graph.size() + 1)
                self.graph.add(top)

                self.brushColor = Qt.black
                self.pen(painter)
                painter.drawText(pos, str(top.getNumber()))

                self.brushColor = Qt.blue
                self.pen(painter)
                painter.drawEllipse(top.x() - Constant.rad / 2, top.y() - Constant.rad / 2, Constant.rad, Constant.rad)
                i = i+1

            flagInside = False

        # draw connection
        i = 0
        while i < self.countCom:
            self.brushColor = Qt.green
            self.pen(painter)

            a = random.randint(0, self.graph.size()-1)
            top1 = self.graph.listV[a]  # type - Top
            b = random.randint(0, self.graph.size()-1)
            if a == b:
                if a+1==self.graph.size():
                    b = b - 1
                else:
                    b = b + 1
            top2 = self.graph.listV[b]

            # check for excisting the road
            if not top1.exsitRoad(top2):
                painter.drawLine(top1.x(), top1.y(), top2.x(), top2.y())

                # count parametres
                param = []
                for j in range(self.countParam):
                    param.append(random.randint(1, 100))
                top1.add(top2, param)
                top2.add(top1, param)

                self.brushColor = Qt.black
                self.pen(painter)

                for k in range(self.countParam):
                    p = str(param[k])
                    painter.drawText(QPointF((top1.x() + top2.x()) / 2 + 5, (top1.y() + top2.y()) / 2 - 5 + 20 * k),
                                      p)

                i = i+1

        self.update()


    def autoCheckBox(self, state):
        if state == Qt.Checked:
            self.countCity = random.randint(2,10)
            a = int((self.countCity*(self.countCity-1))/2)
            self.countCom = random.randint(1, a)
            self.countParam = random.randint(0, 3)

    def editCity(self):
        if len(self.countCityF.text())!=0:
            self.countCity = int(self.countCityF.text())

    def editCom(self):
        self.countCom = int(self.countCommunF.text())


    def editParam(self):
        self.countParam = int(self.countParamF.text())

    def center(self):
        position = self.frameGeometry() #get rectangle our app
        cnrScreen = QDesktopWidget().availableGeometry().center() # get the center point on the screen
        position.moveCenter(cnrScreen) # rect put on the center
        self.move(position.topLeft()) # shift app


    # доделать динамическое обновление параметров
    @pyqtSlot()
    def inputToFieldPar(self):
        line = QLineEdit(self.parDial)
        self.parametrs.append(line)
        grid = self.parDial.layout()
        grid.addWidget(line, len(self.parametrs),0)
        line.returnPressed.connect(self.inputToFieldPar)

    @pyqtSlot()
    def saveParam(self):
        self.parDial.close()

    # диалог, где  вручную вводим параметры
    def instalParametDialog(self):
        self.parDial = QDialog()
        self.parametrs = []

        grid = QGridLayout()
        grid.setSpacing(10)
        countPara = self.countParam

        for i in range(countPara):

            line = QLineEdit('0', self.parDial)
            grid.addWidget(line, i+1, 0)
            self.parametrs.append(line)

       # self.parametrs[0].returnPressed.connect(self.inputToFieldPar)

        saveParam = QPushButton("Save", self.parDial)
        grid.addWidget(saveParam, countPara+1, 1)
        saveParam.clicked.connect(self.saveParam)
        self.parDial.setLayout(grid)
        self.parDial.resize(150, 150)
        self.parDial.setWindowTitle("Input parametrs")
        self.parDial.setWindowModality(Qt.ApplicationModal)
        self.parDial.exec_()


    def showdialog(self):
        self.d = QDialog()
        self.countCityF = QLineEdit(self.d)
        self.countCommunF = QLineEdit(self.d)
        self.countParamF = QLineEdit(self.d)
        isHandleInputF = QCheckBox('')
        autoGenC = QCheckBox('Авто')
        ok = QPushButton("ОК", self.d)
        saveSetting = QPushButton("Сохранить", self.d)
        saveSetting.setMaximumSize(ok.width(), ok.height())

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(QLabel('Желаемое количество городов:', self.d), 1, 0)
        grid.addWidget(self.countCityF, 1, 1)
        grid.addWidget(QLabel('Желаемое количество связей', self.d), 2, 0)
        grid.addWidget(self.countCommunF, 2, 1)
        grid.addWidget(QLabel('Желаемое количество параметров', self.d), 3, 0)
        grid.addWidget(self.countParamF, 3,1)
        grid.addWidget(QLabel('Сгенерировать:', self.d), 4,0)
        grid.addWidget(autoGenC, 4, 1)
        grid.addWidget(QLabel('Ручная настройка параметров?', self.d), 5,0)
        grid.addWidget(isHandleInputF, 5,1)
        grid.addWidget(saveSetting, 6,0)
        grid.addWidget(ok, 6, 1)

        ok.clicked.connect(self.clickOk)
        saveSetting.clicked.connect(self.clickSaveSettin)
        autoGenC.stateChanged.connect(self.autoCheckBox)
        isHandleInputF.stateChanged.connect(self.handleInput)
        self.countCityF.editingFinished.connect(self.editCity)
        self.countCommunF.editingFinished.connect(self.editCom)
        self.countParamF.editingFinished.connect(self.editParam)


        self.d.setLayout(grid)
        self.d.resize(150,150)
        self.d.setWindowTitle("Настройка графа")
        self.d.setWindowModality(Qt.ApplicationModal)
        self.d.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())