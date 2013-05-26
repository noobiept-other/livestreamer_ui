import sys
import subprocess

from PySide.QtGui import QApplication, QLabel, QPushButton, QLineEdit, QHBoxLayout, QWidget

'''
    to doo:

        - add a text element that shows the messages from the livestreamer program
        - be able to save the links (to be easy later to open the stream again, without having to write it again)
        - maybe only have a single entry (QLineEdit) for the url and quality?..
'''



URL = None
QUALITY = None
PROCESS = None


def go():

    global URL
    global QUALITY

    app = QApplication( sys.argv )

    URL = QLineEdit()
    QUALITY = QLineEdit()

    URL.returnPressed.connect( start_stream )
    QUALITY.returnPressed.connect( start_stream )

    layout = QHBoxLayout()

    layout.addWidget( URL )
    layout.addWidget( QUALITY )


    window = QWidget()

    window.setLayout( layout )
    window.setWindowTitle( 'Live Streamer' )
    window.show()

    app.exec_()



def start_stream():

    global PROCESS

    url = URL.text()
    quality = QUALITY.text()

    print( 'starting: {} {}'.format( url, quality ) )

    program = 'livestreamer'

    subprocess.call([ program, url, quality ])




if __name__ == '__main__':

    go()