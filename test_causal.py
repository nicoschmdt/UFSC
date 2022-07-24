from dataclasses import dataclass, field
from collections import deque, defaultdict
from trab import Configs, Messenger
from typing import DefaultDict


@dataclass
class FakeNetwork:
    inboxes: DefaultDict[tuple[str, int], deque[bytes]] = field(default_factory=lambda: defaultdict(deque))

    def send(self, address: str, port: int, message: bytes) -> None:
        self.inboxes[(address, port)].append(message)

    def receive(self, address: str, port: int) -> bytes:
        return self.inboxes[(address, port)].popleft()


@dataclass
class FakeConnection:
    address: str
    port: int
    fake_network: FakeNetwork

    def send(self, address: str, port: int, message: bytes) -> None:
        self.fake_network.send(address, port, message)

    def receive(self) -> bytes:
        return self.fake_network.receive(self.address, self.port)


def test_event_sequence() -> None:
    fake_network = FakeNetwork()

    def make_fake_connection(address: str, port: int) -> FakeConnection:
        return FakeConnection(address, port, fake_network)

    addresses = {
        0: 'address:6001',
        1: 'address:6002',
        2: 'address:6003',
    }

    p0 = Messenger(Configs(3, 0, addresses, 0), connector_factory=make_fake_connection)
    p1 = Messenger(Configs(3, 1, addresses, 0), connector_factory=make_fake_connection)
    p2 = Messenger(Configs(3, 2, addresses, 0), connector_factory=make_fake_connection)

    def assert_clocks(c0, c1, c2):
        def assert_messenger_clocks(m, c):
            assert (m.clocks[0], m.clocks[1], m.clocks[2]) == c

        assert_messenger_clocks(p0, c0)
        assert_messenger_clocks(p1, c1)
        assert_messenger_clocks(p2, c2)

    p0.increment_clock()
    assert_clocks((1, 0, 0), (0, 0, 0), (0, 0, 0))
    p2.send(1, b'')
    assert_clocks((1, 0, 0), (0, 0, 0), (0, 0, 1))
    p1.receive()
    assert_clocks((1, 0, 0), (0, 1, 1), (0, 0, 1))
    p0.send(1, b'')
    assert_clocks((2, 0, 0), (0, 1, 1), (0, 0, 1))
    p1.receive()
    assert_clocks((2, 0, 0), (2, 2, 1), (0, 0, 1))
    p2.increment_clock()
    assert_clocks((2, 0, 0), (2, 2, 1), (0, 0, 2))
    p0.increment_clock()
    assert_clocks((3, 0, 0), (2, 2, 1), (0, 0, 2))
    p1.send(0, b'')
    assert_clocks((3, 0, 0), (2, 3, 1), (0, 0, 2))
    p0.receive()
    assert_clocks((4, 3, 1), (2, 3, 1), (0, 0, 2))
    p0.send(2, b'')
    assert_clocks((5, 3, 1), (2, 3, 1), (0, 0, 2))
    p2.receive()
    assert_clocks((5, 3, 1), (2, 3, 1), (5, 3, 3))
