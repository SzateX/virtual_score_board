from autobahn.twisted.websocket import WebSocketServerFactory
from virtual_score_board.server.handler import ServerHandler
# import sys
from twisted.python import log
from twisted.internet import reactor
from virtual_score_board.config_manager import ConfigManager
# import click


# "@click.command()
# @click.option('--port', default=5000, help='Number of port (default=5000).')
# @click.option('--interface', default="0.0.0.0", prompt='Please enter interface ip (default=0.0.0.0)',
#             help='Ip of interface. (default=0.0.0.0)')
def main():
    config = ConfigManager.get_config()
    config.read_config()

    # log.startLogging(sys.stdout)
    # with open(config.log_file_path, "a") as log_file:
    #     log.startLogging(log_file)

    log.startLogging(open(config.log_file_path, 'w'))

    factory = WebSocketServerFactory(u"%s://%s:%s" % ("wss" if config.use_ssl else "ws", config.host, config.port))
    factory.protocol = ServerHandler
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(int(config.port), factory)
    reactor.run()

if __name__ == "__main__":
    main()
