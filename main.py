import sys

from PySide.QtGui import QApplication, QLabel, QPushButton, QLineEdit, QHBoxLayout, QWidget, QTextEdit, QVBoxLayout
from PySide.QtCore import QProcess


'''
    to doo:

        - be able to save the links (to be easy later to open the stream again, without having to write it again)
        - maybe only have a single entry (QLineEdit) for the url and quality?..
'''




URL = None
QUALITY = None
PROCESS = None
MESSAGES = None


def go():

    global URL
    global QUALITY
    global MESSAGES


    app = QApplication( sys.argv )

    URL = QLineEdit()
    QUALITY = QLineEdit()
    MESSAGES = QTextEdit()



    URL.returnPressed.connect( start_stream )
    QUALITY.returnPressed.connect( start_stream )

    mainLayout = QVBoxLayout()
    urlLayout = QHBoxLayout()

    urlLayout.addWidget( URL )
    urlLayout.addWidget( QUALITY )

    mainLayout.addLayout( urlLayout )
    mainLayout.addWidget( MESSAGES )


    window = QWidget()

    window.setLayout( mainLayout )
    window.setWindowTitle( 'Live Streamer' )
    window.show()

    app.exec_()



def start_stream():

    global PROCESS

    url = URL.text()
    quality = QUALITY.text()

    # print( 'starting: {} {}'.format( url, quality ) )

    program = 'livestreamer'

    PROCESS = QProcess()
    PROCESS.setProcessChannelMode( QProcess.MergedChannels )

    PROCESS.start( program, [ url, quality ] )

    PROCESS.readyReadStandardOutput.connect( showMessages )



def showMessages():

    outputBytes = PROCESS.readAll().data()

    outputUnicode = outputBytes.decode( 'utf-8' )

    MESSAGES.append( outputUnicode )


if __name__ == '__main__':

    go()
