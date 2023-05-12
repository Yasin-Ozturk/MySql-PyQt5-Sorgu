import sys 
from ui_Spor import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from SQLconnect import connection,cursor
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt


class myApp(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(myApp,self).__init__()

        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)

        
        self.ui.btnKayitEkle.clicked.connect(self.Ekle)
        self.ui.btnListele.clicked.connect(self.Liste)
        self.ui.btnKayitSil.clicked.connect(self.KayitSil)
        self.ui.btnCikis.clicked.connect(self.close)
        self.ui.btnGuncelle.clicked.connect(self.Guncelle)
        self.ui.btnKayitAra.clicked.connect(self.Ara)
        self.ui.btn_toplam.clicked.connect(self.Toplam)

        
    def Ekle(self):
        self.lneTCK=self.ui.lneTCK.text()
        self.lneSporcuAdi=self.ui.lneSporcuAdi.text()
        self.lneSporcuSoyadi=self.ui.lneSporcuSoyadi.text()
        self.cmbKulup=self.ui.cmbKulup.currentText()
        self.Brans=self.ui.Brans.currentItem()
        if self.Brans == None:
            print("Branş Seçiniz")
        else:
            self.Brans=self.ui.Brans.currentItem().text()
            
        self.cmbCinsiyet=self.ui.cmbCinsiyet.currentText()
        self.DogumTarihi=self.ui.DogumTarihi.selectedDate().toString(QtCore.Qt.ISODate)
        if self.ui.MedeniHali.isChecked():
            self.MedeniHali="Evli"
        else :
            self.MedeniHali="Bekar"
        self.spbKilo=self.ui.spbKilo.value()
        
        sql="Insert Into sporexp (TcKimlikNo,Ad,Soyad,KulupAdi,Brans,Cinsiyet,DogumTarihi,MedeniHal,Kilo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values= (self.lneTCK,self.lneSporcuAdi,self.lneSporcuSoyadi,self.cmbKulup,self.Brans,self.cmbCinsiyet,self.DogumTarihi,self.MedeniHali,self.spbKilo)
        cursor.execute(sql,values)
        connection.commit()
        # connection.close() 
        
    def Liste(self):
        self.ui.tblBilgiler.clear()
        self.ui.tblBilgiler.setHorizontalHeaderLabels(('No','Sporcu Adı','Sporcu Soyadı','TC Kimlik No',\
                                                  'Cinsiyet','Doğum Tarihi','Branş','Medeni Hal',\
                                                      'Kulüp Adı','Sporcu Kilosu'))
        self.ui.tblBilgiler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        cursor.execute("SELECT * FROM sporexp")
        for satirIndeks, satirVeri in enumerate(cursor):
            for sutunIndeks, sutunVeri in enumerate(satirVeri):
                self.ui.tblBilgiler.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))

    def KayitSil(self):
        sil = self.ui.lneSil.text()
        # mycursor = connection.cursor()
        sql = "DELETE FROM sporexp WHERE id = %s"
        values = (sil,)    
        cursor.execute(sql,values)
        connection.commit()
        # print(cursor.rowcount, "kayıt silindi.")
       
    def Guncelle(self):
        self.lneTCK=self.ui.lneTCK.text()
        self.lneSporcuAdi=self.ui.lneSporcuAdi.text()
        self.lneSporcuSoyadi=self.ui.lneSporcuSoyadi.text()
        self.cmbKulup=self.ui.cmbKulup.currentText()
        self.Brans=self.ui.Brans.currentItem()
        if self.Brans == None:
            pass
        else:
            self.Brans=self.ui.Brans.currentItem().text()
            
        self.cmbCinsiyet=self.ui.cmbCinsiyet.currentText()
        self.DogumTarihi=self.ui.DogumTarihi.selectedDate().toString(QtCore.Qt.ISODate)
        if self.ui.MedeniHali.isChecked():
            self.MedeniHali="Evli"
        else :
            self.MedeniHali="Bekar"
        self.spbKilo=self.ui.spbKilo.value()
        
        kayitid = self.ui.lneGuncel.text()
        sql = "Select * From sporexp Where id=%s"
        value = (kayitid,)
        cursor.execute(sql,value)
        old_data = cursor.fetchone()

        new_data = (
            self.lneSporcuAdi if self.lneSporcuAdi else old_data[1],
            self.lneSporcuSoyadi if self.lneSporcuSoyadi else old_data[2],
            self.lneTCK if self.lneTCK else old_data[3],
            self.cmbCinsiyet if self.cmbCinsiyet else old_data[4],
            self.DogumTarihi if self.DogumTarihi else old_data[5],
            self.Brans if self.Brans else old_data[6],
            self.MedeniHali if self.MedeniHali else old_data[7],
            self.cmbKulup if self.cmbKulup else old_data[8],
            self.spbKilo if self.spbKilo else old_data[9],
            old_data[0] 
            )
        sql = "UPDATE sporexp SET Ad=%s,Soyad=%s,TcKimlikNo=%s,Cinsiyet=%s,DogumTarihi=%s,Brans=%s,MedeniHal=%s,KulupAdi=%s,Kilo=%s WHERE id = %s"
        cursor.execute(sql, new_data)
        connection.commit()
    
    def Ara(self):
        KayitAra = self.ui.lneAra.text()
        sql = "SELECT * FROM sporexp WHERE CONCAT(Ad,Soyad,TcKimlikNo,Cinsiyet,DogumTarihi,Brans,MedeniHal,KulupAdi,Kilo) LIKE %s"
        val = ("%{}%".format(KayitAra),)
        cursor.execute(sql, val)
  
        myresult = cursor.fetchall()
        row_count = len(myresult)
        column_count = len(myresult[0])
        self.ui.tblBilgiler.clear()
        self.ui.tblBilgiler.setHorizontalHeaderLabels(('No','Sporcu Adı','Sporcu Soyadı','TC Kimlik No',\
                                                  'Cinsiyet','Doğum Tarihi','Branş','Medeni Hal',\
                                                      'Kulüp Adı','Sporcu Kilosu'))

        for row in range(row_count):
            for column in range(column_count):
                item = QTableWidgetItem(str(myresult[row][column]))
                self.ui.tblBilgiler.setItem(row, column, item)
                
    def Toplam(self):
        cursor.execute("Select Count(*) From sporexp") 
        result = cursor.fetchone()
        toplam = result[0]
        self.ui.lbl_toplam.setText(str(toplam))

    def closeEvent(self,event):
        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "kapatma", "Cikmak istediginize emin misiniz?")

        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'evet')
        cancel.setText(u'hayir')
        # msg.setDetailedText('sdfsdff')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
            connection.close()
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.ui.btnListele.click()

        if event.key() == Qt.Key_Escape:
            self.ui.btnCikis.click()

def app():
    app=QtWidgets.QApplication(sys.argv)

    win=myApp()
    win.show()
    sys.exit(app.exec_())  
    

app()



