import can

from autotest_lab.ecus.engine import EngineECU
from autotest_lab.ecus.dashboard import DashboardECU
from autotest_lab.ecus.brake import BrakeECU

def test_brake_can_transmission():
    brake=BrakeECU()
    brake.update_pressure(50.5)

    sender=can.Bus(
        channel="brake_test",
        interface="virtual"
    )

    receiver=can.Bus(
        channel="brake_test",
        interface="virtual"
    )
    try:
        message=brake.create_pressure_message()
        sender.send(message)
        received=receiver.recv(timeout=1.0)
        assert received is not None
        assert received.arbitration_id==0x200
        assert received.is_extended_id is False
        assert received.data==bytes([0xF9,0x01])
    finally:
        sender.shutdown()
        receiver.shutdown()


def test_engine_to_dashboard_over_can():
    engine=EngineECU()
    dashboard=DashboardECU()
    engine.update_rpm(3000)
    engine_bus=can.Bus(
        channel="integration_test",
        interface="virtual"
    )
    dashboard_bus=can.Bus(
        channel="integration_test",
        interface="virtual"
    )
    try:
        message=engine.create_rpm_message()
        engine_bus.send(message)
        recieved=dashboard_bus.recv(timeout=1.0)
        assert recieved is not None
        accepted=dashboard.process_message(recieved)
        assert accepted is True
        assert dashboard.get_rpm()==3000
    finally:
        engine_bus.shutdown()
        dashboard_bus.shutdown()