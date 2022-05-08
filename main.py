import locale
import ui.resources_rc
import datetime
import sys
import json
from PyQt5 import QtWidgets, QtCore, uic
import psycopg2
from smtplib import SMTP
import sys
import requests


from database import db_session
from database.tables import *

HOST = 'localhost'
PORT = 4567


class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        uic.loadUi('ui/MainUI.ui', self)
        self.user = None
        self.InstallationButton.clicked.connect(lambda: self.UserStackedWidget.setCurrentIndex(1))
        self.ChangeButton.clicked.connect(lambda: self.UserStackedWidget.setCurrentIndex(2))
        self.RepairButton.clicked.connect(lambda: self.UserStackedWidget.setCurrentIndex(3))
        self.PurchaseButton.clicked.connect(lambda: self.UserStackedWidget.setCurrentIndex(4))
        self.UtilizationButton.clicked.connect(lambda: self.UserStackedWidget.setCurrentIndex(5))

        self.InstallationSendButton.clicked.connect(self.installation_call)
        self.ChangeSendButton.clicked.connect(self.change_call)
        self.RepairSendButton.clicked.connect(self.repair_call)
        self.PurchaseSendButton.clicked.connect(self.purchase_call)
        #self.UtilizationSendButton.clicked.connect(self.utilization_call)

        self.EnterButton.clicked.connect(self.enter)
        self.ExitButton.clicked.connect(self.exit)
        self.MainStackedWidget.setCurrentIndex(0)
        self.UserStackedWidget.setCurrentIndex(0)
        self.menu_button.clicked.connect(self.slide_left_menu)

    def slide_left_menu(self):
        width = self.side_menu.width()
        print(width)
        if width == 0:
            new_width = 160
        else:
            new_width = 0
        self.animation = QtCore.QPropertyAnimation(self.side_menu, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.start()

    def enter(self):
        data = {"login": self.Login.text(),
                "password": self.Password.text()}
        response = requests.get(f'http://{HOST}:{str(PORT)}/login', params=data).json()
        if response['status'] == 'success':
            self.StatusLabel.setText('Добро пожаловать!')
            self.user = json.loads(response['user'])
            if self.user.get("is_admin"):
                try:
                    self.MainStackedWidget.setCurrentIndex(2)
                except BaseException as e:
                    print('Admin error')
            else:
                self.user_nick.setText(f"{self.user.get('surname')} {self.user.get('name')}")
                self.user_nick.update()
                #self.user = user
                # self.letter.user_icon.setPixmap(self.account.photo)
                self.MainStackedWidget.setCurrentIndex(1)
        elif response.get('status') == 'password fail':
            self.input_label.setText("Неверный пароль")
        else:
            self.input_label.setText("Нет пользователя с таким логином")

    def exit(self):
        self.user = None
        self.MainStackedWidget.setCurrentIndex(0)
        self.UserStackedWidget.setCurrentIndex(0)
        self.installation_clean()
        self.change_clean()
        self.repair_clean()
        self.purchase_clean()
        #self.utilization_clean()

    def installation_call(self):
        name = self.NameInstallation.text()
        quantity = self.QuantityInstallation.value()
        number = self.NumberInstallation.text()
        # добавить обработчик текста
        place = self.PlaceInstallation.currentText()
        task_type = 1
        inf = {"name": name,
               "quantity": quantity,
               "number": number,
               "place": place}
        inf = json.dumps(inf)
        data = {"task_type": task_type,
                "user": self.user.id,
                "inf": inf}
        response = requests.post(f'http://{HOST}:{str(PORT)}/task_interacting_with_db', data=data)
        if response.text == 'success':
            self.StatusLabel.setText('Запрос на установку оборудования отправлен')
        else:
            self.StatusLabel.setText('Ошибка при отправке запроса!\nПовторите попытку')
        self.installation_clean()
        self.UserStackedWidget.setCurrentIndex(0)

    def installation_clean(self):
        self.NameInstallation.setText('')
        self.QuantityInstallation.setValue(0)
        self.NumberInstallation.setText('')
        self.PlaceInstallation.setCurrentText('-')

    def change_call(self):
        old_name = self.OldNameChange.text()
        old_quantity = self.OldQuantityChange.value()
        old_number = self.OldNumberChange.text()
        new_name = self.NewNameChange.text()
        new_quantity = self.NewQuantityChange.value()
        new_number = self.NewNumberChange.text()
        # добавить обработчик текста
        place = self.PlaceInstallation.currentText()
        task_type = 2
        inf = {'old_name': old_name,
               'old_quantity': old_quantity,
               'old_number': old_number,
               'new_name': new_name,
               'new_quantity': new_quantity,
               'new_number': new_number,
               'place': place}
        inf = json.dumps(inf)
        data = {'task_type': task_type,
                'user': self.user.id,
                'inf': inf}
        response = requests.post('http://localhost:4567/task_interacting_with_db', data=data)
        if response.text == 'success':
            self.StatusLabel.setText('Запрос на замену оборудования отправлен')
        else:
            self.StatusLabel.setText('Ошибка при отправке запроса!\nПовторите попытку')
        self.change_clean()
        self.UserStackedWidget.setCurrentIndex(0)

    def change_clean(self):
        self.OldNameChange.setText('')
        self.OldQuantityChange.setValue(0)
        self.OldNumberChange.setText('')
        self.NewNameChange.setText('')
        self.NewQuantityChange.setValue(0)
        self.NewNumberChange.setText('')
        self.PlaceInstallation.setCurrentText('-')

    def repair_call(self):
        name = self.NameRepair.text()
        quantity = self.QuantityRepair.value()
        number = self.NumberRepair.text()
        # добавить обработчик текста
        place = self.PlaceRepair.currentText()
        reason = self.ReasonRepair.toPlainText()
        task_type = 3
        inf = {'name': name,
               'quantity': quantity,
               'number': number,
               'reason': reason,
               'place': place
        }
        inf = json.dumps(inf)
        data = {'task_type': task_type,
                'user': self.user.id,
                'inf': inf}
        response = requests.post('http://localhost:4567/task_interacting_with_db', data=data)
        if response.text == 'success':
            self.StatusLabel.setText('Запрос на обслуживание оборудования отправлен')
        else:
            self.StatusLabel.setText('Ошибка при отправке запроса!\nПовторите попытку')
        self.UserStackedWidget.setCurrentIndex(0)

    def repair_clean(self):
        self.NameRepair.setText('')
        self.QuantityRepair.setValue(0)
        self.NumberRepair.setText('')
        self.PlaceRepair.setCurrentText('-')
        self.ReasonRepair.setText('')

    def purchase_call(self):
        name = self.NamePurchase.text()
        quantity = self.QuantityPurchase.value()
        price = self.PricePurchase.text()
        reason = self.ReasonPurchase.toPlainText()
        # добавить обработчик текста
        link = self.LinkPurchase.text()
        task_type = 4
        inf = {'name': name,
               'quantity': quantity,
               'price': price,
               'reason': reason,
               'link': link}
        inf = json.dumps(inf)
        data = {'task_type': task_type,
                'user': self.user.id,
                'inf': inf}
        response = requests.post('http://localhost:4567/task_interacting_with_db', data=data)
        if response.text == 'success':
            self.StatusLabel.setText('Запрос на закупку оборудования отправлен')
        else:
            self.StatusLabel.setText('Ошибка при отправке запроса!\nПовторите попытку')
        self.purchase_clean()
        self.UserStackedWidget.setCurrentIndex(0)

    def purchase_clean(self):
        self.NamePurchase.setText('')
        self.QuantityPurchase.setValue(0)
        self.PricePurchase.setText('')
        self.LinkPurchase.setText('')
        self.ReasonPurchase.setText('')

    def utilization_call(self):
        pass
        # отправка запроса
        # полчуение ответа

    def utilization_clean(self):
        pass


if __name__ == "__main__":
    db_session.global_init()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    main = Application()
    main.show()
    app.exec_()