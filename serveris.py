import socket
import argparse
import os
import logging
import threading


def multi_client(c):
    while True:
        data = c.recv(1024)
        if data == "DarbDir":
            logging.info("Is vartotojo gavome uzklausa: " + str(data))
            data = os.getcwd()
            logging.info("Siunciame darbo direktorija " + str(data))
            c.send(data)
        elif data == "PatikDir":
            logging.info("Is vartotojo gavome uzklausa: " + str(data))
            dir = os.getcwd()
            list_dir = os.listdir(dir)
            data = list_dir
            logging.info("Siunciame direktorijos turini " + str(data))
            c.send(str(data))
        elif data == "FailDir":
            logging.info("Is vartotojo gavome uzklausa: " + str(data))
            c.send("Iveskite failo pavadinima: ")
            data = c.recv(1024)
            name = str(data)
            if os.path.isfile(name) and os.access(name, os.R_OK):
                logging.info("%s, failas egzistuoja" % str(name))
                c.send("%s, failas egzistuoja" % str(name))
            else:
                logging.info("Tokio failo nera")
                c.send("Tokio failo nera")
        else:
            logging.info("Nera ko siusti")
            c.send("Klientas atsijungia")
            break
    c.close()

def Main():
    logging.basicConfig(level=logging.DEBUG, filename="server_logging.log")
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
    s.bind(server_address)

    logging.info("Laukiama prisijungimo")
    s.listen(5)
    while True:
        c, addr = s.accept()
        c.settimeout(20)
        logging.info("Prie serverio prisijunge" + str(addr))
        c.send("Sveiki")
        t = threading.Thread(target=multi_client, args=(c,))
        t.start()
    s.close()

if __name__ == "__main__":
    Main()