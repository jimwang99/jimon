import os
import enum
import grpc
import json
import time
import atexit
import psutil
import socket
import dataclasses

from typing import NamedTuple

from loguru import logger

import jimon_pb2
import jimon_pb2_grpc


class UpdateType(enum.IntEnum):
    UPDATE = 0
    POWERUP = 1
    POWERDOWN = 2


class Client:
    def __init__(self, fpath_config: str = "config.json"):
        logger.info(f"Client initializing...")

        # read config from file
        logger.info("Reading config from file")
        with open(fpath_config, "r") as f:
            config = json.load(f)
            self.server_ip = config["server_ip"]
            self.server_port = config["server_port"]
            self.client_interval = config["client_interval"]
        self.hostname = socket.gethostname()
        logger.info(f"{self.hostname=} {self.server_ip=} {self.server_port=}")

        atexit.register(self.exit)

        # send powerup message
        logger.info("Sending powerup message")
        self._send_update(UpdateType.POWERUP)

    def exit(self):
        logger.info(f"Client tearing down...")
        # send powerdown message
        logger.info("Sending powerdown message")
        self._send_update(UpdateType.POWERDOWN)

    def run(self, interval: int = 0, is_test: bool = False):
        if interval == 0:
            interval = self.client_interval
        while True:
            self._send_update()
            if is_test:
                break
            time.sleep(interval)

    def _send_update(self, update_type: UpdateType = UpdateType.UPDATE):
        try:
            with grpc.insecure_channel(f"{self.server_ip}:{self.server_port}") as channel:
                stub = jimon_pb2_grpc.JimonStub(channel)
                msg_update = jimon_pb2.MsgUpdate(
                    update_type=update_type,
                    hostname=self.hostname,
                    timestamp=self._get_timestamp(),
                    temp=self._get_temp(),
                    cpu_usage=self._get_cpu_usage(),
                    mem_usage=self._get_mem_usage(),
                )
                logger.debug(
                    f"MsgUpdate: type={msg_update.update_type} name={msg_update.hostname} time={msg_update.timestamp} temp={msg_update.temp:.2f} cpu_usage={msg_update.cpu_usage:.2f} mem_usage={msg_update.mem_usage:.2f}"
                )

                msg_ack = stub.UpdateAndAck(msg_update)
                if msg_ack.errno != 0:
                    logger.error(f"MsgAck: errno={msg_ack.errno}")
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                logger.error(f"gRPC CANCELLED")
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                logger.error(f"gRPC UNAVAILABLE")
            else:
                print(f"gRPC UNKNOWN: code={rpc_error.code()} message={rpc_error.details()}")

    def _get_timestamp(self):
        return int(time.time())

    def _get_temp(self) -> float:
        try:
            zones = os.listdir("/sys/class/thermal")
        except FileNotFoundError:
            return 0.0
        temps = []
        for zone in zones:
            if zone.startswith("thermal_zone"):
                with open(f"/sys/class/thermal/{zone}/temp") as f:
                    temp = int(f.read()) / 1000.0
                    temps.append(temp)
                    logger.debug(f"{zone=} {temp=}")
        if len(temps) == 0:
            return 0.0
        else:
            return max(temps)

    def _get_cpu_usage(self) -> float:
        return psutil.cpu_percent()

    def _get_mem_usage(self) -> float:
        return psutil.virtual_memory().percent

    def __repr__(self):
        return f"Status: {self.hostname=} {self.server_ip=} {self.server_port=}"

def main(interval: int = 0, is_test: bool = False):
    client = Client()
    client.run(interval=interval, is_test=is_test)


if __name__ == "__main__":
    import fire
    fire.Fire(main)
