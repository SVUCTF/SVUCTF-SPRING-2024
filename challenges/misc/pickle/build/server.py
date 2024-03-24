#!/usr/local/bin/python

import socket
import pickle
from datetime import datetime

IP = "0.0.0.0"
PORT = 8848
INFO = """
{}
[CPU]
    CPU 核数: {}
    CPU 使用率: {:.1f}%
[内存]
    总内存: {} 字节
    可用内存: {} 字节
    内存使用率: {:.1f}%
[磁盘]
    总磁盘: {} 字节
    已使用磁盘: {} 字节
    磁盘空闲: {} 字节
    磁盘使用率: {:.1f}%
[网络]
    发送的总字节: {} 字节
    接收的总字节: {} 字节
    发送的总包裹: {} 个
    接收的总包裹: {} 个
{}"""


class Info:
    def __init__(
        self,
        time=0.0,
        cpu_count=None,
        cpu_percent=None,
        mem_total=None,
        mem_available=None,
        mem_percent=None,
        disk_total=None,
        disk_used=None,
        disk_free=None,
        disk_percent=None,
        net_bytes_sent=None,
        net_bytes_recv=None,
        net_packets_sent=None,
        net_packets_recv=None,
    ) -> None:
        self.time = time
        self.cpu_count = cpu_count
        self.cpu_percent = cpu_percent
        self.mem_total = mem_total
        self.mem_available = mem_available
        self.disk_total = disk_total
        self.disk_used = disk_used
        self.disk_free = disk_free
        self.disk_percent = disk_percent
        self.mem_percent = mem_percent
        self.net_bytes_sent = net_bytes_sent
        self.net_bytes_recv = net_bytes_recv
        self.net_packets_sent = net_packets_sent
        self.net_packets_recv = net_packets_recv


def print_info(info: Info):
    dtime = datetime.fromtimestamp(info.time)
    time_str = dtime.strftime(" %Y-%m-%d %H:%M:%S ")
    info_str = INFO.format(
        time_str.center(35, "="),
        info.cpu_count,
        info.cpu_percent,
        info.mem_total,
        info.mem_available,
        info.mem_percent,
        info.disk_total,
        info.disk_used,
        info.disk_free,
        info.disk_percent,
        info.net_bytes_sent,
        info.net_bytes_recv,
        info.net_packets_sent,
        info.net_packets_recv,
        "=" * 35,
    )
    print(info_str)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PORT))
    server.listen()

    print(f"Server is running and listening on port {PORT}...")

    while True:
        client, address = server.accept()
        client_ip, client_port = address
        print(f"Connected to client: {client_ip}:{client_port}")

        while True:
            try:
                data_len = client.recv(4)
                len = int.from_bytes(data_len)
                data = client.recv(len)
                info = pickle.loads(data)
                print_info(info)
            except Exception:
                client.close()
                break


if __name__ == "__main__":
    main()
