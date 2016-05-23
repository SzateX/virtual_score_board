from autobahn.twisted.websocket import WebSocketServerFactory
from virtual_score_board.server.handler import ServerHandler
import sys
from twisted.python import log
from twisted.internet import reactor
import click


@click.command()
@click.option('--port', default=5000, help='Number of port (default=5000).')
@click.option('--interface', default="0.0.0.0", prompt='Please enter interface ip (default=0.0.0.0)',
              help='Ip of interface. (default=0.0.0.0)')
def main(interface, port):
    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://%s" % interface)
    factory.protocol = ServerHandler
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(int(port), factory)
    reactor.run()

if __name__ == "__main__":
    main()
