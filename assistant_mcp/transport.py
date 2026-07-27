from enum import Enum


class TransportType(str, Enum):
    STDIO = "stdio"
    SSE = "sse"