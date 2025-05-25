import argparse
import os
import socket
import sys
import threading
from random import randint
from typing import Tuple

running = True


def generate_random_reply(packet_size: Tuple[int, int]) -> str | bytes:
    size = randint(*packet_size)
    return os.urandom(size)


def to_bytes(text: str | bytes) -> bytes:
    if not isinstance(text, bytes):
        return text.encode('utf-8')
    return text


def handle_tcp_client(conn, addr, packet_size: Tuple[int, int]):
    """Handles a single TCP client connection."""
    print(f"[TCP] Connected by {addr}")
    try:
        while True:
            data = conn.recv(4096)  # Receive up to 4KB of data
            if not data:
                break  # Client disconnected

            received_message = data.decode('utf-8', errors='ignore')
            print(f"[TCP] Received from {addr}: {received_message[:100]}")  # Print first 100 chars

            reply_message = generate_random_reply(packet_size)
            print(f"[TCP] Replying to {addr}: {reply_message}")
            conn.sendall(to_bytes(reply_message))

    except ConnectionResetError:
        print(f"[TCP] Client {addr} unexpectedly disconnected.")
    except Exception as e:
        print(f"[TCP] Error handling client {addr}: {e}")
    finally:
        print(f"[TCP] Client {addr} disconnected.")
        conn.close()


def start_tcp_server(host: str, port: int, packet_size: Tuple[int, int]) -> None:
    """Starts the TCP server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"TCP Server listening on {host}:{port}")

        while running:
            conn, addr = s.accept()
            client_handler = threading.Thread(target=handle_tcp_client, args=(conn, addr, packet_size))
            client_handler.start()


def start_udp_server(host: str, port: int, packet_size: Tuple[int, int]) -> None:
    """Starts the UDP server."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        print(f"UDP Server listening on {host}:{port}")

        while running:
            try:
                data, addr = s.recvfrom(4096)  # Receive data and sender address
                received_message = data.decode('utf-8', errors='ignore')
                print(f"[UDP] Received from {addr}: {received_message[:100]}")  # Print first 100 chars

                reply_message = generate_random_reply(packet_size)
                print(f"[UDP] Replying to {addr}: {reply_message}")
                s.sendto(to_bytes(reply_message), addr)  # Send reply back to sender
            except Exception as e:
                print(f"[UDP] Error processing UDP packet: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start an automatic reply server.")
    parser.add_argument('--protocol', '-t', type=str, choices=['tcp', 'udp'], required=True,
                        help="Specify the protocol: 'tcp' or 'udp'")
    parser.add_argument('--port', '-p', type=int, required=True,
                        help="Specify the port to listen")
    parser.add_argument('--host', '-o', type=str, default="0.0.0.0",
                        help="Specify the port to listen")
    parser.add_argument('--min-packet-size', '-n', type=int, default=20,
                        help="Minimum packet (only payload) size of the response")
    parser.add_argument('--max-packet-size', '-m', type=int, default=1000,
                        help="Maximum packet (only payload) size of the response")

    args = parser.parse_args()

    try:
        if args.protocol == 'tcp':
            start_tcp_server(host=args.host, port=args.port, packet_size=(args.min_packet_size, args.max_packet_size))
        elif args.protocol == 'udp':
            start_udp_server(host=args.host, port=args.port, packet_size=(args.min_packet_size, args.max_packet_size))
        else:
            print("Invalid protocol specified. Use 'tcp' or 'udp'.")
            sys.exit(1)
    except KeyboardInterrupt:
        running = False
        sys.exit(0)
