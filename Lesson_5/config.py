from enum import Enum

token = "YOUR_TOKEN_HERE"
db_file = "database.vdb"


class States(Enum):
    S_START = "0"
    S_ENTER_NAME = "1"
    S_ENTER_AGE = "2"
    S_SEND_PIC = "3"
