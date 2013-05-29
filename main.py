import sys
import json

from PySide.QtGui import QApplication, QLabel, QPushButton, QLineEdit, QHBoxLayout, QWidget, QTextEdit, QVBoxLayout, QListWidget, QListWidgetItem, QGridLayout
from PySide.QtCore import QProcess


'''
    to doo:

        - be able to save the links (to be easy later to open the stream again, without having to write it again)
        - maybe only have a single entry (QLineEdit) for the url and quality?..
        - tell which qualities are available (and show them in a widget to be able to change easily between them)
        - be able to call the livestreamer with its other arguments (like '--version')
        - be able to clear the messages
'''




class LiveStreamer:

    def __init__( self ):

        url = QLineEdit()
        urlLabel = QLabel( 'Url' )
        quality = QLineEdit()
        qualityLabel = QLabel( 'Quality' )
        messages = QTextEdit()
        messagesLabel = QLabel( 'Messages' )
        links = QListWidget()
        linksLabel = QLabel( 'Links' )
        clearMessages = QPushButton( 'Clear Messages' )
        removeSelectedLink = QPushButton( 'Remove Selected Link' )


        links.addItem( 'test' )

        messages.setReadOnly( True )

            # set the events

        url.returnPressed.connect( self.parse_url )
        quality.returnPressed.connect( self.parse_url )
        links.itemClicked.connect( self.select_stream )
        clearMessages.clicked.connect( self.clear_messages )

            # set the layouts

        mainLayout = QGridLayout()

            # first row
        mainLayout.addWidget( urlLabel, 0, 0 )
        mainLayout.addWidget( qualityLabel, 0, 1 )
        mainLayout.addWidget( linksLabel, 0, 2 )

            # second row  (links widget occupies 2 rows)
        mainLayout.addWidget( url, 1, 0 )
        mainLayout.addWidget( quality, 1, 1 )
        mainLayout.addWidget( links, 1, 2, 2, 1 )

            # third row (messages widget occupies 2 columns)
        mainLayout.addWidget( messages, 2, 0, 1, 2 )

            # fourth row
        mainLayout.addWidget( messagesLabel, 3, 0 )
        mainLayout.addWidget( clearMessages, 3, 1 )
        mainLayout.addWidget( removeSelectedLink, 3, 2 )


        window = QWidget()

        window.setLayout( mainLayout )
        window.setWindowTitle( 'Live Streamer' )
        window.show()

        self.url_ui = url
        self.quality_ui = quality
        self.messages_ui = messages
        self.links_ui = links
        self.window_ui = window

        self.stream_url = ''
        self.stream_quality = ''


    def parse_url( self ):

        """
            Gets the values from the ui elements, and executes the program in json mode, to determine if the values are valid
        """

        url = self.url_ui.text()
        quality = self.quality_ui.text()

        self.messages_ui.append( 'Trying to open stream: {} {}'.format(url, quality) )

        arguments = []
        process_function = self.determine_if_valid_url  # function to call with the live-streamer's output


        if url:
            arguments.append( '--json' )
            arguments.append( url )


                # if quality isn't provided, the program gives the possible quality values
            if quality:
                arguments.append( quality )

            # if url is not given, show the help
        else:
            arguments.append( '--help' )
            process_function = self.show_messages   # nothing to check, so just show the messages the program gives


        self.stream_url = url
        self.stream_quality = quality

            # we'll call live-streamer two times, one to get the json info, and the other to actually start the stream
        process = QProcess()

        if url:
            self.process_json = process

        else:
            self.process = process

        process.setProcessChannelMode( QProcess.MergedChannels )
        process.start( 'livestreamer', arguments )
        process.readyReadStandardOutput.connect( process_function )


    def determine_if_valid_url( self ):

        """
            Determines if the url and quality are valid values
        """

        outputBytes = self.process_json.readAll().data()

        outputUnicode = outputBytes.decode( 'utf-8' )

        try:
            outputObject = json.loads( outputUnicode )

        except ValueError as errorMessage:
            print( errorMessage )
            self.messages_ui.append( outputUnicode )
            return


        if outputObject.get( 'error' ):

            self.messages_ui.append( outputObject[ 'error' ] )

            # the quality wasn't provided
        elif outputObject.get( 'streams' ):
            qualityAvailable = ''

            for quality in outputObject['streams']:
                qualityAvailable += quality + ' '


            self.messages_ui.append( 'Need to specify the quality of the stream.\nQualities Available: {}'.format( qualityAvailable ) )

        else:
            self.messages_ui.append( 'Opening the stream.' )
            self.start_stream()



    def start_stream( self ):

        """
            Assumes self.stream_url and self.stream_quality have valid values
        """

        process = QProcess()

        self.process = process

        process.setProcessChannelMode( QProcess.MergedChannels )
        process.start( 'livestreamer', [ self.stream_url, self.stream_quality ] )
        process.readyReadStandardOutput.connect( self.show_messages )



    def show_messages( self ):

        outputBytes = self.process.readAll().data()

        outputUnicode = outputBytes.decode( 'utf-8' )

        self.messages_ui.append( outputUnicode )


    def clear_messages( self ):

        self.messages_ui.setText( '' )


    def select_stream( self, listWidgetItem ):

        print( listWidgetItem.text() )





if __name__ == '__main__':

    app = QApplication( sys.argv )

    streamer = LiveStreamer()

    app.exec_()



