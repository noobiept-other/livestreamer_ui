import sys
import json

from PySide.QtGui import QApplication, QLabel, QPushButton, QLineEdit, QHBoxLayout, QWidget, QTextEdit, QVBoxLayout, QListWidget, QListWidgetItem, QGridLayout
from PySide.QtCore import QProcess


from stream import Stream


'''
    to doo:

        - tell which ones of the urls in the links are live at the moment
'''



class LiveStreamer:

    def __init__( self ):

        url = QLineEdit()
        urlLabel = QLabel( 'Url' )
        messages = QTextEdit()
        messagesLabel = QLabel( 'Messages' )
        links = QListWidget()
        linksLabel = QLabel( 'Links' )
        clearMessages = QPushButton( 'Clear Messages' )
        addSelectedLink = QPushButton( 'Add Selected Link' )
        removeSelectedLink = QPushButton( 'Remove Selected Link' )

        messages.setReadOnly( True )

            # set the events

        url.returnPressed.connect( self.select_stream_from_entry )
        links.itemDoubleClicked.connect( self.select_stream_from_link )
        clearMessages.clicked.connect( self.clear_messages )
        addSelectedLink.clicked.connect( self.add_selected_link )
        removeSelectedLink.clicked.connect( self.remove_selected_link )

            # set the layouts

        mainLayout = QGridLayout()

            # first row
        mainLayout.addWidget( urlLabel, 0, 0, 1, 2 )    # spans 2 columns
        mainLayout.addWidget( linksLabel, 0, 2, 1, 2 )  # spans 2 columns

            # second row  (links widget occupies 2 rows and 2 columns)
        mainLayout.addWidget( url, 1, 0, 1, 2 )         # spans 2 columns
        mainLayout.addWidget( links, 1, 2, 2, 2 )

            # third row (messages widget occupies 2 columns)
        mainLayout.addWidget( messages, 2, 0, 1, 2 )

            # fourth row
        mainLayout.addWidget( messagesLabel, 3, 0 )
        mainLayout.addWidget( clearMessages, 3, 1 )
        mainLayout.addWidget( addSelectedLink, 3, 2 )
        mainLayout.addWidget( removeSelectedLink, 3, 3 )


        window = QWidget()

        window.setLayout( mainLayout )
        window.setWindowTitle( 'Live Streamer' )
        window.show()

        self.url_ui = url
        self.messages_ui = messages
        self.links_ui = links
        self.window_ui = window

        self.links = set()


    def select_stream_from_entry( self ):

        """
            Gets the values from the ui elements, and executes the program in json mode, to determine if the values are valid
        """
        url = self.url_ui.text()
        split_url = url.split()

        self.messages_ui.append( 'Trying to open stream: {}'.format( url ) )

        Stream( split_url, self.messages_ui )



    def select_stream_from_link( self, listWidgetItem ):

        url = listWidgetItem.text()
        split_url = url.split()

        self.messages_ui.append( 'Trying to open stream: {}'.format( url ) )


        Stream( split_url, self.messages_ui )



    def clear_messages( self ):

        self.messages_ui.setText( '' )


    def add_link( self, url ):

        """
            Adds a link to the link widget.

            Only adds if its not already present.
        """

        if url not in self.links:

            self.links.add( url )

            self.links_ui.addItem( url )


    def add_selected_link( self ):

        url = self.url_ui.text()

        if url:

            self.add_link( url )


    def remove_selected_link( self ):

        selectedItem = self.links_ui.currentItem()

        if selectedItem:

            self.links.remove( selectedItem.text() )

            currentRow = self.links_ui.currentRow()
            self.links_ui.takeItem( currentRow )



    def save( self ):

        """
            Save any data to a file (the links/etc)
        """

            # json doesn't have sets, so convert to a list
        linksList = list( self.links )

        saveJsonText = json.dumps( linksList )

        with open( 'data.txt', 'w', encoding= 'utf-8' ) as f:
            f.write( saveJsonText )


    def load( self ):

        """
            Load any saved data
        """

        try:
            file = open( 'data.txt', 'r', encoding= 'utf-8' )

        except FileNotFoundError:
            return


        linksList = json.loads( file.read() )

        file.close()


        for link in linksList:
            self.add_link( link )



if __name__ == '__main__':

    app = QApplication( sys.argv )

    streamer = LiveStreamer()

    streamer.load()

    app.aboutToQuit.connect( streamer.save )

    app.exec_()



