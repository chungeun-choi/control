from server import create_app
from grpc_server.control_server import serve

if __name__ == '__main__':
    create_app("localhost",8080)
    #serve()


