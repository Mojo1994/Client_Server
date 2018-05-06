import socket
import argparse
import os
import logging
import sys


def Main():
    logging.basicConfig(level=logging.DEBUG, filename="client_logging.log")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger("").addHandler(console)

    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port")
    args = parser.parse_args()
    server_host = str(args.host)
    server_port = int(args.port)

    s = socket.socket()
    server_address = (server_host, server_port)
    s.connect(server_address)
    s.settimeout(5)

    logging.info("")

    logging.info(s.recv(1024))
    logging.info("")
    logging.info("Pasirinkite norima atlikti veiksma:\n")
    logging.info("Pateikti darbine direktorija iveskite: 'DarbDir'")
    logging.info("Patikrinti ar yra reikiamas failas iveskite: 'FailDir'")
    logging.info("Pateikti direktorijos turiniui iveskite: 'PatikDir'")
    logging.info("Norint iseiti iveskite: 'Exit'")
    logging.info("")
    while True:
        message = raw_input("Veiksmas: ")
        if message != "":
            s.send(message)
            data = s.recv(1024)
            logging.info("Serverio zinute: " + str(data))
            continue
        else:
            logging.info("Klientas atsijungia")
            s.close()


if __name__ == "__main__":
    Main()
