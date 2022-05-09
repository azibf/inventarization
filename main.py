import json
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import (QTableWidgetItem)
from smtplib import SMTP
import sys
import requests
from Message.message_widget import *


from database import db_session
from database.tables import *

HOST = 'localhost'
PORT = 4567


class AdminFeatures(QtWidgets.QMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        super().__init__()
        uic.loadUi('ui/MainUI.ui', self)

    def save_task(self):
            pass

    def save_equipment(self):
        pass

    def save_user(self):
        pass

    def open_users(self):
        s = ['Пользователь', 'Админ']
        users = json.loads(requests.get(f'http://{HOST}:{str(PORT)}/user_admin').json())
        self.UserViewTable.setRowCount(len(users))
        for i, el in enumerate(users.keys()):
            user = json.loads(users[el])
            self.UserViewTable.setItem(i, 0, QTableWidgetItem(user['id']))
            self.UserViewTable.setItem(i, 1, QTableWidgetItem(user['surname']))
            self.UserViewTable.setItem(i, 2, QTableWidgetItem(user['name']))
            self.UserViewTable.setItem(i, 3, QTableWidgetItem(user['patronymic']))
            self.UserViewTable.setItem(i, 4, QTableWidgetItem(user['email']))
            self.UserViewTable.setItem(i, 5, QTableWidgetItem(user['phone']))
            item = QTableWidgetItem('')
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if not user['is_admin']:
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setText(s[0])
            else:
                item.setCheckState(QtCore.Qt.Checked)
                item.setText(s[1])
            self.UserViewTable.setItem(i, 6, item)

    def open_tasks(self):
        counter = 0
        self.TaskViewTable.setRowCount(counter)
        s = ['В процессе', 'Завершено']
        state_params = [self.InstallationCB.checkState() == QtCore.Qt.Checked,
                        self.ChangeCB.checkState() == QtCore.Qt.Checked,
                        self.MovingCB.checkState() == QtCore.Qt.Checked,
                        self.PurchaseCB.checkState() == QtCore.Qt.Checked,
                        self.UtilizationCB.checkState() == QtCore.Qt.Checked]
        print(state_params)
        tasks = json.loads(requests.get(f'http://{HOST}:{str(PORT)}/task_admin').json())
        dict = {1: "Установка оборудования",
                2: "Замена оборудования",
                3: "Обслуживание оборудования",
                4: "Закупка оборудования",
                5: "Утилизация оборудования"}
        for i, el in enumerate(tasks.keys()):
            elem = json.loads(tasks[el])
            if state_params[elem['task_type'] - 1] and (elem['is_finished'] in [False, self.IsFihishedCB.checkState()]):
                self.TaskViewTable.setRowCount(counter + 1)
                self.TaskViewTable.setItem(counter, 0, QTableWidgetItem(str(elem['id'])))
                self.TaskViewTable.setItem(counter, 1, QTableWidgetItem(dict[elem['task_type']]))
                self.TaskViewTable.setItem(counter, 2, QTableWidgetItem(elem['inf']))
                self.TaskViewTable.setItem(counter, 3, QTableWidgetItem(elem['user']))
                item = QTableWidgetItem('')
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                if not elem['is_finished']:
                    item.setCheckState(QtCore.Qt.Unchecked)
                else:
                    item.setCheckState(QtCore.Qt.Checked)
                item.setText(s[elem['is_finished']])
                self.TaskViewTable.setItem(counter, 4, item)
                counter += 1

    def open_equipment(self):
        all_equipment = json.loads(requests.get(f'http://{HOST}:{str(PORT)}/equipment_admin').json())
        print(all_equipment)
        self.EquipmentViewTable.setRowCount(len(all_equipment))
        for i, el in enumerate(all_equipment.keys()):
            equipment = json.loads(all_equipment[el])
            self.EquipmentViewTable.setItem(i, 0, QTableWidgetItem(equipment['id']))
            self.EquipmentViewTable.setItem(i, 1, QTableWidgetItem(equipment['name']))
            self.EquipmentViewTable.setItem(i, 2, QTableWidgetItem(equipment['number']))
            self.EquipmentViewTable.setItem(i, 3, QTableWidgetItem(equipment['place']))

    def add_equipment(self):
        rows = self.EquipmentViewTable.rowCount() + 1
        self.EquipmentViewTable.setRowCount(rows)

    def send_email(self):
        email_from = 'mailsenderfromwork@gmail.com'
        email_to = self.user[5]
        text = ''
        rows = self.TaskViewTable.rowCount()
        for i in range(rows):
            text += f"{self.ViewTable.item(i, 0).text()} {self.ViewTable.item(i, 1).text()} {self.ViewTable.item(i, 2).text()}\n"
        try:
            with SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('mailsenderfromwork@gmail.com', 'gDjbyDSmW7i6uvT')
                server.sendmail(email_from, email_to, text.encode('utf-8'))
            self.second_form = Message()
        except:
            self.second_form = Message(1)


class UserFeatures(QtWidgets.QMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        super().__init__()
        uic.loadUi('ui/MainUI.ui', self)
        self.user = None

    def send_request(self, task_type, inf):
        inf = json.dumps(inf)
        data = {"task_type": task_type,
                "user": self.user["id"],
                "inf": inf}
        response = requests.post(f'http://{HOST}:{str(PORT)}/task_interacting_with_db', data=data)
        print(response.text)
        if response.text == 'success':
            self.StatusLabel.setText('Запрос отправлен')
        else:
            self.StatusLabel.setText('Ошибка при отправке запроса!\nПовторите попытку')
        self.UserStackedWidget.setCurrentIndex(0)

    def clean_tasks_params(self):
        state_params = [self.InstallationCB, self.ChangeCB, self.MovingCB, self.PurchaseCB, self.UtilizationCB]
        for elem in state_params:
            elem.setCheckState(QtCore.Qt.Checked)
        self.IsFihishedCB.setCheckState(QtCore.Qt.Unchecked)
        self.open_tasks()

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
        self.send_request(task_type, inf)
        self.installation_clean()

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
        self.send_request(task_type, inf)
        self.change_clean()

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
        self.send_request(task_type, inf)
        self.repair_clean()

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
        self.send_request(task_type, inf)
        self.purchase_clean()

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


class Application(AdminFeatures, UserFeatures):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/MainUI.ui', self)
        self.changes = {'task': [],
                        'equipment': [],
                        'user': []}
        self.InstallationButton.clicked.connect(lambda: self.UserStackedWidget.setCurrentIndex(1))
        self.ChangeButton.clicked.connect(lambda: self.UserStackedWidget.setCurrentIndex(2))
        self.RepairButton.clicked.connect(lambda: self.UserStackedWidget.setCurrentIndex(3))
        self.PurchaseButton.clicked.connect(lambda: self.UserStackedWidget.setCurrentIndex(4))
        self.UtilizationButton.clicked.connect(lambda: self.UserStackedWidget.setCurrentIndex(5))
        self.TaskButton.clicked.connect(lambda: self.AdminStackedWidget.setCurrentIndex(0))
        self.EquipmentButton.clicked.connect(lambda: self.AdminStackedWidget.setCurrentIndex(1))
        self.UserButton.clicked.connect(lambda: self.AdminStackedWidget.setCurrentIndex(2))

        self.InstallationSendButton.clicked.connect(self.installation_call)
        self.ChangeSendButton.clicked.connect(self.change_call)
        self.RepairSendButton.clicked.connect(self.repair_call)
        self.PurchaseSendButton.clicked.connect(self.purchase_call)
        #self.UtilizationSendButton.clicked.connect(self.utilization_call)

        self.EnterButton.clicked.connect(self.enter)
        self.ExitButton.clicked.connect(self.exit)
        self.MainStackedWidget.setCurrentIndex(0)
        self.UserStackedWidget.setCurrentIndex(0)
        self.AdminStackedWidget.setCurrentIndex(0)
        self.menu_button.clicked.connect(self.slide_left_menu)
        self.menu_button_1.clicked.connect(self.slide_left_menu)
        self.ExitButton_1.clicked.connect(self.exit)

        self.ApplyBtn.clicked.connect(self.open_tasks)
        self.RestartBtn.clicked.connect(self.clean_tasks_params)

        self.TaskSaveButton.clicked.connect(self.save_task)
        self.EquipmentSaveButton.clicked.connect(self.save_equipment)
        self.UserSaveButton.clicked.connect(self.save_user)
        self.AddEquipmentButton.clicked.connect(self.add_equipment)

    def slide_left_menu(self):
        width = self.side_menu.width()
        width_1 = self.side_menu_1.width()
        if width == 0:
            new_width = 160
        else:
            new_width = 0
        if width_1 == 0:
            new_width_1 = 160
        else:
            new_width_1 = 0
        self.animation = QtCore.QPropertyAnimation(self.side_menu, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.start()
        self.animation_1 = QtCore.QPropertyAnimation(self.side_menu_1, b"maximumWidth")
        self.animation_1.setDuration(250)
        self.animation_1.setStartValue(width_1)
        self.animation_1.setEndValue(new_width_1)
        self.animation_1.start()

    def enter(self):
        data = {"login": self.Login.text(),
                "password": self.Password.text()}
        response = requests.get(f'http://{HOST}:{str(PORT)}/login', params=data).json()
        if response['status'] == 'success':
            self.StatusLabel.setText('Добро пожаловать!')
            self.user = json.loads(response['user'])
            if self.user.get("is_admin"):
                self.MainStackedWidget.setCurrentIndex(2)
                self.user_nick_1.setText(f"{self.user.get('surname')} {self.user.get('name')}")
                self.user_nick_1.update()
                self.open_tasks()
                self.open_users()
                self.open_equipment()
            else:
                self.MainStackedWidget.setCurrentIndex(1)
                self.user_nick.setText(f"{self.user.get('surname')} {self.user.get('name')}")
                self.user_nick.update()
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


if __name__ == "__main__":
    db_session.global_init()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    main = Application()
    main.show()
    app.exec_()