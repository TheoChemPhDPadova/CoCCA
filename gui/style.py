 
def set_style(self):
  self.setStyleSheet("""
            QPushButton{
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f6f7fa, stop: 1 #dadbde);
                min-width: 80px;
            }

            QWidget{

                background-color:#F34



            }

             QMainWindow{

                background-color:#F34



            }

            
                           """)