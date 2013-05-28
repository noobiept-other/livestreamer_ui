import sys

from PySide.QtGui import QApplication, QLabel, QPushButton, QLineEdit, QHBoxLayout, QWidget, QTextEdit, QVBoxLayout, QListWidget, QListWidgetItem
from PySide.QtCore import QProcess


'''
    to doo:

        - be able to save the links (to be easy later to open the stream again, without having to write it again)
        - maybe only have a single entry (QLineEdit) for the url and quality?..
        - tell which qualities are available
'''




class LiveStreamer:

    def __init__( self ):

        url = QLineEdit()
        quality = QLineEdit()
        messages = QTextEdit()
        links = QListWidget()


        links.addItem( 'test' )


        messages.setReadOnly( True )

            # set the events

        url.returnPressed.connect( self.start_stream )
        quality.returnPressed.connect( self.start_stream )
        links.itemClicked.connect( self.select_stream )

        mainLayout = QVBoxLayout()
        urlLayout = QHBoxLayout()

        urlLayout.addWidget( url )
        urlLayout.addWidget( quality )

        mainLayout.addLayout( urlLayout )
        mainLayout.addWidget( messages )
        mainLayout.addWidget( links )

        window = QWidget()

        window.setLayout( mainLayout )
        window.setWindowTitle( 'Live Streamer' )
        window.show()

        self.url = url
        self.quality = quality
        self.messages = messages
        self.links = links
        self.window = window


    def start_stream( self ):

        url = self.url.text()
        quality = self.quality.text()

        arguments = []

            # don't add if the argument isn't provided (if url is not given, the program gives a 'help' text)
        if url:
            arguments.append( url )

            # if quality isn't provided, the program gives the possible quality values
        if quality:

            arguments.append( quality )

        else:
            self.messages.append( '< Need to specify the quality of the stream. >' )


        program = 'livestreamer'

        process = QProcess()

        self.process = process

        process.setProcessChannelMode( QProcess.MergedChannels )
        process.start( program, arguments )
        process.readyReadStandardOutput.connect( self.show_messages )


    def show_messages( self ):

        outputBytes = self.process.readAll().data()

        outputUnicode = outputBytes.decode( 'utf-8' )

        self.messages.append( outputUnicode )


    def select_stream( self, listWidgetItem ):

        print( listWidgetItem.text() )





if __name__ == '__main__':

    app = QApplication( sys.argv )

    streamer = LiveStreamer()

    app.exec_()



