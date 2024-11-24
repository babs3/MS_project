from spade.behaviour import PeriodicBehaviour
import socket


class CreateMessageBehaviour(PeriodicBehaviour):
        async def run(self):
            # Create the message
            topic = "location_updates"
            host = 'localhost'
            port = 65432
            payload = f"{self.agent.jid} is at (lat, lng)"
            message = f"{topic},{payload}"  # Message format to be sent

            if not hasattr(self.agent, 'sock') or self.agent.sock.fileno() == -1:
                # Create a socket (IPv4, TCP)
                self.agent.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.agent.sock.connect((host, port))
                print(f"{self.agent.jid} connected to broker")

            # Send the message to the broker
            self.agent.sock.sendall(message.encode())
            print(f"{self.agent.jid} sent message: {message}")
            