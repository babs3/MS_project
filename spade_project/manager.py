import socket
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def broker_server():
    host = 'localhost'
    port = 65432  # Port to listen on

    # Create a socket (IPv4, TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        logging.info(f"Broker listening on {host}:{port}")
        
        while True:
            # Accept a connection from an agent
            conn, addr = s.accept()
            with conn:
                logging.info(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break  # No more data from the agent
                    message = data.decode()
                    logging.info(f"Broker received: {message}")
                    
            logging.info("Connection closed, waiting for the next connection...")

if __name__ == "__main__":
    broker_server()
