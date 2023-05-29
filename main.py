import math
import os
import random
import smtplib
import sqlite3
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Tuple, Union

import cv2 as cv
import numpy as np
import pytesseract
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QRadioButton
from gtts import gTTS


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.pencere4 = None
        self.edit_text = None
        self.remember = None
        self.password_label = None
        self.user = None
        self.register = None
        self.login = None
        self.forgot = None
        self.password = None
        self.username = None
        self.cursor = None
        self.connection = None
        self.create_connection()
        self.init_ui()

    def create_connection(self):
        self.connection = sqlite3.connect("Database.db", timeout=10)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Members (Username TEXT,Password TEXT,Name TEXT,Surname TEXT, "
                            "Mail TEXT)")
        self.connection.commit()

    def init_ui(self):
        self.username = QtWidgets.QLineEdit()
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.forgot = QtWidgets.QPushButton("Şifremi Unuttum!")
        self.login = QtWidgets.QPushButton("Giriş")
        self.register = QtWidgets.QPushButton("Kaydol")
        self.user = QtWidgets.QLabel("Kullanıcı Adı :")
        self.password_label = QtWidgets.QLabel("Şifre            :")
        self.remember = QtWidgets.QCheckBox("Hatırla")
        self.setWindowTitle("Kullanıcı Girişi")
        self.edit_text = QtWidgets.QLabel("")

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.user)
        h_box.addWidget(self.username)
        h_box.addStretch()

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.password_label)
        h_box2.addWidget(self.password)
        h_box2.addStretch()

        h_box5 = QtWidgets.QHBoxLayout()
        h_box5.addStretch()
        h_box5.addWidget(self.edit_text)
        h_box5.addStretch()

        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addStretch()
        h_box3.addWidget(self.remember)
        h_box3.addWidget(self.forgot)
        h_box3.addStretch()

        h_box4 = QtWidgets.QHBoxLayout()
        h_box4.addStretch()
        h_box4.addWidget(self.login)
        h_box4.addWidget(self.register)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addLayout(h_box2)
        v_box.addLayout(h_box5)
        v_box.addLayout(h_box3)
        v_box.addStretch()
        v_box.addLayout(h_box4)

        self.user.setFixedSize(60, 20)
        self.username.setFixedSize(120, 20)
        self.password_label.setFixedSize(60, 20)
        self.password.setFixedSize(120, 20)

        self.setLayout(v_box)

        self.setGeometry(800, 300, 300, 300)
        self.setFixedSize(300, 300)

        self.show()

        self.forgot.clicked.connect(self.yenile)
        self.login.clicked.connect(self.sign)
        self.register.clicked.connect(self.kayit)

    @staticmethod
    def yenile():
        pencere2.show()

    @staticmethod
    def kayit():
        pencere3.show()

    def sign(self):
        ad = self.username.text()
        parol = self.password.text()

        self.cursor.execute("SELECT * FROM Members WHERE Username=? AND Password=?", (ad, parol))

        data = self.cursor.fetchall()

        if len(data) == 0:
            self.edit_text.setText("Kullanıcı Adı veya Parola Hatalı...")
        else:
            self.edit_text.setText("Hoş Geldiniz.")
            self.close()
            self.pencere4 = Language()


class ForgotPasswordWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.cursor = None
        self.baglanti = None
        self.mai = None
        self.sifre = None
        self.yazi_alani = None
        self.gonder = None
        self.mail = None
        self.email = None
        self.gorsel()

    def gorsel(self):
        self.email = QtWidgets.QLabel("E-Mail :")
        self.mail = QtWidgets.QLineEdit()
        self.gonder = QtWidgets.QPushButton("Gönder")
        self.yazi_alani = QtWidgets.QLabel("")

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.email)
        h_box.addWidget(self.mail)
        h_box.addStretch()

        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addStretch()
        h_box3.addWidget(self.yazi_alani)
        h_box3.addStretch()

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.gonder)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()
        v_box.addLayout(h_box)
        v_box.addLayout(h_box3)
        v_box.addLayout(h_box2)
        v_box.addStretch()

        self.setLayout(v_box)

        self.setWindowTitle("Şifre Yenileme")

        self.gonder.clicked.connect(self.yolla)

    def yolla(self):
        self.sifre = str(random.randint(1000, 9999))
        self.mai = self.mail.text()
        mesaj = MIMEMultipart()
        mesaj["From"] = "yasinokat@gmail.com"
        mesaj["To"] = self.mai
        mesaj["Subject"] = "Şifre Yenileme"
        yazi = "Mail Şifresi : "
        mesaj_govdesi = MIMEText(yazi + self.sifre, "plain")

        mesaj.attach(mesaj_govdesi)

        try:
            mail = smtplib.SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login("yasinokat@gmail.com", "yasinokat")
            mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
            self.yazi_alani.setText("Şifre Maile Gönderildi.")
            mail.close()

        except:
            self.yazi_alani.setText("Mail Gönderilemedi.")

        self.baglanti = sqlite3.connect("Database.db", timeout=10)
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("UPDATE Members SET Password=? WHERE Mail=?", (self.sifre, self.mai))
        self.baglanti.commit()


class SignUpWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.gorsel()

    def gorsel(self):
        self.ad = QtWidgets.QLabel("İsim             :")
        self.soyad = QtWidgets.QLabel("Soyisim        :")
        self.kullanici_adi = QtWidgets.QLabel("Kullanıcı Adı :")
        self.email = QtWidgets.QLabel("E-Mail          :")
        self.sifre = QtWidgets.QLabel("Şifre            :")
        self.isim = QtWidgets.QLineEdit()
        self.soy = QtWidgets.QLineEdit()
        self.kullanici = QtWidgets.QLineEdit()
        self.mail = QtWidgets.QLineEdit()
        self.parola = QtWidgets.QLineEdit()
        self.kaydol = QtWidgets.QPushButton("Kaydet!")
        self.yazi_alani = QtWidgets.QLabel("")

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.ad)
        h_box.addWidget(self.isim)
        h_box.addStretch()

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(self.soyad)
        h_box2.addWidget(self.soy)
        h_box2.addStretch()

        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addStretch()
        h_box3.addWidget(self.kullanici_adi)
        h_box3.addWidget(self.kullanici)
        h_box3.addStretch()

        h_box4 = QtWidgets.QHBoxLayout()
        h_box4.addStretch()
        h_box4.addWidget(self.email)
        h_box4.addWidget(self.mail)
        h_box4.addStretch()

        h_box5 = QtWidgets.QHBoxLayout()
        h_box5.addStretch()
        h_box5.addWidget(self.sifre)
        h_box5.addWidget(self.parola)
        h_box5.addStretch()

        h_box7 = QtWidgets.QHBoxLayout()
        h_box7.addStretch()
        h_box7.addWidget(self.yazi_alani)
        h_box7.addStretch()

        h_box6 = QtWidgets.QHBoxLayout()
        h_box6.addStretch()
        h_box6.addWidget(self.kaydol)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addLayout(h_box2)
        v_box.addLayout(h_box3)
        v_box.addLayout(h_box4)
        v_box.addLayout(h_box5)
        v_box.addStretch()
        v_box.addLayout(h_box7)
        v_box.addStretch()
        v_box.addStretch()
        v_box.addLayout(h_box6)

        self.setLayout(v_box)

        self.ad.setFixedSize(65, 20)
        self.isim.setFixedSize(120, 20)
        self.soyad.setFixedSize(65, 20)
        self.soy.setFixedSize(120, 20)
        self.kullanici_adi.setFixedSize(65, 20)
        self.kullanici.setFixedSize(120, 20)
        self.email.setFixedSize(65, 20)
        self.mail.setFixedSize(120, 20)
        self.sifre.setFixedSize(65, 20)
        self.parola.setFixedSize(120, 20)

        self.setWindowTitle("           KAYDOL            ")
        self.setFixedSize(300, 300)

        self.kaydol.clicked.connect(self.yeni)

    def yeni(self):
        ad = self.isim.text()
        soyad = self.soy.text()
        kullan = self.kullanici.text()
        parol = self.parola.text()
        mai = self.mail.text()

        self.im = sqlite3.connect("Database.db", timeout=10)
        self.curs = self.im.cursor()
        self.curs.execute("SELECT * FROM Members WHERE Username=?", (kullan,))
        data = self.curs.fetchall()

        if len(data) == 0:
            self.yazi_alani.setText("Bilgileriniz Kaydedildi.")
            self.curs.execute("INSERT INTO Members VALUES (?,?,?,?,?)", (kullan, parol, ad, soyad, mai))
            self.im.commit()
        else:
            self.yazi_alani.setText("Kullanıcı Adı Alınmış.")


class Language(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Select a Language")
        self.languages = {"Turkish": "tr", "English": "en", "German": "de", "French": "fr"}
        self.yazi_alani = QLabel("Select a Language")

        self.radio_buttons = []
        for language in self.languages:
            radio_button = QRadioButton(language)
            self.radio_buttons.append(radio_button)

        self.sonuc = QLabel("")
        self.buton = QPushButton("Select!")

        v_box = QVBoxLayout()
        v_box.addWidget(self.yazi_alani)
        for radio_button in self.radio_buttons:
            v_box.addWidget(radio_button)
        v_box.addWidget(self.sonuc)
        v_box.addWidget(self.buton)
        v_box.addStretch()

        self.setLayout(v_box)
        self.setGeometry(800, 300, 300, 300)
        self.setFixedSize(300, 300)

        self.buton.clicked.connect(self.click)
        self.show()

    def click(self):
        selected_language = None
        for radio_button in self.radio_buttons:
            if radio_button.isChecked():
                selected_language = self.languages[radio_button.text()]
                print(f"{radio_button.text()} language is selected")
                break

        if selected_language is None:
            print("No language selected.")
            return

        global qwe
        qwe = selected_language
        self.close()
        ProjectEEE()


class ProjectEEE:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        self.run()

    def rescale_frame(self, frame, scale):
        height = int(frame.shape[0] * scale)
        width = int(frame.shape[1] * scale)
        dimensions = (width, height)
        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    def rotate(self, image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]):
        old_width, old_height = image.shape[:2]
        angle_radian = math.radians(angle)
        width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
        height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
        rot_mat[1, 2] += (width - old_width) / 2
        rot_mat[0, 2] += (height - old_height) / 2
        return cv.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)

    def capture_frame(self, url):
        capture = cv.VideoCapture(url)
        while True:
            is_true, frame = capture.read()
            if not is_true:
                break
            resized = self.rescale_frame(frame, scale=0.5)
            rotated_frame = self.rotate(resized, -90, None)
            cv.imshow("Resized", rotated_frame)
            key = cv.waitKey(20)
            if key == ord("q"):
                break
            elif key == ord("a"):
                rotated = self.rotate(resized, -90, (0, 0, 0))
                cv.imwrite("capture.jpg", rotated)
                break

        capture.release()
        cv.destroyAllWindows()

    def process_captured_image(self):
        captured_image = cv.imread("capture.jpg")
        capture_image_resized = self.rescale_frame(captured_image, scale=1)
        cv.imshow("captured_image", capture_image_resized)
        cv.waitKey(0)
        cv.destroyAllWindows()

        gray = cv.cvtColor(capture_image_resized, cv.COLOR_BGR2GRAY)
        cv.imshow("captured_image", capture_image_resized)
        cv.imshow("Gray", gray)
        cv.waitKey(0)
        cv.destroyAllWindows()

        kernel = np.ones((2, 2), np.uint8)
        eroded = cv.erode(gray, kernel, iterations=1)
        cv.imshow("captured_image", capture_image_resized)
        cv.imshow("Gray", gray)
        cv.imshow("Thicken Letters", eroded)
        cv.imwrite("Thicken Letters.jpg", eroded)
        cv.waitKey(0)
        cv.destroyAllWindows()

        rgb_planes = cv.split(eroded)
        result_planes = []
        result_norm_planes = []

        for plane in rgb_planes:
            dilated_img = cv.dilate(plane, np.ones((7, 7), np.uint8))
            bg_img = cv.medianBlur(dilated_img, 21)
            diff_img = 255 - cv.absdiff(plane, bg_img)
            norm_img = cv.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1)
            result_planes.append(diff_img)
            result_norm_planes.append(norm_img)

        result = cv.merge(result_planes)
        result_norm = cv.merge(result_norm_planes)

        cv.imwrite('shadows_out.png', result)
        cv.imwrite('shadows_out_norm.png', result_norm)

        cv.imshow('shadows_out', result)
        cv.imshow('shadows_out_norm', result_norm)
        cv.waitKey(0)
        cv.destroyAllWindows()

        text = pytesseract.image_to_string("shadows_out_norm.png", lang="tur")
        print(text)

        with open("text.txt", "w", encoding="utf-8") as file:
            file.write(text)

        output = gTTS(text=text, lang=qwe, slow=False)
        output.save("output.mp3")
        os.system("start output.mp3")
        os.system("text.txt")

    def run(self):
        url = "https://192.168.1.167:8080/video"
        self.capture_frame(url)
        self.process_captured_image()


if __name__ == '__main__':
    uygulama = QtWidgets.QApplication(sys.argv)
    pencere = MainWindow()
    pencere2 = ForgotPasswordWindow()
    pencere3 = SignUpWindow()
    sys.exit(uygulama.exec_())
