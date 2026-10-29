import can

from autotest_lab.ecus.engine import EngineECU
from autotest_lab.ecus.dashboard import DashboardECU

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