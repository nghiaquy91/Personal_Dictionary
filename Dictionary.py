import sys
import time
import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QMainWindow, QApplication
from AddNewPhase import *


class MyForm(QMainWindow):
    tableCommand = ""

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Connect to Functions
        self.ui.pushButtonUpdate.clicked.connect(self.Update)
        self.show()

    def Update(self):
        try:
            conn = sqlite3.connect("database.db")
            print("Connected to database.db")
            # Create table
            tableCommand = "CREATE TABLE IF NOT EXISTS dictionary(" \
                           "phase TEXT," \
                           "meaning TEXT," \
                           "create_time TEXT);"
            print(tableCommand)
            c = conn.cursor()
            c.execute(tableCommand)
            conn.commit()

            # Check phase and Meaning
            if len(self.ui.plainTextEditPhase.toPlainText()) == 0 or \
                    len(self.ui.plainTextEditMeaning.toPlainText()) == 0:
                self.ui.labelResponse.setText("Điền đủ thông tin đi chứ, babe!")
            else:
                # Add data to database
                phase = "\'" + self.ui.plainTextEditPhase.toPlainText() + "\'"
                meaning = "\'" + self.ui.plainTextEditMeaning.toPlainText() + "\'"
                timestr = "\'" + str(time.time()) + "\'"
                tableCommand = "INSERT INTO dictionary (phase, meaning, create_time) VALUES (" + \
                               phase + "," + meaning + "," + timestr + ");"

                print(tableCommand)
                c = conn.cursor()
                c.execute(tableCommand)
                conn.commit()
                # Respond text

        except Error as e:
            print("Error while handling database: %s", str(e))
            pass
        finally:
            conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
