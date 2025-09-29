""""""

from ucan.models.responses.base_response import Ack

if __name__ == "__main__":
    data = b"5aff000000000000000000000000000000000000000000000000"
    print(data)
    print(Ack.parse(data))
