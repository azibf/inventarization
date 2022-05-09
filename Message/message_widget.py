from PyQt5 import QtWidgets, uic


class Message(QtWidgets.QDialog):
    def __init__(self, val=0):
        super(Message, self).__init__()
        uic.loadUi('Message\message.ui', self)
        if val == -1:
            self.ResultLabel.setText('Ошибка!')
        if val == 0:
            self.ResultLabel.setText('Заявка успешно отправлена')
        if val == 1:
            self.ResultLabel.setText('Ошибка отправки!')
        if val == 2:
            self.ResultLabel.setText('Повторяющиеся номера!')
        if val == 3:
            self.ResultLabel.setText('Количество номер не совпадает с указанным количеством!')

        self.show()
