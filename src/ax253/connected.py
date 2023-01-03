import enum

from .frame import FrameType, Frame, Control
from .address import Address

class State(enum.Enum):
    CLOSED = 0x00
    LINKED = 0x01

class AX25Connected:
    state = State.CLOSED
    t1Timer = 0
    currentFrame = None
    returnFrame = None

    def __init__(self):
        pass

    def process_frame(self, frame):
        self.currentFrame = frame
        self.source = str(frame.source)
        self.destination = str(frame.destination)
        if frame.control.ftype == FrameType.U_SABM:
            self._handle_SABM()
        elif frame.control.ftype == FrameType.U_DISC:
            self._handle_DISC()

    # SABM Frame
    def _handle_SABM(self):
        # We're in a closed state, we can accept a new connection
        # TODO: Write code to handle return path
        path = None
        if self.state == State.CLOSED:
            self.returnFrame = Frame(
                                    destination = Address.from_str(self.source),
                                    source = Address.from_str(self.destination, a7_hldc=True),
                                    path = [Address.from_any(p, a7_hldc=(p == path[-1])) for p in path or []],
                                    control = Control(FrameType.U_UA.value, final=True),
                                )

        # We're not in a closed state, we should bale the connection
        else:
            self.returnFrame = Frame(
                                    destination = Address.from_str(self.source),
                                    source = Address.from_str(self.destination, a7_hldc=True),
                                    path = [Address.from_any(p, a7_hldc=(p == path[-1])) for p in path or []],
                                    control = Control(FrameType.U_DM.value, final=True),
                                )

    # DISC Frame
    def _handle_DISC(self):
        # We're in a closed state, we can accept a new connection
        # TODO: Write code to handle return path
        path = None
        if self.state == State.LINKED:
            self.returnFrame = Frame(
                                    destination = Address.from_str(self.source),
                                    source = Address.from_str(self.destination, a7_hldc=True),
                                    path = [Address.from_any(p, a7_hldc=(p == path[-1])) for p in path or []],
                                    control = Control(FrameType.U_UA.value, final=True),
                                )

        # We're not in a closed state, we should bale the connection
        else:
            self.returnFrame = Frame(
                                    destination = Address.from_str(self.source),
                                    source = Address.from_str(self.destination, a7_hldc=True),
                                    path = [Address.from_any(p, a7_hldc=(p == path[-1])) for p in path or []],
                                    control = Control(FrameType.U_DM.value, final=True),
                                )
