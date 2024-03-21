import json
import grpc
import atexit
import concurrent

import jimon_pb2
import jimon_pb2_grpc

import jimondb

from loguru import logger


class Servicer(jimon_pb2_grpc.JimonServicer):
    def UpdateAndAck(self, msg_update, context) -> jimon_pb2.MsgAck:
        logger.debug(
            f"MsgUpdate: type={msg_update.update_type} name={msg_update.hostname} time={msg_update.timestamp} temp={msg_update.temp:.2f} cpu_usage={msg_update.cpu_usage:.2f} mem_usage={msg_update.mem_usage:.2f}"
        )
        jimondb.insert(
            msg_update.update_type,
            msg_update.hostname,
            msg_update.timestamp,
            msg_update.temp,
            msg_update.cpu_usage,
            msg_update.mem_usage,
        )
        msg_ack = jimon_pb2.MsgAck(errno=0)
        return msg_ack


class Server:
    def __init__(self, fpath_config: str = "config.json"):
        logger.info("Server initializing...")
        # read config from file
        logger.info("Reading config from file")
        with open(fpath_config, "r") as f:
            config = json.load(f)
            self.server_port = config["server_port"]
        logger.info(f"Server {self.server_port=}")
        # connect to database
        logger.info("Connecting to database")
        jimondb.connect()

    def run(self):
        self.server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
        jimon_pb2_grpc.add_JimonServicer_to_server(Servicer(), self.server)
        self.server.add_insecure_port("[::]:" + str(self.server_port))
        self.server.start()
        logger.info(f"Server started, listening on {self.server_port=}")
        self.server.wait_for_termination()

    def exit(self):
        logger.info("Server tearing down...")
        jimondb.debug()
        logger.info("Closing database connection")
        jimondb.close()
        logger.info("Stop gRPC server")
        self.server.stop(0)


if __name__ == "__main__":
    server = Server()
    server.run()
