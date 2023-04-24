from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from messages import *
import sys, pickle, os
from csv_module import *
import r


class Require(qtw.QDialog):
    submit_tab = qtc.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setFixedSize(100, 50)
        self.setWindowTitle('Введите название вкладки')
        self.setWindowIcon(qtg.QIcon(qtg.QPixmap('./icons/museum.png')))



        ## layouts##
        main = qtw.QVBoxLayout()
        self.setLayout(main)
        upper = qtw.QHBoxLayout()
        lower = qtw.QGridLayout()
        main.addLayout(upper)
        main.addLayout(lower)
        ###//
        self.line_edit = qtw.QLineEdit()
        upper.addWidget(qtw.QLabel('Название вкладки'))
        upper.addWidget(self.line_edit)

        self.setMinimumSize(400, 100)

        ## buttons ##
        submit_b = qtw.QPushButton('Добавить', clicked=self.emit_text)
        cancel_b = qtw.QPushButton('Отмена', clicked=self.close)
        lower.addWidget(submit_b, 0, 0)
        lower.addWidget(cancel_b, 0, 2)


        self.show()

    def emit_text(self):
        self.submit_tab.emit(self.line_edit.text())
        self.close()
        

class list_window(qtw.QDialog):
    submitted = qtc.pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.setFixedSize(100,50)
        self.setWindowTitle('Введите название позиции')

        ## layouts##
        main = qtw.QVBoxLayout()
        self.setLayout(main)
        upper = qtw.QHBoxLayout()
        lower = qtw.QGridLayout()
        main.addLayout(upper)
        main.addLayout(lower)
        ###//
        self.line_edit = qtw.QLineEdit()
        upper.addWidget(qtw.QLabel('Позиция'))
        upper.addWidget(self.line_edit)

        self.setMinimumSize(400, 100)


        ## buttons ##
        submit_b = qtw.QPushButton('Добавить', clicked=self.onSubmit)
        cancel_b = qtw.QPushButton('Отмена', clicked=self.close)
        lower.addWidget(submit_b, 0, 0)
        lower.addWidget(cancel_b, 0, 2)


        self.show()

    def onSubmit(self):
        if self.line_edit.text() in Container_Widget.big_dict.keys():
            error()
        elif self.line_edit.text() != '':
          self.submitted.emit(self.line_edit.text())
          #Container_Widget.position_list.append(self.line_edit.text())
          #Container_Widget.list_tab_dict[self.line_edit.text()] = []
          #Container_Widget.tabs_for_each_position_in_a_list[self.line_edit.text()] = []

          #### BIG DICT #####
          Container_Widget.big_dict[self.line_edit.text()] = {}
          ## one more dict ##
          Container_Widget.TABLE_objects[self.line_edit.text()] = {}

        else:
            self.close()
        self.close()


class Container_Widget( qtw.QWidget):

    TABLE_objects = {}
    big_dict = {}

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 500)
        self.working_tab = qtw.QTabWidget()
        self.setWindowTitle('Клуб Друзей Музея')
        self.setMinimumSize(900, 600)


        ## layouts ##
        grid = qtw.QGridLayout()
        self.right_l = qtw.QVBoxLayout()
        self.grid = qtw.QGridLayout()
        h_layout = qtw.QHBoxLayout()

        left_layout = qtw.QVBoxLayout()

        add_b = qtw.QPushButton('Добавить', clicked=self.pop_up_window)
        delete_b = qtw.QPushButton('Удалить', clicked=self.delete_list_position)



        ## toolbar ##
        self.working_area_toolbar = qtw.QToolBar('Операции')
        self.working_area_toolbar.setOrientation(qtc.Qt.Vertical)
        #self.right_l.addWidget(self.working_area_toolbar)

       ## list  ##
        self.list = qtw.QListWidget()

        ## add horizontal_l
        self.setLayout(h_layout)

        # add left layout
        h_layout.addLayout(left_layout, 1)
        h_layout.addLayout(self.right_l, 9)
        h_layout.addLayout(self.grid)
        left_layout.addWidget(self.list)
        left_layout.addLayout(grid)
        self.grid.addWidget(self.working_area_toolbar, 0, 1)


        self.right_l.addWidget(self.working_tab)

        grid.addWidget(add_b, 0, 0)
        grid.addWidget(delete_b, 0, 2)



        delete_tab = qtg.QIcon(qtg.QPixmap(':/bin.png'))
        add_column = qtg.QIcon(qtg.QPixmap(':/column.png'))
        delete_row = qtg.QIcon(qtg.QPixmap(':/delete_row.png'))
        plus_page = qtg.QIcon(qtg.QPixmap(':/plus_page.png'))
        add_row = qtg.QIcon(qtg.QPixmap(':/row.png'))
        save_data = qtg.QIcon(qtg.QPixmap(':/save.png'))
        upload = qtg.QIcon(qtg.QPixmap(':/upload.png'))

        




        ## Adding a toolbar ###
        self.working_area_toolbar.addAction(plus_page, 'Добавить Вкладку', self.add_tab_to_working_area)
        self.working_area_toolbar.addAction(delete_tab, 'Удалить Вкладку', self.delete_from_working_area)
        self.working_area_toolbar.addAction(save_data, 'Сохранить', self.save_info)
        self.working_area_toolbar.addAction(add_row, 'Вставить строку', self.insert_row)
        self.working_area_toolbar.addAction(add_column, 'Вставить столбец', self.insert_column)
        self.working_area_toolbar.addAction(delete_row, 'Удалить строку/столбец', self.remove)
        self.working_area_toolbar.addAction(upload, 'Загрузить файл', self.load_file)

        #### SIGNALS ###
        self.list.itemClicked.connect(self.populate_tab)

        self.working_area_toolbar.setStyleSheet('spacing: 10px;'
                                                '')
        stylesheet = '''
        QToolButton:pressed{background-color: grey;}
        QToolButton:hover {background-color: #c5d9ed}       
        '''
        self.setStyleSheet(stylesheet)




        self.show()

    def closeEvent(self, event):
        if self.list:
            response = qtw.QMessageBox.question(
                self,
                'Сохранение',
                'Хотите ли вы сохранить файл?',
                qtw.QMessageBox.Yes | qtw.QMessageBox.No
            )
            if response == qtw.QMessageBox.Yes:
                self.save_info()
                event.accept()
            else:
                event.accept()




    def call_for_save(self):
        response = qtw.QMessageBox.question(
            self,
            'Сохранение',
            ' Хотите ли вы сохранить файл?'
        )
        if response == qtw.QMessageBox.Yes:
            self.save_info()
            self.show()
        else:
            self.close()


    def populate_tab(self, position):

        if self.big_dict.values():
            self.working_tab.clear()
            #position = self.list.currentItem().text()
            dict = self.TABLE_objects.get(position.text())
            if dict:
                for name in dict.keys():
                    object = dict.get(name)
                    self.working_tab.addTab(object, name)



    def add_tab_to_working_area(self):
        if self.list.count() > 0:
            self.require = Require()
            self.require.submit_tab.connect(self.ADD)


    def ADD(self, name):

            position_d = self.list.currentItem().text()
            n1 = self.big_dict.get(position_d)
            n2 = n1.keys()
            if name not in n2:
                self.container = qtw.QWidget()
                self.container.setLayout(qtw.QVBoxLayout())
                table = Table()
                self.objects_d = self.TABLE_objects[position_d]
                self.objects_d[name] = table


                ##################################
                self.row = table.rowCount()
                self.column = table.columnCount()
                self.l1 = []
                self.info = []
                for i in range(self.row):
                    self.info.append([])

                ##################################

                self.container.layout().addWidget(table)
                #self.tab_list.append(name)
                #print(self.tab_list)
                self.working_tab.addTab(self.container, name)
                #l = self.list_tab_dict.get(self.list.currentItem().text())

                #self.list_tab_dict.get(self.list.currentItem().text()).append(name)
                #print(self.list_tab_dict)


                #### BIG DICT ###
                ## adding tab_names in inner dictionary ###

                self.tab_names = self.big_dict.get(self.list.currentItem().text())
                self.tab_names[name] = self.info
                print(self.big_dict)

            else:
                error()



    def pop_up_window(self):
        self.pop = list_window()
        self.pop.submitted.connect(self.list.addItem)


    def delete_list_position(self):

        if self.list.selectedItems():
            text = self.list.currentItem().text()
            ind = self.list.currentRow()
            if text in self.big_dict.keys():
                self.big_dict.pop(text)
                self.TABLE_objects.pop(text)
                self.populate_list()
                if self.list.count() >= 2:
                    self.list.setCurrentRow(ind - 1)
                    t = self.list.currentItem()
                    self.populate_tab(t)
                else:
                    self.working_tab.clear()



    def populate_list(self):
         self.list.clear()
         items = self.big_dict.keys()
         self.list.addItems(items)




    def delete_from_working_area(self):

            selected = self.working_tab.currentIndex()
            name = self.working_tab.tabText(selected)
            #self.tab_list.remove(name)
            #self.list_tab_dict.get(self.list.currentItem().text()).remove(name)
            self.working_tab.removeTab(selected)


    def save_info(self):
        self.clean_big_d()
        for position in self.TABLE_objects.keys():
            dicts = self.TABLE_objects.get(position)
            for name in dicts.keys():
                value = dicts.get(name)
                value.setCurrentCell(0, 0)
                row_c = value.rowCount()
                column_c = value.columnCount()

                for row in range(row_c):
                    for column in range(column_c):
                        item = value.item(row, column)
                        tab_n = self.big_dict.get(position)
                        list = tab_n.get(name)
                        if item and item.text():
                            list[row].append(item.text())
                        else:
                            list[row].append('')
        self.save_()


    def insert_row(self):

        if self.working_tab.currentIndex() != -1 != 0:

            current_list_item = self.list.currentItem().text()


            selected = self.working_tab.currentIndex()
            tab_name = self.working_tab.tabText(selected)
            t1 = self.TABLE_objects.get(current_list_item)
            t_object = t1.get(tab_name)
            t_object.insertRow(t_object.currentRow())

            ## config in big_dict

            bd1_d = self.big_dict.get(current_list_item)
            bd2_l = bd1_d.get(tab_name)
            bd2_l.insert(t_object.currentRow()-1, [])



    def insert_column(self):
        if self.working_tab.currentIndex() != -1 != 0:
            current_list_item = self.list.currentItem().text()

            selected = self.working_tab.currentIndex()
            tab_name = self.working_tab.tabText(selected)
            t1 = self.TABLE_objects.get(current_list_item)
            t_object = t1.get(tab_name)
            t_object.insertColumn(t_object.currentColumn())

    def remove(self):
        if self.working_tab.currentIndex() != -1:

            current_item = self.list.currentItem().text()
            selected = self.working_tab.currentIndex()
            current_tab = self.working_tab.tabText(selected)
            t1 = self.TABLE_objects.get(current_item)
            if t1.keys():
                object = t1.get(current_tab)
                if object.currentRow():
                    row = object.currentRow()
                    object.removeRow(row)

                    bd1_d = self.big_dict.get(current_item)
                    bd2_l = bd1_d.get(current_tab)
                    del bd2_l[row]

                if object.currentColumn():
                    column = object.currentColumn()
                    object.removeColumn(column)

    def clean_big_d(self):
        for position in self.big_dict.values():
            for lists in position.values():
                for i in lists:
                    del i[:]

    def save_(self):
        if self.list.count() != 0:
            file_name, _ = qtw.QFileDialog.getSaveFileName(self,
                                                        'Сохранить Файл',
                                                        filter = 'Database (*.dat)')
            if file_name:
                with open(file_name, 'wb') as db:
                    pickle.dump(self.big_dict, db)
            else:
                pass
        else:
            qtw.QMessageBox.warning(
                self,
                'Предупреждение',
                'База данных пуста.'
                ' Создайте её.'
            )


    def load_file(self):
        try:


            filename, _ = qtw.QFileDialog.getOpenFileName(
                parent = self,
                caption = 'Выберите файл',
                directory = os.getcwd(),
                filter = 'dabases (*.dat)'
            )

            with open(filename, 'rb') as db:
                self.big_dict = pickle.load(db)





            keys = self.big_dict.keys()
            self.list.addItems(keys)
            for k in keys:
                self.TABLE_objects[k] = {}
                inner_dict_big_d = self.big_dict.get(k)         # inner dictionary with tab names as keys
                inner_d_T = self.TABLE_objects.get(k)
                for tab_name in inner_dict_big_d.keys():## all the keys in inner dict

                    list = inner_dict_big_d.get(tab_name)       # value as a big list
                    rows = len(list)
                    columns = len(list[0])
                    inner_d_T[tab_name] = qtw.QTableWidget(rows, columns)

            ### populate tables after loading ##

            for k in self.big_dict.keys():
                in_d_bigdic = self.big_dict.get(k)
                in_d_T = self.TABLE_objects.get(k)
                for inner_key in in_d_bigdic.keys():
                    big_list = in_d_bigdic.get(inner_key)
                    object = in_d_T.get(inner_key)
                    for row in range(len(big_list)):
                        for column in range(len(big_list[0])):
                            item = big_list[row][column]
                            object.setItem(row, column, qtw.QTableWidgetItem(item))
            self.list.clear()
        except:
            qtw.QMessageBox.critical(
                self,
                'Ошибка',
                'Выберите файл для загрузки.'
            )


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setWindowIcon(qtg.QIcon(':/museum.ico'))
    mw = Container_Widget()
    sys.exit(app.exec())




