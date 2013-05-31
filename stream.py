from PySide.QtCore import QProcess


ALL_STREAMS = []


class Stream:

    def __init__( self, arguments, textEditElement ):

        global ALL_STREAMS

        print(len(ALL_STREAMS))

        process = QProcess()

        self.process = process
        self.textEditElement = textEditElement

        process.setProcessChannelMode( QProcess.MergedChannels )
        process.start( 'livestreamer', arguments )
        process.readyReadStandardOutput.connect( self.show_messages )
        process.finished.connect( self.clear )

        ALL_STREAMS.append( self )



    def clear( self ):

        global ALL_STREAMS


        #ALL_STREAMS.remove( self )     #HERE its crashing the program


    def show_messages( self ):

        outputBytes = self.process.readAll().data()

        outputUnicode = outputBytes.decode( 'utf-8' )

        self.textEditElement.append( outputUnicode )
