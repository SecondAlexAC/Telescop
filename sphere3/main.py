import sys
import os
import configparser
import time
import pandas as pd

import colorsys
from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QVBoxLayout, QLabel, QMenu, QPushButton, QWidget, QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QMessageBox, QSlider, QPlainTextEdit, QTextBrowser, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QPixmap, QFont, QAction, QCursor
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QObject, QThread, pyqtSignal, Qt, QEvent

from matplotlib.colors import Normalize
from matplotlib.patches import RegularPolygon, Rectangle
import numpy as np
import matplotlib.cm as cm
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class WorkerPD(QObject):

    stepIncreased = pyqtSignal(int)

    def __init__(self, parent):
        super(WorkerPD, self).__init__()
        self.parentt = parent
        self._step = int(self.parentt.stbord)
        self._isRunning = False
        self._maxSteps = 20

    def task(self):
        self.parentt.btnStopPD.show()
        self.parentt.btnStartPD.hide()
        if not self._isRunning:
            self._isRunning = True
            self._step = int(self.parentt.currentStepPD.value())

        while self._isRunning == True:
            if self._step == int(self.parentt.labord):
                self._step = self.parentt.stbord - 1
            self._step += 1
            self.stepIncreased.emit(self._step)
            time.sleep(-self.parentt.SliderAU.value()/100)

        self._step = self.parentt.currentStepPD.value()
        print("finished...")

    def stop(self):
        self.parentt.btnStopPD.hide()
        self.parentt.btnStartPD.show()
        self._step = self.parentt.currentStepPD.value()
        print(999)
        self._isRunning = False

class WorkerUA(QObject):

    stepIncreased = pyqtSignal(int)

    def __init__(self, parent):
        super(WorkerUA, self).__init__()
        self.parentt = parent
        self._step = int(self.parentt.i)
        self._isRunning = False
        self._maxSteps = 20

    def task(self):
        if not self._isRunning:
            self._isRunning = True
            self._step = int(self.parentt.i)

        while self._isRunning == True:
            if self._step == len(self.parentt.AllItems) - 1:
                self._step = -1
            self._step += 1
            self.stepIncreased.emit(self._step)
            time.sleep(-self.parentt.SliderAU.value()/20)

        self._step = 0
        print("finished...")

    def stop(self):
        self.parentt.buttonrightW.setEnabled(True)
        self.parentt.buttonleftW.setEnabled(True)
        self._step = 0
        self._isRunning = False


class WorkerUAL(QObject):

    stepIncreased = pyqtSignal(int)

    def __init__(self, parent):
        super(WorkerUAL, self).__init__()
        self.parentt = parent
        self._step = int(self.parentt.i)
        self._isRunning = False
        self._maxSteps = 20

    def task(self):
        if not self._isRunning:
            self._isRunning = True
            self._step = int(self.parentt.i)

        while self._isRunning == True:
            if self._step == 0:
                self._step = len(self.parentt.AllItems)
            self._step -= 1
            self.stepIncreased.emit(self._step)
            time.sleep(-self.parentt.SliderAU.value()/20)

        self._step = 0
        print("finished...")

    def stop(self):
        self.parentt.buttonrightW.setEnabled(True)
        self.parentt.buttonleftW.setEnabled(True)
        self._step = 0
        self._isRunning = False

def drowA(parent, st):
        '''
        sipm = []
        ch = []
        znach = []
        X = []
        Y = []

        o = parent.df[parent.df['Event'] == int(parent.event)]

        for sp in parent.coords['SIPM'].unique().tolist():

            for i in parent.coords[parent.coords['SIPM'] == sp]['ch'].unique().tolist():
                sipm.append(sp)
                ch.append(i)
                znach.append(max(o[(o['SIPM'] == sp) & (o['ch'] == i)].iloc[0, 5+st:5+st+1]))'''
        
        znach = []

        for i in list(parent.df.columns):
            if parent.df[i].tolist()[st] != 0:
                print(i, parent.df[i].tolist()[st])
            #print(i, parent.df[i].tolist()[st])
            znach.append(parent.df[i].tolist()[st])
        print(parent.df.index.max())
        cmap = cm.get_cmap(parent.theme)

        znach.append(parent.nowAmax)

        norm = Normalize(vmin=min(parent.df.min()), vmax=max(parent.df.max()))
        rgba_values = cmap(norm(znach))
        for i in range(len(parent.buttons)):
            parent.buttons[i].rgbcol = rgba_values[i]
            h, l, s = colorsys.rgb_to_hls(rgba_values[i][0], rgba_values[i][1], rgba_values[i][2])
            h = (h + 0.1) % 1
            s = 0.5
            l = 1
            parent.buttons[i].textcol = matplotlib.colors.rgb2hex(colorsys.hls_to_rgb(h, s, l))
            if (sum(rgba_values[i]) - 1) / 3 < 0.5:
                parent.buttons[i].textcol = matplotlib.colors.rgb2hex((1, 1, 1))
            else:
                parent.buttons[i].textcol = matplotlib.colors.rgb2hex((0, 0, 0))

            #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))

            parent.buttons[i].col = matplotlib.colors.rgb2hex(rgba_values[i])
            parent.buttons[i].setStyleSheet("QPushButton {background-color: "+ parent.buttons[i].col +" ; color: White;  border-radius: "+str(int(parent.buttons[i].frameSize().width()/2))+"px; }"
                                        "QPushButton:pressed {background-color:#b784a7)} ;")         
            parent.buttons[i].znach = znach[i]
        '''
        znach.pop()

        for Si, c, col, z in zip(sipm, ch, rgba_values, znach):
            for i in parent.buttons:   
                if i.sipm == Si and i.ch == c:
                    i.rgbcol = col

                    #h, l, s = colorsys.rgb_to_hls(col[0], col[1], col[2])
                    #h = (h + 0.1) % 1
                    #s = 0.5
                    #l = 1
                    #i.textcol = matplotlib.colors.rgb2hex(colorsys.hls_to_rgb(h, s, l))

                    if (sum(col) - 1) / 3 < 0.5:
                        i.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
                    else:
                        i.textcol = matplotlib.colors.rgb2hex((0, 0, 0))

                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
                    i.col = matplotlib.colors.rgb2hex(col)
                    i.setStyleSheet("QPushButton {background-color: "+ i.col +" ; color: White;  border-radius: "+str(int(i.frameSize().width()/2))+"px; }"
                                        "QPushButton:pressed {background-color:#b784a7)} ;")         
                    i.znach = z
                    i.setText(f'{z}\nSIPM:{i.sipm}\nPin:{i.ch}')

                    break
        print(i)'''
        parent.newSize()

def drow(parent):
        '''
        sipm = []
        ch = []
        znach = []
        X = []
        Y = []

        print(parent.stbord)

        o = parent.df[parent.df['Event'] == int(parent.event)]


        for sp in parent.coords['SIPM'].unique().tolist():

            for i in parent.coords[parent.coords['SIPM'] == sp]['ch'].unique().tolist():
                sipm.append(sp)
                ch.append(i)
                znach.append(max(o[(o['SIPM'] == sp) & (o['ch'] == i)].iloc[0, 5+parent.stbord:5+parent.labord+1]))
        '''
        znach = []

        for i in list(parent.df.columns):
            d = parent.df[i].tolist()
            k = max(d)
            
            print(i, sum(d[d.index(k)-10:d.index(k)+11]))
            znach.append(sum(d[d.index(k)-10:d.index(k)+11]))

        cmap = cm.get_cmap(parent.theme)

        print(parent.df.index.min())
        print(parent.df.index.max())

        
        norm = Normalize(vmin=min(znach), vmax=max(znach))
        
        rgba_values = cmap(norm(znach))

        for i in range(len(parent.buttons)):
            parent.buttons[i].rgbcol = rgba_values[i]
            h, l, s = colorsys.rgb_to_hls(rgba_values[i][0], rgba_values[i][1], rgba_values[i][2])
            h = (h + 0.1) % 1
            s = 0.5
            l = 1
            parent.buttons[i].textcol = matplotlib.colors.rgb2hex(colorsys.hls_to_rgb(h, s, l))
            if (sum(rgba_values[i]) - 1) / 3 < 0.5:
                parent.buttons[i].textcol = matplotlib.colors.rgb2hex((1, 1, 1))
            else:
                parent.buttons[i].textcol = matplotlib.colors.rgb2hex((0, 0, 0))

            #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
            parent.buttons[i].col = matplotlib.colors.rgb2hex(rgba_values[i])
            parent.buttons[i].setStyleSheet("QPushButton {background-color: "+ parent.buttons[i].col +" ; color: White;  border-radius: "+str(int(parent.buttons[i].frameSize().width()/2))+"px; }"
                                        "QPushButton:pressed {background-color:#b784a7)} ;")         
            parent.buttons[i].znach = znach[i]
        '''

        print(max(znach))

        for Si, c, col, z in zip(sipm, ch, rgba_values, znach):
            for i in parent.buttons:   
                if i.sipm == Si and i.ch == c:
                    i.rgbcol = col

                    #h, l, s = colorsys.rgb_to_hls(col[0], col[1], col[2])
                    #h = (h + 0.1) % 1
                    #s = 0.5
                    #l = 1
                    #i.textcol = matplotlib.colors.rgb2hex(colorsys.hls_to_rgb(h, s, l))

                    if (sum(col) - 1) / 3 < 0.5:
                        i.textcol = matplotlib.colors.rgb2hex((1, 1, 1))
                    else:
                        i.textcol = matplotlib.colors.rgb2hex((0, 0, 0))

                    #i.textcol = matplotlib.colors.rgb2hex((s - r, s - g, s - b))
                    i.col = matplotlib.colors.rgb2hex(col)
                    i.setStyleSheet("QPushButton {background-color: "+ i.col +" ; color: White;  border-radius: "+str(int(i.frameSize().width()/2))+"px; }"
                                        "QPushButton:pressed {background-color:#b784a7)} ;")         
                    i.znach = z
                    i.setText(f'{z}\nSIPM:{i.sipm}\nPin:{i.ch}')

                    break
        parent.nowAmax = max(znach)'''
        parent.newSize()

def Data(app, filename):
    f = open(app.directory_of_ustanovki + '/' + filename)
    df = pd.read_csv(app.directory_of_ustanovki + '/' + filename, encoding="windows-1251")
    df = df.dropna()
    #df['SIPM'] = df["SIPM"].astype(int)
    #df['ch'] = df["ch"].astype(int)
    print(df.head())
    return df

class VisualWindow(QMainWindow):

    resized = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parentt = parent

        self.setWindowTitle("Settings")
        self.setMinimumWidth(650)
        self.setMinimumHeight(400)
        self.setFixedSize(390, 200)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resized.connect(self.newSize)
        
        self.sizeButtons = QDoubleSpinBox(self)
        self.sizeButtons.move(10, 5)
        self.sizeButtons.setValue(float(self.parentt.settings.get('Set_SIMPS', 'buttonsHW')))
        self.sizeButtons.valueChanged.connect(self.changeSizeButtons)
        self.sizeButtons.setMinimum(0.1)
        self.sizeButtons.setFixedSize(60, 25)

        self.sizeButtonsT = QLabel('size of pixel', self)
        self.sizeButtonsT.setFixedSize(70, 25)
        self.sizeButtonsT.move(75, 5)

        self.spinX = QDoubleSpinBox(self)
        self.spinX.move(10, 30)
        self.spinX.setValue(float(self.parentt.settings.get('Set_SIMPS', 'moveX'))) 
        self.spinX.valueChanged.connect(self.changeSpinX)
        self.spinX.setMinimum(0.1)
        self.spinX.setFixedSize(60, 25)

        self.spinXT = QLabel('X-distance between pixels', self)
        self.spinXT.setFixedSize(170, 25)
        self.spinXT.move(75, 30)

        self.spinY = QDoubleSpinBox(self)
        self.spinY.move(10, 55)
        self.spinY.setValue(float(self.parentt.settings.get('Set_SIMPS', 'moveY'))) 
        self.spinY.valueChanged.connect(self.changeSpinY)
        self.spinY.setMinimum(0.1)
        self.spinY.setFixedSize(60, 25)

        self.spinYT = QLabel('Y-distance between pixels', self)
        self.spinYT.setFixedSize(170, 25)
        self.spinYT.move(75, 55)

        self.moveX = QSpinBox(self)
        self.moveX.move(10, 80)
        self.moveX.setMinimum(-10000)
        self.moveX.setValue(int(self.parentt.settings.get('Set_SIMPS', 'movingX'))) 
        self.moveX.valueChanged.connect(self.changeMovingX)
        self.moveX.setFixedSize(60, 25)

        self.moveXT = QLabel('X-shift', self)
        self.moveXT.setFixedSize(170, 25)
        self.moveXT.move(75, 80)
        
        self.moveY = QSpinBox(self)
        self.moveY.move(10,105)
        self.moveY.setMinimum(-10000)
        self.moveY.setValue(int(self.parentt.settings.get('Set_SIMPS', 'movingY'))) 
        self.moveY.valueChanged.connect(self.changeMovingY)
        self.moveY.setFixedSize(60, 25)

        self.moveYT = QLabel('Y-shift', self)
        self.moveYT.setFixedSize(170, 25)
        self.moveYT.move(75, 105)

        self.setDefultsettings = QPushButton('Load default setting', self)
        self.setDefultsettings.move(10, 160)
        self.setDefultsettings.setFixedSize(180, 30)
        self.setDefultsettings.clicked.connect(self.setDefultSETTINGS)
        
        self.saveSettingsInFILE = QPushButton('save settings in file', self)
        self.saveSettingsInFILE.move(200, 160)
        self.saveSettingsInFILE.setFixedSize(180, 30)
        self.saveSettingsInFILE.clicked.connect(self.saveSettingsInFile)

        self.HSznach = QCheckBox(self)
        self.HSznach.toggled.connect(self.HSZNACH)
        self.HSznach.setChecked(False if self.parentt.settings.get('Set_HStext', 'HZnach') == '1' else True)
        #self.HSznach.setFixedSize(25, 25) 
        self.HSznach.move(250, 5)

        self.HSznachT = QLabel('hide A max', self)
        self.HSznachT.setFixedSize(170, 25)
        self.HSznachT.move(275, 5)

        self.HSsipm = QCheckBox(self)
        self.HSsipm.toggled.connect(self.HSSIPM)
        self.HSsipm.setChecked(False if self.parentt.settings.get('Set_HStext', 'HSipm') == '1' else True) 
        self.HSsipm.move(250, 30)


        self.HSsipmT = QLabel('hide SIPM numbers', self)
        self.HSsipmT.setFixedSize(170, 25)
        self.HSsipmT.move(275, 30)
        self.HSsipm.hide()
        self.HSsipmT.hide()

        self.HSchan = QCheckBox(self)
        self.HSchan.toggled.connect(self.HSCHAN)
        self.HSchan.setChecked(False if self.parentt.settings.get('Set_HStext', 'HChan') == '1' else True) 
        self.HSchan.move(250, 55)

        self.HSchanT = QLabel('hide pixel numbers', self)
        self.HSchanT.setFixedSize(170, 25)
        self.HSchanT.move(275, 55)

        self.stb = QSpinBox(self)
        self.stb.setMinimum(0)
        self.stb.setMaximum(1023)
        self.stb.setValue(self.parentt.stbord)
        self.stb.valueChanged.connect(self.changebord)
        self.stb.setFixedSize(60, 25)
        self.stb.move(100, 130)

        self.stbT = QLabel('find A-max from', self)
        self.stbT.move(10, 130)

        self.lab = QSpinBox(self)
        self.lab.setMinimum(0)
        self.lab.setMaximum(1023)
        self.lab.setValue(self.parentt.labord)
        self.lab.valueChanged.connect(self.changebord)
        self.lab.setFixedSize(60, 25)
        self.lab.move(180, 130)

        self.labT = QLabel('to', self)
        self.labT.move(165, 130)
        self.labT.setFixedSize(25, 25)

        self.theme = QComboBox(self)
        self.theme.addItem(self.parentt.settings.get('Set_theme', 'theme'))
        self.theme.addItems(['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'])
        self.theme.activated.connect(self.changetheme)
        self.theme.setFixedSize(80, 25)
        self.theme.move(230, 85)

        self.themeT = QLabel(' theme', self)
        self.themeT.move(310, 85)
        self.themeT.setFixedSize(50, 25)

        self.saveDir = QPushButton('save dir', self)
        self.saveDir.move(245, 120)
        self.saveDir.setFixedSize(60, 30)
        self.saveDir.clicked.connect(self.savedir)
    
        self.clsaveDir = QPushButton('clear saved\ndir', self)
        self.clsaveDir.move(310, 120)
        self.clsaveDir.setFixedSize(60, 30)
        self.clsaveDir.clicked.connect(self.clearsaveddir)

    def savedir(self):
        f = open('config.ini', 'r')
        d = f.readlines()
        f.close()
        d[len(d)-1] = f'dir = {self.parentt.directory_of_ustanovki}'
        f = open('config.ini', 'w')
        for i in d:
            f.write(i)
        f.close()

    def clearsaveddir(self):
        f = open('config.ini', 'r')
        d = f.readlines()
        f.close()
        d[len(d)-1] = f'dir = None'
        f = open('config.ini', 'w')
        for i in d:
            f.write(i)
        f.close()

    def changetheme(self):
        self.parentt.theme = self.theme.currentText()
        self.parentt.settings.set('Set_theme', 'theme', self.theme.currentText())
        self.parentt.changetheme()

    def changebord(self):
        if self.stb.value() < self.lab.value():
            self.parentt.stbord = self.stb.value()
            self.parentt.ii = self.stb.value()
            self.parentt.labord = self.lab.value()
            self.parentt.settings.set('Set_bord', 'st', f'{self.stb.value()}')
            self.parentt.settings.set('Set_bord', 'la', f'{self.lab.value()}')
            self.parentt.setEventAndDrow()

    def HSZNACH(self):
        if self.HSznach.isChecked():
            self.parentt.HZnach = False
        else:
            self.parentt.HZnach = True
        self.parentt.settings.set('Set_HStext', 'HZnach', f'{"1" if self.parentt.HZnach else "0"}')
        self.parentt.newSize()

    def HSSIPM(self):
        if self.HSsipm.isChecked():
            self.parentt.HSipm = False
        else:
            self.parentt.HSipm = True
        self.parentt.settings.set('Set_HStext', 'HSipm', f'{"1" if self.parentt.HSipm else "0"}')
        self.parentt.newSize()

    def HSCHAN(self):
        if self.HSchan.isChecked():
            self.parentt.HChan = False
        else:
            self.parentt.HChan = True
        self.parentt.settings.set('Set_HStext', 'HChan', f'{"1" if self.parentt.HChan else "0"}')
        self.parentt.newSize()

    def changeSpinX(self):
        self.parentt.settings.set('Set_SIMPS', 'moveX', f'{self.spinX.value()}')
        self.parentt.newSize()
    
    def changeSpinY(self):
        self.parentt.settings.set('Set_SIMPS', 'moveY', f'{self.spinY.value()}')
        self.parentt.newSize()

    def changeSizeButtons(self):
        self.parentt.settings.set('Set_SIMPS', 'buttonsHW', f'{self.sizeButtons.value()}')
        self.parentt.newSize()

    def changeMovingX(self):
        self.parentt.settings.set('Set_SIMPS', 'movingX', f'{self.moveX.value()}')
        self.parentt.newSize()

    def changeMovingY(self):
        self.parentt.settings.set('Set_SIMPS', 'movingY', f'{self.moveY.value()}')
        self.parentt.newSize()

    def setDefultSETTINGS(self):
        self.parentt.settings = self.parentt.DefultSettings()
        self.sizeButtons.setValue(float(self.parentt.settings.get('Set_SIMPS', 'buttonsHW')))
        self.spinX.setValue(float(self.parentt.settings.get('Set_SIMPS', 'moveX'))) 
        self.spinY.setValue(float(self.parentt.settings.get('Set_SIMPS', 'moveY')))
        self.moveX.setValue(int(self.parentt.settings.get('Set_SIMPS', 'movingX'))) 
        self.moveY.setValue(int(self.parentt.settings.get('Set_SIMPS', 'movingY'))) 
        self.HSznach.setChecked(False if self.parentt.settings.get('Set_HStext', 'HZnach') == '1' else True)
        self.HSsipm.setChecked(False if self.parentt.settings.get('Set_HStext', 'HSipm') == '1' else True) 
        self.HSchan.setChecked(False if self.parentt.settings.get('Set_HStext', 'HChan') == '1' else True)
        self.stb.setValue(int(self.parentt.settings.get('Set_bord', 'st')))
        self.lab.setValue(int(self.parentt.settings.get('Set_bord', 'la')))
        self.theme.clear()
        self.theme.addItem(self.parentt.settings.get('Set_theme', 'theme'))
        self.theme.addItems(['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'])
        self.parentt.theme = self.parentt.settings.get('Set_theme', 'theme')
        self.parentt.changetheme()
        self.parentt.newSize()

    def saveSettingsInFile(self):
        self.parentt.saveSettingsInFile()

    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        self.parentt.vid = False
        event.accept()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(VisualWindow, self).resizeEvent(event)
    
    def newSize(self):
        #self.drow.move(self.centralwidget.frameSize().width() // 2 - 50, 30)
        print(99)
        #self.events.move(self.centralwidget.frameSize().width() - 75, 10)

class App(QMainWindow):

    resized = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        global buttonsHW, moveX, moveY

        if os.path.exists('config.ini') is not True:
            print(9)
            config = self.DefultSettings()
            with open('config.ini', 'w') as config_file:
                config.write(config_file)

        
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.settings = config

        pos = QCursor.pos()
        self.mouseX = pos.x()
        self.mouseY = pos.y()

        self.nowAmax = 0
        self.ff = False
        self.qs = []

        self.setWindowTitle("SPHERE-2")
        self.setMinimumWidth(650)
        self.setMinimumHeight(450)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resized.connect(self.newSize)

        self.buttons = []
        coords = pd.read_csv('sphere2_mosaic_pmt_coords.txt', sep='\s+')
        print(coords.head())
        #self.theme.addItems(['magma', 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'])
        for x, y, ch in zip(coords['x'], coords['y'], coords['ch']):
            but = QPushButton(f'{ch}', self)
            #but.sipm = sipm
            but.x = x
            but.y = -y
            but.ch = ch-1
            but.f = False
            but.move(int(x*10), int(y*10))
            but.textcol = 'White'
            but.znach = None
            but.clicked.connect(self.openAdditWin)
            self.sipm = 'None'
            but.win = []
            #if but.sipm == 2:
            but.col = '#1f75fe'
            #else:
            #but.col = '#c35831'
            self.buttons.append(but)
        self.coords = coords

        self.ii = 0 
        
        self.nowevent = QLabel("Event", self)
        self.nowevent.hide()

        self.nowdir = QLabel("File", self)
        self.nowdir.setFixedSize(500, 25)
        self.nowdir.hide()

        self.time = QLabel("Time", self)
        self.time.setFixedSize(150, 10)
        self.time.hide()

        self.events = QComboBox(self)
        self.events.move(10, 30)
        self.events.activated.connect(self.changeEventsfromcombobox)
        self.events.hide()
        self.events.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        #self.theme = QComboBox(self)
        #self.theme.addItem(self.settings.get('Set_theme', 'theme'))
        #self.theme.addItems(['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'])
        #self.theme.activated.connect(self.changetheme)
        #self.theme.hide()

        self.theme = self.settings.get('Set_theme', 'theme')

        self.buttonleft = QPushButton('<-', self)
        self.buttonleft.clicked.connect(self.changeEventsfromLBut)
        self.buttonleft.setFixedSize(40, 30)
        self.buttonleft.hide()

        self.buttonright = QPushButton('->', self)
        self.buttonright.clicked.connect(self.changeEventsfromRBut)
        self.buttonright.setFixedSize(40, 30)
        self.buttonright.hide()

        self.buttonstop = QPushButton('Stop', self)
        #self.buttonright.clicked.connect(self.stop)
        self.buttonstop.hide()
        self.buttonstop.setFixedSize(40, 30)

        self.buttonrightW = QPushButton('>>', self)
        #self.buttonrightW.clicked.connect(self.changeEventsfromRBut)
        self.buttonrightW.setFixedSize(40, 30)
        self.buttonrightW.hide()

        self.buttonleftW = QPushButton('<<', self)
        #self.buttonleftW.clicked.connect(self.changeEventsfromLBut)
        self.buttonleftW.setFixedSize(40, 30)
        self.buttonleftW.hide()

        #self.showText.toggled.connect(self.onClicked)
        self.vid = False

        self.hideWidg = QCheckBox(self)
        self.hideWidg.move(90, 120)
        self.hideWidg.toggled.connect(self.changeHide)
        self.hideWidg.hide()
        
        self.HZnach = True if self.settings.get('Set_HStext', 'HZnach') == '1' else False
        self.HSipm = True if self.settings.get('Set_HStext', 'HSipm') == '1' else False
        self.HChan = True if self.settings.get('Set_HStext', 'HChan') == '1' else False

        self.stbord = int(self.settings.get('Set_bord', 'st'))
        self.ii = int(self.settings.get('Set_bord', 'st'))
        
        self.labord = int(self.settings.get('Set_bord', 'la'))

        self.intervalT = QLabel("interval", self)
        self.intervalT.hide()

        

        self.AllpInEvent = QPushButton('All pixels in event', self)
        self.AllpInEvent.move(50, 100)
        self.AllpInEvent.clicked.connect(self.AllPixelInEvent)
        self.AllpInEvent.hide()

        self.openASmatplot = QPushButton('event in plt\nwindow', self)
        self.openASmatplot.move(100, 100)
        self.openASmatplot.clicked.connect(self.openEventInMAatplot)
        self.openASmatplot.setFixedSize(100, 35)
        self.openASmatplot.hide()

        self.eventt = ''
        self.i = 0

        #

        self.btnStartAU = QPushButton('>', self)
        self.btnStartAU.move(90, 270)
        self.btnStartAU.setFixedSize(25, 25)
        #self.btnStartAU.hide()
        self.btnStartAU.hide()
        self.btnStopAU = QPushButton('||', self)
        self.btnStopAU.move(90, 270)
        self.btnStopAU.setFixedSize(25, 25)
        self.btnStopAU.hide()
        self.currentStepAU = QSpinBox(self)
        self.currentStepAU.move(30, 270)
        self.currentStepAU.hide()
    
        self.threadAU = QThread()
        self.threadAU.start()

        self.workerAU = WorkerUA(self)
        self.workerAU.moveToThread(self.threadAU)
        self.workerAU.stepIncreased.connect(self.currentStepAU.setValue)

        self.buttonstop.clicked.connect(lambda: self.workerAU.stop())
        self.buttonrightW.clicked.connect(self.workerAU.task)
        
        self.currentStepAU.valueChanged.connect(self.AU)


        self.threadAUL = QThread()
        self.threadAUL.start()

        self.workerAUL = WorkerUAL(self)
        self.workerAUL.moveToThread(self.threadAUL)
        self.workerAUL.stepIncreased.connect(self.currentStepAU.setValue)

        self.buttonstop.clicked.connect(lambda: self.workerAUL.stop())
        self.buttonleftW.clicked.connect(self.workerAUL.task)
        
        #self.currentStepAU.valueChanged.connect(self.AU)


        self.SliderAU = QSlider(self)
        self.SliderAU.setOrientation(Qt.Orientation.Horizontal) 
        self.SliderAU.setGeometry(30, 40, 100, 25)
        self.SliderAU.move(50, 50)
        self.SliderAU.setMinimum(-200)
        self.SliderAU.setMaximum(-10)
        self.SliderAU.hide()
        #SliderAU.valueChanged[int].connect(self.changeValue)

        self.btnStartPD = QPushButton('>', self)
        self.btnStartPD.move(60, 270)
        self.btnStartPD.setFixedSize(25, 25)
        self.btnStartPD.hide()
        #self.btnStartAU.hide()
        self.btnStopPD = QPushButton('||', self)
        self.btnStopPD.move(60, 270)
        self.btnStopPD.setFixedSize(25, 25)
        self.btnStopPD.hide()
        self.currentStepPD = QSpinBox(self)
        self.currentStepPD.setMinimum(0)
        self.currentStepPD.setMaximum(1025)
        self.currentStepPD.move(10, 270)
        self.currentStepPD.setFixedSize(50, 25)
        self.currentStepPD.hide()

        self.reference = False
    
        self.threadPD = QThread()
        self.threadPD.start()

        self.workerPD = WorkerPD(self)
        self.workerPD.moveToThread(self.threadPD)
        self.workerPD.stepIncreased.connect(self.currentStepPD.setValue)

        self.btnStopPD.clicked.connect(lambda: self.workerPD.stop())
        self.btnStartPD.clicked.connect(self.workerPD.task)
        
        self.currentStepPD.setValue(int(self.settings.get('Set_bord', 'st')))
        self.currentStepPD.valueChanged.connect(self.PD)
        

        #self.finished.connect(self.stop_thread)
        
        self.newRegim = QPushButton("Change Mode", self)
        self.newRegim.move(40, 40)
        self.newRegim.hide()
        self.newRegim.clicked.connect(self.openNewRegim)

        self.isopenNewRegim = False
        self._createMenuBar()
        self.i = -1

        self.directory_of_ustanovki = 'None'
        if self.settings.get('Dir', 'dir') != 'None':
            print(self.settings.get('Dir', 'dir'))
            if os.path.isdir(self.settings.get('Dir', 'dir')):
                self.directory_of_ustanovki = str(self.settings.get('Dir', 'dir'))
                #self.directorynameText.setText(f'dir: {self.directory_of_ustanovki}')
                #self.openingFile(fname)
                self.AllItems = os.listdir(self.settings.get('Dir', 'dir'))
                self.showWidgets()
                self.showNug()
                self.btnStopAU.hide()
                self.events.clear()
                self.events.addItems([str(i) for i in self.AllItems])
                self.i = 0
                self.nowdir.setText(f'Dir: {self.directory_of_ustanovki}')
                self.changeEventsfromcombobox()
            else:
                QMessageBox.about(self, "Error", "The directory with the name specified in the file does not exist")



    def openNewRegim(self):
        if self.workerAU._isRunning:
            print('Cantt')
        elif self.workerPD._isRunning:
            print(9)
        elif self.isopenNewRegim:
            print(9)
            self.isopenNewRegim = False
            #self.showNug()
            self.btnStopPD.hide()
            self.btnStartPD.hide()
            self.btnStopAU.hide()
            self.currentStepPD.hide()
            self.buttonleftW.setEnabled(True)
            self.buttonrightW.setEnabled(True)
            self.buttonleft.setEnabled(True)
            self.buttonright.setEnabled(True)
        else:
            print(10)
            self.isopenNewRegim = True
            self.btnStartAU.hide()
            self.btnStopAU.hide()
            self.buttonleftW.setEnabled(False)
            self.buttonrightW.setEnabled(False)
            self.buttonleft.setEnabled(False)
            self.buttonright.setEnabled(False)
            self.btnStartPD.show()
            self.btnStopPD.hide()
            self.currentStepPD.show()
            #self.hideNug()
        print(self.isopenNewRegim)

    def PD(self):
        drowA(self, self.currentStepPD.value())
        print(self.currentStepPD.value())
        
    def AU(self):
        self.buttonrightW.setEnabled(False)
        self.buttonleftW.setEnabled(False)
        self.i = self.currentStepAU.value()
        self.eventt = self.AllItems[self.i]
        self.setEventAndDrow()
        #self.changeEventsfromRBut()

    def AllPixelInEvent(self):
        self.qs.append(Grafic(self))
        self.qs[len(self.qs) - 1].show()


    def openEventInMAatplot(self):
        print(100)
        ch = []
        znach = []
        X = []
        Y = []
        print(self.df)
        self.df
        for i in self.coords['ch'].unique():
            X.append(self.coords[self.coords['ch'] == i]['x'].unique()[0])
            Y.append(self.coords[self.coords['ch'] == i]['y'].unique()[0])
            d = self.df[str((int(i) - 1))].tolist()
            k = max(d)
            ch.append(str((int(i) - 1)))
            znach.append(sum(d[d.index(k)-10:d.index(k)+11]))

        cmap = cm.get_cmap(self.theme)
        fig, ax = plt.subplots(1, 1)
        norm = Normalize(vmin=min(znach), vmax=max(znach))
        rgba_values = cmap(norm(znach))

        print(X, Y, znach)

        ax.set_aspect('equal')
        print(len(Y), len(Y), len(ch) ,len(rgba_values))
        for x, y, c, col, z in zip(X, Y, ch, rgba_values, znach):
            hex = RegularPolygon((x, y), numVertices=6, radius=20, 
                orientation=np.radians(60), 
                facecolor=col, alpha=0.9, edgecolor=col)
            
            if (sum(col) - 1) / 3 < 0.5:
                t = (1, 1, 1)
            else:
                t =(0, 0, 0)
            ax.add_patch(hex)
            ax.text(x, y, f"{z}", ha ='center',
            va ='center', size = 10, color=t)

        ax.scatter(-15, -15, alpha=0.0)
        #ax.get_xaxis().set_visible(False)
        #ax.get_yaxis().set_visible(False)
        plt.subplots_adjust(left=0, bottom=0, right=1, top=0.9)
        plt.axis('off')
        plt.show()

    def changeHide(self):
        if self.hideWidg.isChecked():
            self.hideWidgets()
        else:
            self.showWidgets()

    def saveSettingsInFile(self):
        with open('config.ini', 'w') as config_file:
            self.settings.write(config_file)

    def openAdditWin(self):
        if self.eventt == "":
            return None
        
        b = self.sender()
        print(b.f)
        if not b.f:
            b.win.append(Chan(b, self))
            b.win[-1].show()
            b.f = True

    def DefultSettings(self):
        config = configparser.ConfigParser()
        config.add_section('Set_SIMPS')
        config.set('Set_SIMPS', 'buttonsHW', '13.5')
        config.set('Set_SIMPS', 'moveX', '43.0')
        config.set('Set_SIMPS', 'moveY', '43.0')
        config.set('Set_SIMPS', 'movingX', '0')
        config.set('Set_SIMPS', 'movingY', '1')
        config.add_section('Set_theme')
        config.set('Set_theme', 'theme', 'Blues')
        config.add_section('Set_HStext')
        config.set('Set_HStext', 'HZnach', '1')
        config.set('Set_HStext', 'HSipm', '1')
        config.set('Set_HStext', 'HChan', '1')
        config.add_section('Set_bord')
        config.set('Set_bord', 'st', '450')
        config.set('Set_bord', 'la', '610')
        config.add_section('Dir')
        config.set('Dir', 'dir', 'None')

        return config

    def changetheme(self):
        if self.eventt != "":
            drow(self)

    def SavePng(self):
        if self.eventt != "":

            dialog = QFileDialog()
            for btn in dialog.findChildren(QPushButton):
                print(btn.text())
                print(888)
                if btn.text() == "Открыть":
                    btn.setText("Remove")
            print(000)
            dialog.setNameFilter('Text File (*.txt)')
            dialogSuccess = dialog.exec()



            if dialogSuccess:
                fileLocation = dialog.selectedFiles()[0]
                print(fileLocation)
        else: 
            QMessageBox.about(self, "Error", "Open file to save event")

    def OpenF(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        
        if fname[0] != '':
            self.openingFile(fname[0])
        else:
            return None
        
    def openingFile(self, name):
        self.df = Data(name)

        if type(self.df) == int:
            QMessageBox.about(self, "Error", "Error at the file opening stage")
            return None
        
        if self.df.empty :
            QMessageBox.about(self, "Error", "The data file is empty")
            return None

        self.hideWidg.show()
        self.SliderAU.show()
        #self.btnStartPD.show()
        #self.currentStepPD.show()
        self.showWidgets()
        self.addItemsToEvents()
        s = 0
        for i in range(len(name)):
            if name[i] == "/":
                s = i
        print('-----', s)
        self.nowdir.setText(f"File Name {name[s+1:]}")
        self.AllItems = [self.events.itemText(i) for i in range(self.events.count())]
        self.i = self.events.currentIndex()
        self.changeEventsfromcombobox()

    def addItemsToEvents(self):
        self.events.clear()
        self.events.addItems([str(i) for i in self.df['Event'].unique()])

    def hideNug(self):
        self.buttonright.hide()
        self.buttonleft.hide()
        self.btnStartAU.hide()
        self.btnStopAU.hide()
        self.SliderAU.hide()

    def showNug(self):
        self.buttonright.show()
        self.buttonleft.show()
        self.btnStopAU.show()
        self.SliderAU.show()
        

    def hideWidgets(self):
        self.newRegim.hide()
        self.openASmatplot.hide()
        self.AllpInEvent.hide()
        self.intervalT.hide()
        self.time.hide()
        self.nowevent.hide()
        self.nowdir.hide()
        self.events.hide()
        self.events.hide()
        self.buttonleft.hide()
        self.buttonright.hide()
        self.buttonstop.hide()
        self.buttonleftW.hide()
        self.buttonrightW.hide()


    def showWidgets(self):
        self.newRegim.show()
        self.openASmatplot.show()
        self.AllpInEvent.show()
        self.intervalT.show()
        self.time.show()
        self.nowevent.show()
        self.nowdir.show()
        self.events.show()
        self.events.show()
        self.buttonleft.show()
        self.buttonright.show()
        self.buttonstop.show()
        self.buttonleftW.show()
        self.buttonrightW.show()

    def changeEventsfromLBut(self):
        if self.i == 0:
            self.i = len(self.AllItems)
        self.i = self.i - 1
        self.workerAU._step = int(self.i)
        self.eventt = self.AllItems[self.i]
        self.events.setCurrentIndex(self.i)
        self.setEventAndDrow()

    def changeEventsfromRBut(self):
        if self.i == len(self.AllItems) - 1:
            self.i = -1
        self.i += 1
        self.workerAU._step = int(self.i)
        print('6666', self.i)
        self.eventt = self.AllItems[self.i]
        self.events.setCurrentIndex(self.i)
        self.setEventAndDrow()

    def changeEventsfromcombobox(self):
        self.eventt = self.events.currentText()
        self.i = self.events.currentIndex()
        self.workerAU._step = int(self.i)
        #self.eventt = self.events.currentText()
        #self.nowevent.setText(f"Event {self.eventt}")
        #print(self.eventt)
        #print(self.i)
        self.setEventAndDrow()
        
    def setEventAndDrow(self):
        #print(self.df.head())
        #self.events.setCurrentText(self.eventt)
        #self.eventt = self.AllItems[self.i]
        self.df = Data(self, self.eventt)
        
        self.nowevent.setText(f"Event {self.i}")
        
        #self.nowtime = self.df[self.df['Event'] == int(self.eventt)]['Time'].unique()[0]
        #self.time.setText(f'Time {self.nowtime}')
        #self.intervalT.setText(f'interval {self.stbord} - {self.labord}')
        self.currentStepPD.setValue(int(self.settings.get('Set_bord', 'st')))
        print(self.i)
        drow(self)

    def _createMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = QMenu("&Directory", self)
        menuBar.addMenu(fileMenu)
        self.openFile = QAction("&Open...", self)
        #self.saveasPng = QAction("&Save as PNG", self)

        self.openFile.triggered.connect(self.OpenDir)
        #self.saveasPng.triggered.connect(self.SavePng)

        fileMenu.addAction(self.openFile)
        #fileMenu.addAction(self.saveasPng)

        editMenu = menuBar.addMenu("&Settings")
        self.setVisual = QAction("&SetVisual...", self)
        self.setVisual.triggered.connect(self.openVisualwin)
        editMenu.addAction(self.setVisual)

        helpMenu = menuBar.addMenu("&Help")
        self.sprafka = QAction("&Reference...", self)
        self.sprafka.triggered.connect(self.openReference)
        helpMenu.addAction(self.sprafka)

    def openReference(self):
        if self.reference == False:
            self.reference = True
            self.ref = Reference(self)
            self.ref.show()

    def newSize(self):
        buttonsHW = float(self.settings.get('Set_SIMPS', 'buttonsHW'))
        moveX = float(self.settings.get('Set_SIMPS', 'moveX'))
        moveY = float(self.settings.get('Set_SIMPS', 'moveY'))
        movingX = int(self.settings.get('Set_SIMPS', 'movingX'))
        movingY = int(self.settings.get('Set_SIMPS', 'movingY'))

        H = self.centralwidget.frameSize().height()
        W = self.centralwidget.frameSize().width()

        #self.theme.move(W - 110, 30)
        self.nowevent.move(10, H - 30)
        self.nowdir.move(10, H - 10)
        self.time.move(10, H - 40)

        self.intervalT.move(10, H - 70)

        self.hideWidg.move(10, H - 90)

        self.buttonleft.move(W // 2 - 60, H - 10)
        self.buttonright.move(W // 2 + 20, H - 10)
        self.buttonstop.move(W // 2 - 20, H - 10)
        self.buttonleftW.move(W // 2 - 100, H - 10)
        self.buttonrightW.move(W // 2 + 60, H - 10)

        self.AllpInEvent.move(W - 110, H - 10)
        self.openASmatplot.move(W - 110, H - 45)

        self.btnStartAU.move(W - 140, H - 70)
        self.btnStopAU.move(W - 140, H - 70)
        self.SliderAU.move(W - 110, H - 70)

        self.newRegim.move(W - 220, H - 10)

        self.btnStartPD.move(W - 170, H - 70)
        self.btnStopPD.move(W - 170, H - 70)
        self.currentStepPD.move(W - 220, H - 70)

        S = min(round(H/buttonsHW), round(W/buttonsHW))
        w = round(W/2)
        h = round(H/2)
        for i in self.buttons:
            i.setFixedSize(S, S)
            
            i.setStyleSheet(" QPushButton {background-color: " + i.col + " ; color: " + i.textcol +" ; border-radius: "+str(int(i.frameSize().width()/2))+"px; font-size: " +str(int(i.frameSize().width()/4.3))+ "px ;} " # QPushButton:hover { background-color: rgb(16, 16, 24) ; color: rgb(76, 76, 76);}
                                        "QPushButton:pressed {background-color: #b784a7 ; }")
            if i.znach is None:
                i.setText(f'{int(i.ch)}') 
            
            else:
                if self.HZnach and self.HChan:
                    i.setText(f'{int(i.znach)}\nC{int(i.ch)}') 
                elif self.HZnach:
                    i.setText(f'{int(i.znach)}') 
                elif self.HChan:
                    i.setText(f'C{int(i.ch)}')
                else:
                    i.setText(f'')
            i.move(round(i.x * S / moveX + w)-S//2+movingX, round(i.y * S / moveY + h)+movingY)
            

    def openVisualwin(self):
        if not self.vid:
            self.vid = True
            self.win = VisualWindow(self)
            self.win.show()

    def OpenDir(self):

        fname = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            #directory=HOME_PATH,
            options=QFileDialog.Option.ShowDirsOnly,
            )
        
        if str(fname) != '':
            self.directory_of_ustanovki = str(fname)
            #self.directorynameText.setText(f'dir: {self.directory_of_ustanovki}')
            #self.openingFile(fname)
            self.AllItems = os.listdir(fname)
            self.showWidgets()
            self.showNug()
            self.btnStopAU.hide()
            self.events.clear()
            self.events.addItems([str(i) for i in self.AllItems])
            self.i = 0
            self.nowdir.setText(f'Dir: {self.directory_of_ustanovki}')
            self.changeEventsfromcombobox()

        else:
            return None   

    def closeEvent(self, event):
        for i in self.buttons:
            for j in i.win:
                j.close()
        if self.vid:
            self.win.close()
        if self.reference:
            self.ref.close()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(App, self).resizeEvent(event)
    
    def wheelEvent(self, event):

        numPixels = event.pixelDelta()
        numDegrees = event.angleDelta() / 8
        self.settings.set('Set_SIMPS', 'buttonsHW', f"{float(self.settings.get('Set_SIMPS', 'buttonsHW')) + event.angleDelta().y() // 120}")
        if float(self.settings.get('Set_SIMPS', 'buttonsHW')) < 0.5:
            self.settings.set('Set_SIMPS', 'buttonsHW', '0.5')
        print(event.modifiers())
        self.newSize()
        event.accept()

    def keyPressEvent(self, e):
        print('srhfoisd')
        if e.key() == Qt.Key.Key_W:
            self.settings.set('Set_SIMPS', 'movingY', f"{(int(self.settings.get('Set_SIMPS', 'movingY')) -  10)}")
            self.newSize()
        elif e.key() == Qt.Key.Key_A:
            self.settings.set('Set_SIMPS', 'movingX', f"{(int(self.settings.get('Set_SIMPS', 'movingX')) -  10)}")
            self.newSize()
        elif e.key() == Qt.Key.Key_D:
            self.settings.set('Set_SIMPS', 'movingX', f"{(int(self.settings.get('Set_SIMPS', 'movingX')) +  10)}")
            self.newSize()
        elif e.key() == Qt.Key.Key_S:
            self.settings.set('Set_SIMPS', 'movingY', f"{(int(self.settings.get('Set_SIMPS', 'movingY')) +  10)}")
            self.newSize()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButtons.RightButton:
                print("Right button clicked")
    '''
    def mouseMoveEvent(self, event):
   # Handle mouse move event
        print(f"Mouse moved to")
        pos = QCursor.pos()
        print(pos.x())
        
        if abs(pos.x() - self.mouseX) > 25 or abs(pos.y() - self.mouseY) > 25:
            self.mouseY = pos.y()
            self.mouseX = pos.x()
        
        print(self.mouseX - pos.x())

        self.settings.set('Set_SIMPS', 'movingX', f'{(int(self.settings.get('Set_SIMPS', 'movingX')) -  self.mouseX + pos.x())}')
        self.settings.set('Set_SIMPS', 'movingY', f'{(int(self.settings.get('Set_SIMPS', 'movingY')) -  self.mouseY + pos.y())}')
        self.newSize()
        print(float(self.settings.get('Set_SIMPS', 'buttonsHW')))
        #print(f'{(int(self.settings.get('Set_SIMPS', 'movingX')) -  self.mouseX + pos.x()) // int(10 / float(self.settings.get('Set_SIMPS', 'buttonsHW')))}')'''

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.tight_layout()
        #fig.subplots_adjust(left=0.020, right=0.980, top=0.950, bottom=0.090)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

    
class Chan(QMainWindow):

    #resized = QtCore.pyqtSignal()
    
    def __init__(self, b, parent):
        
        super().__init__()
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.setWindowTitle(f" Channel: {int(b.ch)} ")

        self.parentt = parent
        self.b = b

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)

        self.chan = QLabel(f"C{int(b.ch)}", self)
        #chan.move(10, 10)
        self.chan.setFixedSize(100, 30)

        #self.sipm = QLabel(f"SIPM: {b.sipm}", self)
        #sipm.move(10, 30)
        #self.sipm.setFixedSize(100, 30)

        self.amax  = QLabel(f"A Max: {b.znach}", self)
        #amax.move(10, 50)
        self.amax.setFixedSize(100, 30)

        self.eventt = QComboBox(self)
        self.eventt.clear()
        self.eventt.addItems(['All'] + self.parentt.AllItems)
        self.eventt.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.eventt.move(230, 10)
        self.eventt.activated.connect(self.event_ch)

        self.chans = QComboBox(self)
        self.chans.addItems([str(int(b.ch))] + ['All'] +  ['sum of Channels'] + list(map(str, range(len(self.parentt.buttons)))))
        #self.chans.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.chans.activated.connect(self.chan_ch)
        self.chans.setFixedWidth(90)

        self.d = ['All'] + self.parentt.AllItems
        self.dir = self.parentt.directory_of_ustanovki

        self.len = len(self.parentt.AllItems) + 1
        
        self.eventt.setCurrentText(self.parentt.eventt)
        self.index = self.eventt.currentIndex()

        self.right_b = QPushButton(f'->', self)
        self.right_b.setFixedSize(50, 30)
        self.right_b.clicked.connect(self.right_b_func)

        self.left_b = QPushButton(f'<-', self)
        self.left_b.setFixedSize(50, 30)
        self.left_b.clicked.connect(self.left_b_func)


        self.st = QSpinBox(self)
        self.st.setMinimum(0)
        self.st.setMaximum(1020)
        self.st.setValue(0)
        self.st.valueChanged.connect(self.chs)
        self.la = QSpinBox(self)
        self.la.setMinimum(0)
        self.la.setMaximum(1020)
        self.la.setValue(1020)
        self.la.valueChanged.connect(self.chs)

        #self.time = QLabel(f'Time: {self.parentt.nowtime}', self)
        #self.time.setFixedSize(200, 30)
        #self.time.move(10, 70)

        self.Hl = QHBoxLayout()
        self.Hl.addWidget(self.chan)
        #self.Hl.addWidget(self.sipm)
        self.Hl.addWidget(self.amax)
        #self.Hl.addWidget(self.time)
        self.Hl.addWidget(self.st)
        self.Hl.addWidget(self.la)
        self.Hl.addWidget(self.left_b)
        self.Hl.addWidget(self.right_b)
        self.Hl.addWidget(self.eventt)
        self.Hl.addWidget(self.chans)

        toolbar = NavigationToolbar(self.sc, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        layout.addLayout(self.Hl)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)

        self.centralwidget = widget
        self.setCentralWidget(widget)
        #self.resized.connect(self.newSize)

        self.drowew()

    def chs(self):
        self.drowew()

    def event_ch(self):
        self.index = self.eventt.currentIndex()
        self.drowew()

    def chan_ch(self):
        self.index = self.eventt.currentIndex()
        self.drowew()

    def right_b_func(self):
        self.index += 1
        if self.index == self.len:
            self.index = 0
        self.eventt.setCurrentIndex(self.index)
        self.drowew()

    def left_b_func(self):
        self.index -= 1
        if self.index == -1:
            self.index = self.len - 1
        self.eventt.setCurrentIndex(self.index)
        self.drowew()

    def drowew(self):
        self.sc.axes.cla()
        print(self.eventt.currentText())
        if self.st.value() > self.la.value():
            return None
        if self.eventt.currentText() == "All" and self.chans.currentText() == "All":
            return None
        elif self.eventt.currentText() == "All" and self.chans.currentText() == "sum of Channels":
            return None
        elif self.eventt.currentText() == "All":
            for i in self.d:
                if i == 'All':
                    continue
                plot_data = pd.read_csv(self.dir + '/' + i)
                plot_data = plot_data[f'{self.chans.currentText()}']
                #self.time.setText(f"Time: {plot_data['Time'].unique()[0]}")
                y = plot_data.tolist()
                #x = range(0,1024)
                #ax.figure(figsize=(7,4))
                self.sc.axes.plot(y)
                #self.sc.axes.set_title(f'Event {self.eventt.currentText()} S{self.b.sipm} C{self.b.ch}')
                self.sc.axes.grid(linestyle='--', color='pink')
            self.amax.setText(f'-')
            self.chan.setText(f'{self.chans.currentText()}')
        elif self.chans.currentText() == "All":
            plot_data = pd.read_csv(self.dir + '/' + self.d[self.index])
            s = 0
            for i in plot_data.columns:
                y = plot_data[i].tolist()
                s += sum(y)
                self.sc.axes.plot(y)
            self.amax.setText(f'sum: {s}')
            self.chan.setText('all')
        elif self.chans.currentText() == 'sum of Channels':
            plot_data = pd.read_csv(self.dir + '/' + self.d[self.index])
            s = 0
            v = []
            for i in range(len(plot_data)):
                v.append(sum(plot_data.iloc[i].tolist()))
            self.sc.axes.plot(v)
            self.amax.setText(f'-')
            self.chan.setText('sum of Channels')
        else:
            plot_data = pd.read_csv(self.dir + '/' + self.d[self.index])
            print(plot_data.head())
            plot_data = plot_data[f'{self.chans.currentText()}']
            #self.time.setText(f"Time: {plot_data['Time'].unique()[0]}")
            y = plot_data.tolist()
            #x = range(0,1024)
            #ax.figure(figsize=(7,4))
            self.sc.axes.plot(y)
            #self.sc.axes.set_title(f'Event {self.eventt.currentText()} S{self.b.sipm} C{self.b.ch}')

            self.amax.setText(f'{max(y)}')
            self.chan.setText(f'{self.chans.currentText()}')
        self.sc.axes.grid(linestyle='--', color='pink')
        self.sc.axes.set_xlim([self.st.value(), self.la.value()])
        self.sc.axes.set_xlabel('time')
        self.sc.axes.set_ylabel('amplitude')            
        self.sc.draw()

    #def resizeEvent(self, event):
    #    self.resized.emit()
    #   return super(Chan, self).resizeEvent(event)
    
    def closeEvent(self, event):
        self.b.f = False
    
    def newSize(self):
        pass

class Reference(QMainWindow):

    resized = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parentt = parent

        self.setWindowTitle("Settings")
        self.setMinimumWidth(650)
        self.setMinimumHeight(400)
        self.setFixedSize(390, 200)
        print(999)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resized.connect(self.newSize)

        self.p = QTextBrowser(self)
        self.p.setFixedSize(390, 200)
        self.p.setOpenExternalLinks(True)
        self.p.setText("Это прогррамма для первичного анализа данных с телескопа LOLITA")
        self.p.append("Автор: Марков Александр")
        self.p.append("Руководитель: Бонвеч Елена Алексеевна")
        self.p.append('<a href=https://github.com/SecondAlexAC/Telescop>Мой Github</a>')
        self.p.append('<a> </a>')

    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        self.parentt.reference = False
        event.accept()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Reference, self).resizeEvent(event)
    
    def newSize(self):
        #self.drow.move(self.centralwidget.frameSize().width() // 2 - 50, 30)
        print(99)
        #self.events.move(self.centralwidget.frameSize().width() - 75, 10)

class MplCanvas1(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=2, height=4, dpi=80):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.tight_layout()
        #fig.subplots_adjust(left=0.020, right=0.980, top=0.950, bottom=0.090)
        self.axes = fig.add_subplot(111)
        super(MplCanvas1, self).__init__(fig)

class Grafic(QMainWindow):

    #resized = QtCore.pyqtSignal()
    
    def __init__(self, parent):
        
        super().__init__()
        self.setMinimumWidth(300)
        self.setMinimumHeight(500)
        

        self.parentt = parent

        self.sc = MplCanvas1(self, width=1, height=2, dpi=100)

        self.eventt = QComboBox(self)
        self.eventt.clear()
        self.index = 0
        self.eventt.addItems(self.parentt.AllItems)
        self.d = self.parentt.directory_of_ustanovki
        self.eventt.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        #self.eventt.move(230, 10)
        self.eventt.activated.connect(self.box_func)
        self.eventt.setCurrentText(self.parentt.eventt)
        toolbar = NavigationToolbar(self.sc, self)

        self.btnL = QPushButton('<', self)
        self.btnL.clicked.connect(self.left_b_func)
        self.btnR = QPushButton('>', self)
        self.btnR.clicked.connect(self.right_b_func)

        self.themes = QComboBox(self)
        self.themes.addItems(['RdGy'] + matplotlib.pyplot.colormaps())
        self.themes.activated.connect(self.drowew)

        self.len = len(self.parentt.AllItems)
        
        layout = QVBoxLayout()
        layout.addWidget(self.sc)

        qw1 = QHBoxLayout()
        qw1.addWidget(toolbar)
        qw1.addWidget(self.themes)

        layout.addLayout(qw1)

        qw2 = QHBoxLayout()
        qw2.addWidget(self.btnL)
        qw2.addWidget(self.btnR)
        qw2.addWidget(self.eventt)

        layout.addLayout(qw2)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)

        self.centralwidget = widget
        self.setCentralWidget(widget)
        #self.resized.connect(self.newSize)
        self.setWindowTitle(f"file:{self.eventt.currentText()}")

        self.drowew()

    def right_b_func(self):
        self.index += 1
        if self.index == self.len:
            self.index = 0
        self.eventt.setCurrentIndex(self.index)
        self.drowew()

    def left_b_func(self):
        self.index -= 1
        if self.index == -1:
            self.index = self.len - 1
        self.eventt.setCurrentIndex(self.index)
        self.drowew()

    def box_func(self):
        self.index = self.eventt.currentIndex()
        self.drowew()

    def drowew(self):
        self.sc.axes.cla()
        plot_data = pd.read_csv(self.d + '/' + self.eventt.currentText())
        #self.time.setText(f"Time: {plot_data['Time'].unique()[0]}")
        #x = range(0,1024)
        #self.sc.axes.figure(figsize=(7,4))
        plot_data = np.array([plot_data.iloc[i].tolist() for i in range(len(plot_data))])
        self.sc.axes.imshow(plot_data, cmap=self.themes.currentText(), aspect='auto')
        print(plot_data)
        #self.sc.axes.set_title(f'Event {self.eventt.currentText()} S{self.b.sipm} C{self.b.ch}')
        #self.sc.axes.grid(linestyle='--', color='pink')
        #self.sc.axes.set_xlim([0, 1023])
        #self.sc.axes.set_xlabel('time')
        #self.sc.axes.set_ylabel('amplitude')
        self.sc.draw()
        #self.amax.setText(f'{max(2, 2)}')

    #def resizeEvent(self, event):
    #    self.resized.emit()
    #   return super(Chan, self).resizeEvent(event)
    
    def closeEvent(self, event):
        self.parentt.ff = False
        pass
    
    def newSize(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())