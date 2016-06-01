from autobahn.twisted.websocket import WebSocketServerFactory
from virtual_score_board.server.handler import ServerHandler
import sys
from twisted.python import log
from twisted.internet import reactor
from virtual_score_board.config_manager import ConfigManager
# import click


# "@click.command()
# @click.option('--port', default=5000, help='Number of port (default=5000).')
# @click.option('--interface', default="0.0.0.0", prompt='Please enter interface ip (default=0.0.0.0)',
#             help='Ip of interface. (default=0.0.0.0)')
def main():
    config = ConfigManager()
    config.read_config()

    # log.startLogging(sys.stdout)
    log.startLogging(config.log_file_path)

    factory = WebSocketServerFactory(u"%s://%s:%s" % ("wss" if config.use_ssl else "ws", config.host, config.port))
    factory.protocol = ServerHandler
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(int(port), factory)
    reactor.run()

if __name__ == "__main__":
    main()
