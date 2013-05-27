import sys

from PySide.QtGui import QApplication, QLabel, QPushButton, QLineEdit, QHBoxLayout, QWidget, QTextEdit, QVBoxLayout
from PySide.QtCore import QProcess


'''
    to doo:

        - be able to save the links (to be easy later to open the stream again, without having to write it again)
        - maybe only have a single entry (QLineEdit) for the url and quality?..
'''




class LiveStreamer:

    def __init__(self):

        url = QLineEdit()
        quality = QLineEdit()
        messages = QTextEdit()

        url.returnPressed.connect( self.start_stream )
        quality.returnPressed.connect( self.start_stream )

        mainLayout = QVBoxLayout()
        urlLayout = QHBoxLayout()

        urlLayout.addWidget( url )
        urlLayout.addWidget( quality )

        mainLayout.addLayout( urlLayout )
        mainLayout.addWidget( messages )

        window = QWidget()

        window.setLayout( mainLayout )
        window.setWindowTitle( 'Live Streamer' )
        window.show()

        self.url = url
        self.quality = quality
        self.messages = messages
        self.window = window


    def start_stream(self):

        url = self.url.text()
        quality = self.quality.text()

        program = 'livestreamer'

        process = QProcess()

        self.process = process

        process.setProcessChannelMode( QProcess.MergedChannels )
        process.start( program, [ url, quality ] )
        process.readyReadStandardOutput.connect( self.showMessages )


    def showMessages( self ):

        outputBytes = self.process.readAll().data()

        outputUnicode = outputBytes.decode( 'utf-8' )

        self.messages.append( outputUnicode )



if __name__ == '__main__':

    app = QApplication( sys.argv )

    streamer = LiveStreamer()

    app.exec_()
