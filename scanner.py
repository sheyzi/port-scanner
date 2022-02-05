from queue import Queue
import socket
import threading


class Scanner:
    def __init__(self, target: str):
        self.target = target
        self.queue = Queue()
        self.open_ports = []

    def portscan(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.target, port))
            return True
        except:
            return False

    def get_ports(self, mode, custom_ports: str = None):
        if mode == 1:
            """
            This scans the 1023 standardized ports
            """
            for port in range(1, 1024):
                self.queue.put(port)
        elif mode == 2:
            """
            Scan the 48,128 reserved ports
            """
            for port in range(1, 49152):
                self.queue.put(port)
        elif mode == 3:
            """
            Scan only important ports
            """
            ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
            for port in ports:
                self.queue.put(port)
        elif mode == 4:
            """
            Scan a custom port
            """
            if not custom_ports:
                raise ValueError("When using mode 4 you must also pass a custom port!")
            ports = custom_ports.split()
            ports = list(map(int, ports))
            for port in ports:
                self.queue.put(port)
        else:
            raise ValueError("Invalid mode passed!")

    def worker(self):
        while not self.queue.empty():
            port = self.queue.get()
            if self.portscan(port):
                self.open_ports.append(port)

    def run(self, mode, custom_ports: str = None):
        self.get_ports(mode, custom_ports)

        thread_list = []

        for t in range(100):
            thread = threading.Thread(target=self.worker)
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        return self.open_ports


if __name__ == "__main__":
    scanner = Scanner(target="127.0.0.1")
    print(scanner.run(2))
