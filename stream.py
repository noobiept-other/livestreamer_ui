import json

from PySide.QtCore import QProcess


ALL_STREAMS = []


class Stream:

    def __init__( self, arguments ):

        self.arguments = arguments


    def start( self, messageElement ):

        global ALL_STREAMS

        print(len(ALL_STREAMS))

        process = QProcess()

        self.process = process
        self.messageElement = messageElement

        process.setProcessChannelMode( QProcess.MergedChannels )
        process.start( 'livestreamer', self.arguments )
        process.readyReadStandardOutput.connect( self.show_messages )
        process.finished.connect( self.clear )

        ALL_STREAMS.append( self )



    def is_online( self, tableWidgetItem ):

        process = QProcess()

        self.process_is_online = process
        self.table_widget_item = tableWidgetItem

        arguments = [ '--json' ] + self.arguments

        process.setProcessChannelMode( QProcess.MergedChannels )
        process.start( 'livestreamer', arguments )
        process.readyReadStandardOutput.connect( self.is_online_callback )
        process.finished.connect( self.clear )

        ALL_STREAMS.append( self )


    def is_online_callback( self ):

        outputBytes = self.process_is_online.readAll().data()

        outputUnicode = outputBytes.decode( 'utf-8' )

        try:
            outputObject = json.loads( outputUnicode )

        except ValueError as errorMessage:
            print( errorMessage )
            return


        if outputObject.get( 'error' ):

            onlineStatus = 'Off'
        else:
            onlineStatus = 'On'


        itemWidget = self.table_widget_item

        itemWidget.setText( onlineStatus )



    def clear( self ):

        global ALL_STREAMS


        #ALL_STREAMS.remove( self )     #HERE its crashing the program


    def show_messages( self ):

        outputBytes = self.process.readAll().data()

        outputUnicode = outputBytes.decode( 'utf-8' )

        self.messageElement.append( outputUnicode )
