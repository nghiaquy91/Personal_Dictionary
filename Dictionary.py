import sys
import time
import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QMainWindow, QApplication
from AddNewPhase import *

# Define the connection to database
conn = None
# Define the number of total items of dictionary
item_total = 0


class MyForm(QMainWindow):
    tableCommand = ""

    def __init__(self):
        global conn
        global item_total
        item_total = 0
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Connect to Functions
        self.ui.pushButtonUpdate.clicked.connect(self.update_data)
        self.ui.pushButtonLoad.clicked.connect(self.load_data)
        # Create Database and tables
        try:
            conn = sqlite3.connect("database.db")
            print("Connected to database.db")
            # Create Dictionary table
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS Dictionary("
                      "ID INTEGER,"
                      "Phase TEXT,"
                      "Meaning TEXT,"
                      "Create_Time TEXT);")
            # Create Metadata table
            c.execute("CREATE TABLE IF NOT EXISTS Metadata("
                      "Total_Items INTEGER);")
            # Got the total of items in dictionary
            c.execute("SELECT * FROM Metadata;")
            conn.commit()
            ret = c.fetchone()
            if ret is None:
                item_total = 0
                # Add the item_total value to table
                c.execute("INSERT INTO Metadata VALUES (0);")
                conn.commit()
            else:
                item_total = ret[0]
            print(item_total)

        except Error as e:
            print("Error while create tables in database:", str(e))
        finally:
            conn.close()
        self.show()

    def update_data(self):
        global conn
        global item_total
        # Check phase and Meaning
        if len(self.ui.plainTextEditPhase.toPlainText()) == 0 or \
                len(self.ui.plainTextEditMeaning.toPlainText()) == 0:
            self.ui.labelResponse.setText("Please add enough information, babe!")
        else:
            item_total += 1
            phase = "\'" + self.ui.plainTextEditPhase.toPlainText() + "\'"
            meaning = "\'" + self.ui.plainTextEditMeaning.toPlainText() + "\'"
            time_str = "\'" + str(time.time()) + "\'"

            try:
                conn = sqlite3.connect("database.db")
                c = conn.cursor()
                # Add data to database
                c.execute("INSERT INTO Dictionary (ID, Phase, Meaning, Create_Time) VALUES (" +
                          str(item_total) + "," + phase + "," + meaning + "," + time_str + ");")
                # Update metadata
                c.execute("UPDATE Metadata SET Total_Items = " + str(item_total) + ";")
                # Create a table of this phase
                c.execute("CREATE TABLE IF NOT EXISTS P" + str(item_total) + "("
                          "Time TEXT,"
                          "Remember_Point INTEGER);")
                # Update the first point - 100: Totally Remember
                c.execute("INSERT INTO P" + str(item_total) + " (Time, Remember_Point) VALUES (" +
                          time_str + ", 100);")
                conn.commit()
                # Respond text
                self.ui.labelResponse.setText("Update text to the Database Successful!")
            except Error as e:
                print("Error while handling database:", str(e))
                pass
            finally:
                conn.close()

    def load_data (self):
        try:
            # Got all data from database
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("SELECT * FROM Dictionary;")
            conn.commit()
            dic_data = c.fetchall()
            # Close database
            conn.close()
            print(dic_data)
            # Display data to table view
            self.ui.tableWidgetData.setRowCount(len(dic_data))
            self.ui.tableWidgetData.setColumnCount(len(dic_data[0]))
            # Insert data to table
            for row_num, row_data in enumerate(dic_data):
                for col_num, data in enumerate(row_data):
                    print("row_num:", row_num)
                    print("col_num:", col_num)
                    if col_num != 3:
                        self.ui.tableWidgetData.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(data)))
                    else:
                        curr_time = time.time()
                        print (int(curr_time - float(data)))
                        diff_sec = int(curr_time - float(data))
                        diff_day = 0
                        diff_h = 0
                        diff_m = 0
                        diff_day_str = ""
                        if diff_sec >= 86400:
                            diff_day = diff_sec // 86400
                            diff_sec = diff_sec %  86400
                            diff_day_str += str(diff_day) + " days "
                        if diff_sec >= 3600:
                            diff_h = diff_sec // 3600
                            diff_sec = diff_sec % 3600
                            diff_day_str += str(diff_h) + " hours "
                        if diff_sec >= 60:
                            diff_m = diff_sec // 60
                            diff_sec = diff_sec % 60
                            diff_day_str += str(diff_m) + " mins " + str(diff_sec) + " secs"
                        self.ui.tableWidgetData.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(diff_day_str))

        except:
            pass
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
