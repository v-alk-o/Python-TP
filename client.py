from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QErrorMessage
from fastapi import status
import webbrowser
import ipaddress
import requests
import sys



ZOOM = 11


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def locate_ip(self):
        ip = self.input_ip.text()
        api_key = self.input_api_key.text()
        hostname = self.input_hostname.text()

        try:
            ipaddress.ip_address(ip)
        except ValueError:
            self.error_dialog.showMessage("You must provide a valid IP address")
            return
        
        if not api_key:
            self.error_dialog.showMessage("You must provide an API key")
            return
        
        # Faire une regex puis une validation de l'adresse IP ou du nom de domaine
        # avec les modules Python adaptés
        if not hostname:
            self.error_dialog.showMessage("You must provide a hostname")
            return

        api_url = f"http://{hostname}/location/{ip}"
        headers = {"X-Api-Key" : api_key}

        try:
            response = requests.get(api_url, headers=headers)    
        except Exception as e:
            self.error_dialog.showMessage("Could not reach the API")
            return

        if response.status_code == status.HTTP_200_OK:
            longitude = response.json()['longitude']
            latitude = response.json()['latitude']
            openstreetmap_url = f"https://www.openstreetmap.org/#map={str(ZOOM)}/{str(latitude)}/{str(longitude)}"
            webbrowser.open(openstreetmap_url)
        else:
            self.error_dialog.showMessage("""Unknown error from Shodan API. 
                You either provided an invalid API key or no results were found for the IP address""")


    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(400, 400)

        self.label_ip = QLabel("Enter an IP address :", self)
        self.label_ip.setGeometry(15, 15, 200, 30)
        self.input_ip = QLineEdit(self)
        self.input_ip.setGeometry(15, 55, 200, 30)

        self.label_api_key = QLabel("Enter your API key :", self)
        self.label_api_key.setGeometry(15, 95, 200, 30)
        self.input_api_key = QLineEdit(self)
        self.input_api_key.setGeometry(15, 135, 200, 30)

        self.label_hostname = QLabel("Enter hostname of API :", self)
        self.label_hostname.setGeometry(15, 175, 200, 30)
        self.input_hostname = QLineEdit(self)
        self.input_hostname.setGeometry(15, 215, 200, 30)

        self.button_send = QPushButton("Send", self)
        self.button_send.setGeometry(15, 275, 50, 30)
        self.button_send.clicked.connect(self.locate_ip)

        self.error_dialog = QErrorMessage()

        self.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()

