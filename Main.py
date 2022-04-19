from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
import seaborn as sns
import sys


def pol2cart(r, theta):  # define function polar form <--> cartesian
    z = r * np.exp(1j * (theta * np.pi / 180))
    x, y = z.real, z.imag
    return complex(x, y)


def cart2pol(x, y):
    z = x + y * 1j
    r, theta_rad = np.abs(z), np.angle(z)
    theta = theta_rad * 180 / np.pi
    return r, theta


def cal_distance(xa, xb, ya, yb):  # *function find Distance between 2 point
    distance = np.sqrt((xa - xb) ** 2 + (ya - yb) ** 2)
    return distance


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/MainCal.ui", self)
        self.help_w = HelpWindow()
        self.about_w = AboutWindow()
        # Font Setup For ErrorDialog
        font = QFont()
        font.setFamily("Leelawadee UI")
        font.setPointSize(12)
        self.error_dialog = QErrorMessage()
        self.error_dialog.setFont(font)
        # define Var
        self.case = None
        self.r_115 = 0.012825
        self.r_22 = 0.00799
        self.gmr_115 = 0.05069
        self.line_current_115 = 1606.539
        self.line_current_22 = 8397.8
        self.EPSILON_0 = 8.854 * pow(10, -12)
        self.v_safe = 12000
        # event control
        self.actionHelp.triggered.connect(self.help_clicked)
        self.actionAbout_US.triggered.connect(self.about_clicked)
        self.calculate_btn.clicked.connect(self.calculate_clicked)

    def help_clicked(self):
        self.help_w.show()

    def about_clicked(self):
        self.about_w.show()

    def check_null_value(self):
        if not self.conduc_size.text():
            self.error_dialog.showMessage('Please Enter Conductor Size , กรุณากรอกข้อมูล ความยาวของตัวนำที่ขนานกับตัวนำที่มีพลังงานในช่อง Conductor Size')
        elif not self.inter_y.text():
            self.error_dialog.showMessage('Please Enter Interest Y , กรุณากรอกข้อมูลจุด Y ที่สนใจคำนวณ ในช่อง Interest Y ')
        elif not self.inter_x.text():
            self.error_dialog.showMessage('Please Enter Interest X , กรุณากรอกข้อมูลจุด X ที่สนใจคำนวณ ในช่อง Interest X ')
        elif not self.max_h.text():
            self.error_dialog.showMessage('Please Enter Max High , กรุณากรอกความสูงที่สูงที่สุดที่จะคำนวณ ในช่อง Max High')
        elif not self.max_dis.text():
            self.error_dialog.showMessage('Please Enter Max Distance , กรุณากรอกระยะทางที่มากที่สุดที่จะคำนวณ ในช่อง Max Distance')
        else:
            self.stepcalc()

    def calculate_clicked(self):
        if self.case1.isChecked():
            self.case = 1
            self.check_null_value()
        elif self.case2.isChecked():
            self.case = 2
            self.check_null_value()
        elif self.case3.isChecked():
            self.case = 3
            self.check_null_value()
        elif self.case4.isChecked():
            self.case = 4
            self.check_null_value()
        elif self.case5.isChecked():
            self.case = 5
            self.check_null_value()
        elif self.case6.isChecked():
            self.case = 6
            self.check_null_value()
        else:
            self.error_dialog.showMessage('Please Select electric pole type \n กรุณาเลือกชนิดของเสาไฟฟ้าที่ต้องการคำนวณ')

    def stepcalc(self):
        obj_size = float(self.conduc_size.text())
        inter_h = float(self.inter_y.text())
        inter_x = float(self.inter_x.text())
        range_x = float(self.max_h.text())
        range_y = float(self.max_dis.text())
        m_xp = []
        v_induce = []

        for Distance_x in np.arange(-range_x, range_x, 0.1):
            Distance_x = round(Distance_x, 1)
            m_xp.append(Distance_x)
            v_induce.append(self.calculate(Distance_x, inter_h, obj_size))
        data = {'distance': m_xp, 'Induced Voltage': v_induce}
        df = pd.DataFrame.from_dict(data)
        df.set_index('distance', inplace=True)

        title_h = str('Induce Voltage & Distance (High '+str(inter_h)+' m) (Mean'+str(round(np.mean(v_induce),2))+' V) (Max '+str(np.max(v_induce))+'V)')
        df.plot(figsize=(10, 8), ylabel='Induce Voltage(V)', xlabel='Distance(m)', title=title_h, grid=True, xlim=-15, ylim=0)


        # heatmap
        x_ax = np.arange(-range_x, range_x, 0.1)
        y_ax = np.arange(0.1, range_y, 0.1)
        x_ax = np.round(x_ax, 2)
        y_ax = np.round(y_ax, 2)
        z_ax = np.zeros(shape=(len(y_ax), len(x_ax)))
        z_con = np.zeros(shape=(len(y_ax), len(x_ax)))
        cx = -1

        for x_vax in x_ax:
            cx += 1
            cy = -1
            for y_vax in y_ax:
                cy += 1
                z_ax[cy][cx] = self.calculate(x_vax, y_vax, obj_size)
                if self.calculate(x_vax, y_vax, obj_size) >= self.v_safe:
                    z_con[cy][cx] = 1
                else:
                    z_con[cy][cx] = 0

        # Normal Heatmap
        df = pd.DataFrame(data=z_ax, columns=x_ax, index=y_ax)
        plt.figure(figsize=(16, 9))
        heatmap = sns.heatmap(df, cbar_kws={'label': 'Induce Voltage(V)'}, cmap='Spectral')
        heatmap.invert_yaxis()
        heatmap.set(xlabel='Distance(m)', ylabel='High(m)', title='Induce Voltage & Distance')

        # safe zone Heatmap
        df = pd.DataFrame(data=z_con, columns=x_ax, index=y_ax)
        plt.figure(figsize=(16, 9))
        heatmap = sns.heatmap(df, cmap='OrRd', cbar=False)
        heatmap.invert_yaxis()
        heatmap.invert_xaxis()
        heatmap.set(xlabel='Distance(m)', ylabel='High(m)', title='Danger Zone')
        plt.show()

    def calculate(self, xp, yp, obj_size):
        with np.errstate(divide='ignore', invalid='ignore'):
        ###########################################################################################
            if self.case == 1:  # case 1 : 115Kv R3
                (xa, ya) = (2.05, 18.8)
                (xb, yb) = (2.05, 16.3)
                (xc, yc) = (2.05, 13.8)
                (r_a, theta_a) = (115000, 0)
                (r_b, theta_b) = (115000, -120)
                (r_c, theta_c) = (115000, 120)
                conductor = ('a', 'b', 'c')
                comb = combinations([conductor[i] for i in range(len(conductor))], 2)
                distant, distantp, distantD, vphase, iphase = {}, {}, {}, {}, {}

                for i in list(comb):
                    key = str(str(i[0]) + str(i[1]))
                    distant[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                            vars()['y' + i[1]])
                    distantp[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                             - vars()['y' + i[1]])
                for i in conductor:
                    key = str('p' + i)
                    distant[key] = cal_distance(xp, vars()['x' + i], yp, vars()['y' + i])
                    distantp[key] = cal_distance(xp, vars()['x' + i], yp, - vars()['y' + i])
                    distantD[key] = cal_distance(xp, vars()['x' + i], 0, vars()['y' + i])
                    vphase[i] = pol2cart(vars()['r_' + i], np.radians(vars()['theta_' + i]))
                    iphase[i] = pol2cart(self.line_current_115, np.radians(vars()['theta_' + i]))

                v_complex = np.array([[np.divide(vphase['a'], np.sqrt(3))], [np.divide(vphase['b'], np.sqrt(3))],
                                  [np.divide(vphase['c'], np.sqrt(3))]])
                Matrix = np.array(
                    [[np.log(2 * np.divide(ya, self.r_115)), np.log(np.divide(distantp['ab'], distant['ab'])),
                    np.log(np.divide(distantp['ac'], distant['ac']))],
                    [np.log(np.divide(distantp['ab'], distant['ab'])), np.log(2 * np.divide(yb, self.r_115)),
                    np.log(np.divide(distantp['bc'], distant['bc']))],
                    [np.log(np.divide(distantp['ac'], distant['ac'])), np.log(np.divide(distantp['bc'], distant['bc'])),
                    np.log(2 * np.divide(yc, self.r_115))]])
                q_cart = (2 * np.pi * self.EPSILON_0) * np.matmul(np.linalg.inv(Matrix), v_complex)
                vpe = np.divide(((q_cart[0] * np.log(np.divide(distantp['pa'], distant['pa']))) +
                             (q_cart[1] * np.log(np.divide(distantp['pb'], distant['pb']))) +
                             (q_cart[2] * np.log(np.divide(distantp['pc'], distant['pc'])))), (2 * np.pi * self.EPSILON_0))
                i_complex = np.array([[iphase['a']], [iphase['b']], [iphase['c']]])
                SuperPosition = np.array([[np.log(np.divide(distantD['pa'], distant['pa'])),
                                       np.log(np.divide(distantD['pb'], distant['pb'])),
                                       np.log(np.divide(distantD['pc'], distant['pc']))]])
                matrix2 = np.matmul(SuperPosition, i_complex)
                ep = 2 * (10 ** -7) * 100 * np.pi * matrix2
                vpm = ep * obj_size
                vp = vpm + vpe
                (VP, VI) = cart2pol(np.real(vp), np.imag(vp))
                return round(VP[0][0], 2)
            ####################################
            if self.case == 2:  # case 2: 115kv L1 R2
                (xa, ya) = (-2, 15.1)
                (xb, yb) = (2, 15.1)
                (xc, yc) = (2, 12.6)
                (r_a, theta_a) = (115000, 0)
                (r_b, theta_b) = (115000, -120)
                (r_c, theta_c) = (115000, 120)
                conductor = ('a', 'b', 'c')
                comb = combinations([conductor[i] for i in range(len(conductor))], 2)
                distant, distantp, distantD, vphase, iphase = {}, {}, {}, {}, {}

                for i in list(comb):
                    key = str(str(i[0]) + str(i[1]))
                    distant[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                            vars()['y' + i[1]])
                    distantp[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                             - vars()['y' + i[1]])
                for i in conductor:
                    key = str('p' + i)
                    distant[key] = cal_distance(xp, vars()['x' + i], yp, vars()['y' + i])
                    distantp[key] = cal_distance(xp, vars()['x' + i], yp, - vars()['y' + i])
                    distantD[key] = cal_distance(xp, vars()['x' + i], 0, vars()['y' + i])
                    vphase[i] = pol2cart(vars()['r_' + i], np.radians(vars()['theta_' + i]))
                    iphase[i] = pol2cart(self.line_current_115, np.radians(vars()['theta_' + i]))

                v_complex = np.array([[np.divide(vphase['a'], np.sqrt(3))], [np.divide(vphase['b'], np.sqrt(3))], [np.divide(vphase['c'], np.sqrt(3))]])
                Matrix = np.array(
                    [[np.log(2 * np.divide(ya, self.r_115)), np.log(np.divide(distantp['ab'], distant['ab'])),
                    np.log(np.divide(distantp['ac'], distant['ac']))],
                    [np.log(np.divide(distantp['ab'], distant['ab'])), np.log(2 * np.divide(yb, self.r_115)),
                     np.log(np.divide(distantp['bc'], distant['bc']))],
                    [np.log(np.divide(distantp['ac'], distant['ac'])), np.log(np.divide(distantp['bc'], distant['bc'])),
                    np.log(2 * np.divide(yc, self.r_115))]])
                q_cart = (2 * np.pi * self.EPSILON_0) * np.matmul(np.linalg.inv(Matrix), v_complex)
                vpe = np.divide(((q_cart[0] * np.log(np.divide(distantp['pa'], distant['pa']))) + (
                        q_cart[1] * np.log(np.divide(distantp['pb'], distant['pb']))) + (
                        q_cart[2] * np.log(np.divide(distantp['pc'], distant['pc'])))), (2 * np.pi * self.EPSILON_0))
                i_complex = np.array([[iphase['a']], [iphase['b']], [iphase['c']]])
                SuperPosition = np.array([[np.log(np.divide(distantD['pa'], distant['pa'])),
                                       np.log(np.divide(distantD['pb'], distant['pb'])),
                                       np.log(np.divide(distantD['pc'], distant['pc']))]])
                matrix2 = np.matmul(SuperPosition, i_complex)
                ep = 2 * (10 ** -7) * 100 * np.pi * matrix2
                vpm = ep * obj_size
                vp = vpm + vpe
                (VP, VI) = cart2pol(np.real(vp), np.imag(vp))
                return round(VP[0][0], 2)
        ###############################################
            if self.case == 3:  # case 3: 115kv R3 Bundle
                (xa, ya) = (1.95, 18.8)
                (xb, yb) = (2.15, 18.8)
                (xc, yc) = (1.95, 16.3)
                (xd, yd) = (2.15, 16.3)
                (xe, ye) = (1.95, 13.8)
                (xf, yf) = (2.15, 13.8)
                (r_a, theta_a) = (115000, 0)
                (r_b, theta_b) = (115000, 0)
                (r_c, theta_c) = (115000, 120)
                (r_d, theta_d) = (115000, 120)
                (r_e, theta_e) = (115000, -120)
                (r_f, theta_f) = (115000, -120)
                conductor = ('a', 'b', 'c', 'd', 'e', 'f')
                comb = combinations([conductor[i] for i in range(len(conductor))], 2)
                distant, distantp, distantD, vphase, iphase = {}, {}, {}, {}, {}
                for i in list(comb):
                    key = str(str(i[0]) + str(i[1]))
                    distant[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                            vars()['y' + i[1]])
                    distantp[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                             - vars()['y' + i[1]])
                for i in conductor:
                    key = str('p' + i)
                    distant[key] = cal_distance(xp, vars()['x' + i], yp, vars()['y' + i])
                    distantp[key] = cal_distance(xp, vars()['x' + i], yp, - vars()['y' + i])
                    distantD[key] = cal_distance(xp, vars()['x' + i], 0, vars()['y' + i])
                    vphase[i] = pol2cart(vars()['r_' + i], np.radians(vars()['theta_' + i]))
                    iphase[i] = pol2cart(self.line_current_115, np.radians(vars()['theta_' + i]))

                v_complex = np.array([[np.divide(vphase['a'], np.sqrt(3))], [np.divide(vphase['b'], np.sqrt(3))], [np.divide(vphase['c'], np.sqrt(3))],
                                  [np.divide(vphase['d'], np.sqrt(3))], [np.divide(vphase['e'], np.sqrt(3))], [np.divide(vphase['f'], np.sqrt(3))]])
                Matrix = np.array([[np.log(2 * np.divide(ya, self.gmr_115)), np.log(np.divide(distantp['ab'], distant['ab'])),
                                np.log(np.divide(distantp['ac'], distant['ac'])), np.log(np.divide(distantp['ad'], distant['ad'])),
                                np.log(np.divide(distantp['ae'], distant['ae'])), np.log(np.divide(distantp['af'], distant['af']))],
                               [np.log(np.divide(distantp['ab'], distant['ab'])), np.log(2 * np.divide(yb, self.gmr_115)),
                                np.log(np.divide(distantp['bc'], distant['bc'])), np.log(np.divide(distantp['bd'], distant['bd'])),
                                np.log(np.divide(distantp['be'], distant['be'])), np.log(np.divide(distantp['bf'], distant['bf']))],
                               [np.log(np.divide(distantp['ac'], distant['ac'])), np.log(np.divide(distantp['bc'], distant['bc'])),
                                np.log(2 * np.divide(yc, self.gmr_115)), np.log(np.divide(distantp['cd'], distant['cd'])),
                                np.log(np.divide(distantp['ce'], distant['ce'])), np.log(np.divide(distantp['cf'], distant['cf']))],
                               [np.log(np.divide(distantp['ad'], distant['ad'])), np.log(np.divide(distantp['bd'], distant['bd'])),
                                np.log(np.divide(distantp['cd'], distant['cd'])), np.log(2 * np.divide(yd, self.gmr_115)),
                                np.log(np.divide(distantp['de'], distant['de'])), np.log(np.divide(distantp['df'], distant['df']))],
                               [np.log(np.divide(distantp['ae'], distant['ae'])), np.log(np.divide(distantp['be'], distant['be'])),
                                np.log(np.divide(distantp['ce'], distant['ce'])), np.log(np.divide(distantp['de'], distant['de'])),
                                np.log(2 * np.divide(ye, self.gmr_115)), np.log(np.divide(distantp['ef'], distant['ef']))],
                               [np.log(np.divide(distantp['af'], distant['af'])), np.log(np.divide(distantp['bf'], distant['bf'])),
                                np.log(np.divide(distantp['cf'], distant['cf'])), np.log(np.divide(distantp['df'], distant['df'])),
                                np.log(np.divide(distantp['ef'], distant['ef'])), np.log(2 * np.divide(yf, self.gmr_115))]])
                q_cart = (2 * np.pi * self.EPSILON_0) * np.matmul(np.linalg.inv(Matrix), v_complex)
                vpe = np.divide(((q_cart[0] * np.log(np.divide(distantp['pa'], distant['pa']))) +
                   (q_cart[1] * np.log(np.divide(distantp['pb'], distant['pb']))) +
                   (q_cart[2] * np.log(np.divide(distantp['pc'], distant['pc']))) +
                   (q_cart[3] * np.log(np.divide(distantp['pd'], distant['pd']))) +
                   (q_cart[4] * np.log(np.divide(distantp['pe'], distant['pe']))) +
                   (q_cart[5] * np.log(np.divide(distantp['pf'], distant['pf'])))), (2 * np.pi * self.EPSILON_0))
                i_complex = np.array(
                    [[iphase['a']], [iphase['b']], [iphase['c']], [iphase['d']], [iphase['e']], [iphase['f']]])
                SuperPosition = np.array([[np.log(np.divide(distantD['pa'], distant['pa'])), np.log(np.divide(distantD['pb'], distant['pb'])),
                                       np.log(np.divide(distantD['pc'], distant['pc'])), np.log(np.divide(distantD['pd'], distant['pd'])),
                                       np.log(np.divide(distantD['pe'], distant['pe'])), np.log(np.divide(distantD['pf'], distant['pf']))]])
                matrix2 = np.matmul(SuperPosition, i_complex)
                ep = 2 * (10 ** -7) * 100 * np.pi * matrix2
                vpm = ep * obj_size
                vp = vpm + vpe
                (VP, VI) = cart2pol(np.real(vp), np.imag(vp))
                return round(VP[0][0], 2)
            ########################
            if self.case == 4:  # case 4: 115kv R3 +22kv
                (xa, ya) = (2, 18.8)
                (xb, yb) = (2, 16.3)
                (xc, yc) = (2, 13.8)
                (xd, yd) = (-1.13, 10.282)
                (xe, ye) = (0.6, 10.282)
                (xf, yf) = (1.15, 10.282)
                (r_a, theta_a) = (115000, 0)
                (r_b, theta_b) = (115000, -120)
                (r_c, theta_c) = (115000, 120)
                (r_d, theta_d) = (22000, 0)
                (r_e, theta_e) = (22000, -120)
                (r_f, theta_f) = (22000, 120)
                conductor = ('a', 'b', 'c', 'd', 'e', 'f')
                comb = combinations([conductor[i] for i in range(len(conductor))], 2)
                distant, distantp, distantD, vphase, iphase = {}, {}, {}, {}, {}
                for i in list(comb):
                    key = str(str(i[0]) + str(i[1]))
                    distant[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                            vars()['y' + i[1]])
                    distantp[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                             - vars()['y' + i[1]])
                for i in conductor:
                    key = str('p' + i)
                    distant[key] = cal_distance(xp, vars()['x' + i], yp, vars()['y' + i])
                    distantp[key] = cal_distance(xp, vars()['x' + i], yp, - vars()['y' + i])
                    distantD[key] = cal_distance(xp, vars()['x' + i], 0, vars()['y' + i])
                    vphase[i] = pol2cart(vars()['r_' + i], np.radians(vars()['theta_' + i]))
                    if i in ('a', 'b', 'c'):
                        iphase[i] = pol2cart(self.line_current_115, np.radians(vars()['theta_' + i]))
                    if i in ('d', 'e', 'f'):
                        iphase[i] = pol2cart(self.line_current_22, np.radians(vars()['theta_' + i]))

                v_complex = np.array([[np.divide(vphase['a'], np.sqrt(3))], [np.divide(vphase['b'], np.sqrt(3))], [np.divide(vphase['c'], np.sqrt(3))],
                                  [np.divide(vphase['d'], np.sqrt(3))], [np.divide(vphase['e'], np.sqrt(3))], [np.divide(vphase['f'], np.sqrt(3))]])
                Matrix = np.array([[np.log(2 * np.divide(ya, self.r_115)), np.log(np.divide(distantp['ab'], distant['ab'])),
                                np.log(np.divide(distantp['ac'], distant['ac'])), np.log(np.divide(distantp['ad'], distant['ad'])),
                                np.log(np.divide(distantp['ae'], distant['ae'])), np.log(np.divide(distantp['af'], distant['af']))],
                               [np.log(np.divide(distantp['ab'], distant['ab'])), np.log(2 * np.divide(yb, self.r_115)),
                                np.log(np.divide(distantp['bc'], distant['bc'])), np.log(np.divide(distantp['bd'], distant['bd'])),
                                np.log(np.divide(distantp['be'], distant['be'])), np.log(np.divide(distantp['bf'], distant['bf']))],
                               [np.log(np.divide(distantp['ac'], distant['ac'])), np.log(np.divide(distantp['bc'], distant['bc'])),
                                np.log(2 * np.divide(yc, self.r_115)), np.log(np.divide(distantp['cd'], distant['cd'])),
                                np.log(np.divide(distantp['ce'], distant['ce'])), np.log(np.divide(distantp['cf'], distant['cf']))],
                               [np.log(np.divide(distantp['ad'], distant['ad'])), np.log(np.divide(distantp['bd'], distant['bd'])),
                                np.log(np.divide(distantp['cd'], distant['cd'])), np.log(2 * np.divide(yd, self.r_22)),
                                np.log(np.divide(distantp['de'], distant['de'])), np.log(np.divide(distantp['df'], distant['df']))],
                               [np.log(np.divide(distantp['ae'], distant['ae'])), np.log(np.divide(distantp['be'], distant['be'])),
                                np.log(np.divide(distantp['ce'], distant['ce'])), np.log(np.divide(distantp['de'], distant['de'])),
                                np.log(2 * np.divide(ye, self.r_22)), np.log(np.divide(distantp['ef'], distant['ef']))],
                               [np.log(np.divide(distantp['af'], distant['af'])), np.log(np.divide(distantp['bf'], distant['bf'])),
                                np.log(np.divide(distantp['cf'], distant['cf'])), np.log(np.divide(distantp['df'], distant['df'])),
                                np.log(np.divide(distantp['ef'], distant['ef'])), np.log(2 * np.divide(yf, self.r_22))]])
                q_cart = 2 * np.pi * self.EPSILON_0 * np.matmul(np.linalg.inv(Matrix), v_complex)
                vpe = np.divide(((q_cart[0] * np.log(np.divide(distantp['pa'], distant['pa']))) + (
                    q_cart[1] * np.log(np.divide(distantp['pb'], distant['pb']))) + (
                    q_cart[2] * np.log(np.divide(distantp['pc'], distant['pc']))) + (
                    q_cart[3] * np.log(np.divide(distantp['pd'], distant['pd']))) + (
                    q_cart[4] * np.log(np.divide(distantp['pe'], distant['pe']))) + (
                    q_cart[5] * np.log(np.divide(distantp['pf'], distant['pf'])))), (2 * np.pi * self.EPSILON_0))
                i_complex = np.array(
                    [[iphase['a']], [iphase['b']], [iphase['c']], [iphase['d']], [iphase['e']], [iphase['f']]])
                SuperPosition = np.array([[np.log(np.divide(distantD['pa'], distant['pa'])), np.log(np.divide(distantD['pb'], distant['pb'])),
                                       np.log(np.divide(distantD['pc'], distant['pc'])), np.log(np.divide(distantD['pd'], distant['pd'])),
                                       np.log(np.divide(distantD['pe'], distant['pe'])), np.log(np.divide(distantD['pf'], distant['pf']))]])
                matrix2 = np.matmul(SuperPosition, i_complex)
                ep = 2 * (10 ** -7) * 100 * np.pi * matrix2
                vpm = ep * obj_size
                vp = vpm + vpe
                (VP, VI) = cart2pol(np.real(vp), np.imag(vp))
                return round(VP[0][0], 2)
        ############################################################################################
            if self.case == 5:  # case 5: 115kv Double Circuit R1+L2  + 22kv
                (xa, ya) = (-2.1, 18.8)
                (xb, yb) = (-1.9, 18.8)
                (xc, yc) = (1.9, 18.8)
                (xd, yd) = (2.1, 18.8)
                (xe, ye) = (1.9, 13.8)
                (xf, yf) = (2.1, 13.8)
                (xg, yg) = (-1.15, 10.282)
                (xh, yh) = (0.6, 10.282)
                (xi, yi) = (1.15, 10.282)
                (r_a, theta_a) = (115000, 0)
                (r_b, theta_b) = (115000, 0)
                (r_c, theta_c) = (115000, 120)
                (r_d, theta_d) = (115000, 120)
                (r_e, theta_e) = (115000, -120)
                (r_f, theta_f) = (115000, -120)
                (r_g, theta_g) = (22000, 0)
                (r_h, theta_h) = (22000, -120)
                (r_i, theta_i) = (22000, 120)
                conductor = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')
                comb = combinations([conductor[i] for i in range(len(conductor))], 2)
                distant, distantp, distantD, vphase, iphase = {}, {}, {}, {}, {}
                for i in list(comb):
                    key = str(str(i[0]) + str(i[1]))
                    distant[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                            vars()['y' + i[1]])
                    distantp[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                             - vars()['y' + i[1]])
                for i in conductor:
                    key = str('p' + i)
                    distant[key] = cal_distance(xp, vars()['x' + i], yp, vars()['y' + i])
                    distantp[key] = cal_distance(xp, vars()['x' + i], yp, - vars()['y' + i])
                    distantD[key] = cal_distance(xp, vars()['x' + i], 0, vars()['y' + i])
                    vphase[i] = pol2cart(vars()['r_' + i], np.radians(vars()['theta_' + i]))
                    if i in ('a', 'b', 'c', 'd', 'e', 'f'):
                        iphase[i] = pol2cart(self.line_current_115, np.radians(vars()['theta_' + i]))
                    if i in ('g', 'h', 'i'):
                        iphase[i] = pol2cart(self.line_current_22, np.radians(vars()['theta_' + i]))

                v_complex = np.array([[np.divide(vphase['a'], np.sqrt(3))], [np.divide(vphase['b'], np.sqrt(3))], [np.divide(vphase['c'], np.sqrt(3))],
                                  [np.divide(vphase['d'], np.sqrt(3))], [np.divide(vphase['e'], np.sqrt(3))], [np.divide(vphase['f'], np.sqrt(3))],
                                  [np.divide(vphase['g'], np.sqrt(3))], [np.divide(vphase['h'], np.sqrt(3))], [np.divide(vphase['i'], np.sqrt(3))]])
                Matrix = np.array([[np.log(2 * np.divide(ya, self.r_115)), np.log(np.divide(distantp['ab'], distant['ab'])),
                                np.log(np.divide(distantp['ac'], distant['ac'])), np.log(np.divide(distantp['ad'], distant['ad'])),
                                np.log(np.divide(distantp['ae'], distant['ae'])), np.log(np.divide(distantp['af'], distant['af'])),
                                np.log(np.divide(distantp['ag'], distant['ag'])), np.log(np.divide(distantp['ah'], distant['ah'])),
                                np.log(np.divide(distantp['ai'], distant['ai']))],
                               [np.log(np.divide(distantp['ab'], distant['ab'])), np.log(2 * np.divide(yb, self.r_115)),
                                np.log(np.divide(distantp['bc'], distant['bc'])), np.log(np.divide(distantp['bd'], distant['bd'])),
                                np.log(np.divide(distantp['be'], distant['be'])), np.log(np.divide(distantp['bf'], distant['bf'])),
                                np.log(np.divide(distantp['bg'], distant['bg'])), np.log(np.divide(distantp['bh'], distant['bh'])),
                                np.log(np.divide(distantp['bi'], distant['bi']))],
                               [np.log(np.divide(distantp['ac'], distant['ac'])), np.log(np.divide(distantp['bc'], distant['bc'])),
                                np.log(2 * np.divide(yc, self.r_115)), np.log(np.divide(distantp['cd'], distant['cd'])),
                                np.log(np.divide(distantp['ce'], distant['ce'])), np.log(np.divide(distantp['cf'], distant['cf'])),
                                np.log(np.divide(distantp['cg'], distant['cg'])), np.log(np.divide(distantp['ch'], distant['ch'])),
                                np.log(np.divide(distantp['ci'], distant['ci']))],
                               [np.log(np.divide(distantp['ad'], distant['ad'])), np.log(np.divide(distantp['bd'], distant['bd'])),
                                np.log(np.divide(distantp['cd'], distant['cd'])), np.log(2 * np.divide(yd, self.r_115)),
                                np.log(np.divide(distantp['de'], distant['de'])), np.log(np.divide(distantp['df'], distant['df'])),
                                np.log(np.divide(distantp['dg'], distant['dg'])), np.log(np.divide(distantp['dh'], distant['dh'])),
                                np.log(np.divide(distantp['di'], distant['di']))],
                               [np.log(np.divide(distantp['ae'], distant['ae'])), np.log(np.divide(distantp['be'], distant['be'])),
                                np.log(np.divide(distantp['ce'], distant['ce'])), np.log(np.divide(distantp['de'], distant['de'])),
                                np.log(2 * np.divide(ye, self.r_115)), np.log(np.divide(distantp['ef'], distant['ef'])),
                                np.log(np.divide(distantp['eg'], distant['eg'])), np.log(np.divide(distantp['eh'], distant['eh'])),
                                np.log(np.divide(distantp['ei'], distant['ei']))],
                               [np.log(np.divide(distantp['af'], distant['af'])), np.log(np.divide(distantp['bf'], distant['bf'])),
                                np.log(np.divide(distantp['cf'], distant['cf'])), np.log(np.divide(distantp['df'], distant['df'])),
                                np.log(np.divide(distantp['ef'], distant['ef'])), np.log(2 * np.divide(yf, self.r_115)),
                                np.log(np.divide(distantp['fg'], distant['fg'])), np.log(np.divide(distantp['fh'], distant['fh'])),
                                np.log(np.divide(distantp['fi'], distant['fi']))],
                               [np.log(np.divide(distantp['ag'], distant['ag'])), np.log(np.divide(distantp['bg'], distant['bg'])),
                                np.log(np.divide(distantp['cg'], distant['cg'])), np.log(np.divide(distantp['dg'], distant['dg'])),
                                np.log(np.divide(distantp['eg'], distant['eg'])), np.log(np.divide(distantp['fg'], distant['fg'])),
                                np.log(2 * np.divide(yg, self.r_22)), np.log(np.divide(distantp['gh'], distant['gh'])),
                                np.log(np.divide(distantp['gi'], distant['gi']))],
                               [np.log(np.divide(distantp['ah'], distant['ah'])), np.log(np.divide(distantp['bh'], distant['bh'])),
                                np.log(np.divide(distantp['ch'], distant['ch'])), np.log(np.divide(distantp['dh'], distant['dh'])),
                                np.log(np.divide(distantp['eh'], distant['eh'])), np.log(np.divide(distantp['fh'], distant['fh'])),
                                np.log(np.divide(distantp['gh'], distant['gh'])), np.log(2 * np.divide(yh, self.r_22)),
                                np.log(np.divide(distantp['hi'], distant['hi']))],
                               [np.log(np.divide(distantp['ai'], distant['ai'])), np.log(np.divide(distantp['bi'], distant['bi'])),
                                np.log(np.divide(distantp['ci'], distant['ci'])), np.log(np.divide(distantp['di'], distant['di'])),
                                np.log(np.divide(distantp['ei'], distant['ei'])), np.log(np.divide(distantp['fi'], distant['fi'])),
                                np.log(np.divide(distantp['gi'], distant['gi'])), np.log(np.divide(distantp['hi'], distant['hi'])),
                                np.log(2 * np.divide(yi, self.r_22))]])

                q_cart = 2 * np.pi * self.EPSILON_0 * np.matmul(np.linalg.inv(Matrix), v_complex)
                vpe = np.divide(((q_cart[0] * np.log(np.divide(distantp['pa'], distant['pa']))) +
                   (q_cart[1] * np.log(np.divide(distantp['pb'], distant['pb']))) +
                   (q_cart[2] * np.log(np.divide(distantp['pc'], distant['pc']))) +
                   (q_cart[3] * np.log(np.divide(distantp['pd'], distant['pd']))) +
                   (q_cart[4] * np.log(np.divide(distantp['pe'], distant['pe']))) +
                   (q_cart[5] * np.log(np.divide(distantp['pf'], distant['pf']))) +
                   (q_cart[6] * np.log(np.divide(distantp['pg'], distant['pg']))) +
                   (q_cart[7] * np.log(np.divide(distantp['ph'], distant['ph']))) +
                   (q_cart[8] * np.log(np.divide(distantp['pi'], distant['pi'])))), (2 * np.pi * self.EPSILON_0))
                i_complex = np.array(
                    [[iphase['a']], [iphase['b']], [iphase['c']], [iphase['d']], [iphase['e']], [iphase['f']],
                    [iphase['g']], [iphase['h']], [iphase['i']]])
                SuperPosition = np.array([[np.log(np.divide(distantD['pa'], distant['pa'])), np.log(np.divide(distantD['pb'], distant['pb'])),
                                       np.log(np.divide(distantD['pc'], distant['pc'])), np.log(np.divide(distantD['pd'], distant['pd'])),
                                       np.log(np.divide(distantD['pe'], distant['pe'])), np.log(np.divide(distantD['pf'], distant['pf'])),
                                       np.log(np.divide(distantD['pg'], distant['pg'])), np.log(np.divide(distantD['ph'], distant['ph'])),
                                       np.log(np.divide(distantD['pi'], distant['pi']))]])
                matrix2 = np.matmul(SuperPosition, i_complex)
                ep = 2 * (10 ** -7) * 100 * np.pi * matrix2
                vpm = ep * obj_size
                vp = vpm + vpe
                (VP, VI) = cart2pol(np.real(vp), np.imag(vp))
                return round(VP[0][0], 2)
            ############################################################################################
            if self.case == 6:  # case 6: 115kv Double Circuit + 22kv
                (xa, ya) = (-2, 18.8)
                (xb, yb) = (2, 18.8)
                (xc, yc) = (-2, 16.3)
                (xd, yd) = (2, 16.3)
                (xe, ye) = (-2, 13.8)
                (xf, yf) = (2, 13.8)
                (xg, yg) = (-1.15, 10.282)
                (xh, yh) = (0.6, 10.282)
                (xi, yi) = (1.15, 10.282)
                (r_a, theta_a) = (115000, 0)
                (r_b, theta_b) = (115000, 0)
                (r_c, theta_c) = (115000, 120)
                (r_d, theta_d) = (115000, 120)
                (r_e, theta_e) = (115000, -120)
                (r_f, theta_f) = (115000, -120)
                (r_g, theta_g) = (22000, 0)
                (r_h, theta_h) = (22000, -120)
                (r_i, theta_i) = (22000, 120)
                conductor = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i')
                comb = combinations([conductor[i] for i in range(len(conductor))], 2)
                distant, distantp, distantD, vphase, iphase = {}, {}, {}, {}, {}
                for i in list(comb):
                    key = str(str(i[0]) + str(i[1]))
                    distant[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                            vars()['y' + i[1]])
                    distantp[key] = cal_distance(vars()['x' + i[0]], vars()['x' + i[1]], vars()['y' + i[0]],
                                             - vars()['y' + i[1]])
                for i in conductor:
                    key = str('p' + i)
                    distant[key] = cal_distance(xp, vars()['x' + i], yp, vars()['y' + i])
                    distantp[key] = cal_distance(xp, vars()['x' + i], yp, - vars()['y' + i])
                    distantD[key] = cal_distance(xp, vars()['x' + i], 0, vars()['y' + i])
                    vphase[i] = pol2cart(vars()['r_' + i], np.radians(vars()['theta_' + i]))
                    if i in ('a', 'b', 'c', 'd', 'e', 'f'):
                        iphase[i] = pol2cart(self.line_current_115, np.radians(vars()['theta_' + i]))
                    if i in ('g', 'h', 'i'):
                        iphase[i] = pol2cart(self.line_current_22, np.radians(vars()['theta_' + i]))

                v_complex = np.array([[np.divide(vphase['a'], np.sqrt(3))], [np.divide(vphase['b'], np.sqrt(3))], [np.divide(vphase['c'], np.sqrt(3))],
                                  [np.divide(vphase['d'], np.sqrt(3))], [np.divide(vphase['e'], np.sqrt(3))], [np.divide(vphase['f'], np.sqrt(3))],
                                  [np.divide(vphase['g'], np.sqrt(3))], [np.divide(vphase['h'], np.sqrt(3))], [np.divide(vphase['i'], np.sqrt(3))]])
                Matrix = np.array([[np.log(2 * np.divide(ya, self.r_115)), np.log(np.divide(distantp['ab'], distant['ab'])),
                                np.log(np.divide(distantp['ac'], distant['ac'])), np.log(np.divide(distantp['ad'], distant['ad'])),
                                np.log(np.divide(distantp['ae'], distant['ae'])), np.log(np.divide(distantp['af'], distant['af'])),
                                np.log(np.divide(distantp['ag'], distant['ag'])), np.log(np.divide(distantp['ah'], distant['ah'])),
                                np.log(np.divide(distantp['ai'], distant['ai']))],
                               [np.log(np.divide(distantp['ab'], distant['ab'])), np.log(2 * np.divide(yb, self.r_115)),
                                np.log(np.divide(distantp['bc'], distant['bc'])), np.log(np.divide(distantp['bd'], distant['bd'])),
                                np.log(np.divide(distantp['be'], distant['be'])), np.log(np.divide(distantp['bf'], distant['bf'])),
                                np.log(np.divide(distantp['bg'], distant['bg'])), np.log(np.divide(distantp['bh'], distant['bh'])),
                                np.log(np.divide(distantp['bi'], distant['bi']))],
                               [np.log(np.divide(distantp['ac'], distant['ac'])), np.log(np.divide(distantp['bc'], distant['bc'])),
                                np.log(2 * np.divide(yc, self.r_115)), np.log(np.divide(distantp['cd'], distant['cd'])),
                                np.log(np.divide(distantp['ce'], distant['ce'])), np.log(np.divide(distantp['cf'], distant['cf'])),
                                np.log(np.divide(distantp['cg'], distant['cg'])), np.log(np.divide(distantp['ch'], distant['ch'])),
                                np.log(np.divide(distantp['ci'], distant['ci']))],
                               [np.log(np.divide(distantp['ad'], distant['ad'])), np.log(np.divide(distantp['bd'], distant['bd'])),
                                np.log(np.divide(distantp['cd'], distant['cd'])), np.log(2 * np.divide(yd, self.r_115)),
                                np.log(np.divide(distantp['de'], distant['de'])), np.log(np.divide(distantp['df'], distant['df'])),
                                np.log(np.divide(distantp['dg'], distant['dg'])), np.log(np.divide(distantp['dh'], distant['dh'])),
                                np.log(np.divide(distantp['di'], distant['di']))],
                               [np.log(np.divide(distantp['ae'], distant['ae'])), np.log(np.divide(distantp['be'], distant['be'])),
                                np.log(np.divide(distantp['ce'], distant['ce'])), np.log(np.divide(distantp['de'], distant['de'])),
                                np.log(2 * np.divide(ye, self.r_115)), np.log(np.divide(distantp['ef'], distant['ef'])),
                                np.log(np.divide(distantp['eg'], distant['eg'])), np.log(np.divide(distantp['eh'], distant['eh'])),
                                np.log(np.divide(distantp['ei'], distant['ei']))],
                               [np.log(np.divide(distantp['af'], distant['af'])), np.log(np.divide(distantp['bf'], distant['bf'])),
                                np.log(np.divide(distantp['cf'], distant['cf'])), np.log(np.divide(distantp['df'], distant['df'])),
                                np.log(np.divide(distantp['ef'], distant['ef'])), np.log(2 * np.divide(yf, self.r_115)),
                                np.log(np.divide(distantp['fg'], distant['fg'])), np.log(np.divide(distantp['fh'], distant['fh'])),
                                np.log(np.divide(distantp['fi'], distant['fi']))],
                               [np.log(np.divide(distantp['ag'], distant['ag'])), np.log(np.divide(distantp['bg'], distant['bg'])),
                                np.log(np.divide(distantp['cg'], distant['cg'])), np.log(np.divide(distantp['dg'], distant['dg'])),
                                np.log(np.divide(distantp['eg'], distant['eg'])), np.log(np.divide(distantp['fg'], distant['fg'])),
                                np.log(2 * np.divide(yg, self.r_22)), np.log(np.divide(distantp['gh'], distant['gh'])),
                                np.log(np.divide(distantp['gi'], distant['gi']))],
                               [np.log(np.divide(distantp['ah'], distant['ah'])), np.log(np.divide(distantp['bh'], distant['bh'])),
                                np.log(np.divide(distantp['ch'], distant['ch'])), np.log(np.divide(distantp['dh'], distant['dh'])),
                                np.log(np.divide(distantp['eh'], distant['eh'])), np.log(np.divide(distantp['fh'], distant['fh'])),
                                np.log(np.divide(distantp['gh'], distant['gh'])), np.log(2 * np.divide(yh, self.r_22)),
                                np.log(np.divide(distantp['hi'], distant['hi']))],
                               [np.log(np.divide(distantp['ai'], distant['ai'])), np.log(np.divide(distantp['bi'], distant['bi'])),
                                np.log(np.divide(distantp['ci'], distant['ci'])), np.log(np.divide(distantp['di'], distant['di'])),
                                np.log(np.divide(distantp['ei'], distant['ei'])), np.log(np.divide(distantp['fi'], distant['fi'])),
                                np.log(np.divide(distantp['gi'], distant['gi'])), np.log(np.divide(distantp['hi'], distant['hi'])),
                                np.log(2 * np.divide(yi, self.r_22))]])

                q_cart = 2 * np.pi * self.EPSILON_0 * np.matmul(np.linalg.inv(Matrix), v_complex)
                vpe = np.divide(((q_cart[0] * np.log(np.divide(distantp['pa'], distant['pa']))) +
                   (q_cart[1] * np.log(np.divide(distantp['pb'], distant['pb']))) +
                   (q_cart[2] * np.log(np.divide(distantp['pc'], distant['pc']))) +
                   (q_cart[3] * np.log(np.divide(distantp['pd'], distant['pd']))) +
                   (q_cart[4] * np.log(np.divide(distantp['pe'], distant['pe']))) +
                   (q_cart[5] * np.log(np.divide(distantp['pf'], distant['pf']))) +
                   (q_cart[6] * np.log(np.divide(distantp['pg'], distant['pg']))) +
                   (q_cart[7] * np.log(np.divide(distantp['ph'], distant['ph']))) +
                   (q_cart[8] * np.log(np.divide(distantp['pi'], distant['pi'])))), (2 * np.pi * self.EPSILON_0))
                i_complex = np.array(
                    [[iphase['a']], [iphase['b']], [iphase['c']], [iphase['d']], [iphase['e']], [iphase['f']],
                    [iphase['g']], [iphase['h']], [iphase['i']]])
                SuperPosition = np.array([[np.log(np.divide(distantD['pa'], distant['pa'])), np.log(np.divide(distantD['pb'], distant['pb'])),
                                       np.log(np.divide(distantD['pc'], distant['pc'])), np.log(np.divide(distantD['pd'], distant['pd'])),
                                       np.log(np.divide(distantD['pe'], distant['pe'])), np.log(np.divide(distantD['pf'], distant['pf'])),
                                       np.log(np.divide(distantD['pg'], distant['pg'])), np.log(np.divide(distantD['ph'], distant['ph'])),
                                       np.log(np.divide(distantD['pi'], distant['pi']))]])
                matrix2 = np.matmul(SuperPosition, i_complex)
                ep = 2 * (10 ** -7) * 100 * np.pi * matrix2
                vpm = ep * obj_size
                vp = vpm + vpe
                (VP, VI) = cart2pol(np.real(vp), np.imag(vp))
                return round(VP[0][0], 2)


class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/Help.ui", self)


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/About.ui", self)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
