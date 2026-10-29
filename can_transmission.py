import can
from autotest_lab.ecus.engine import EngineECU
from autotest_lab.ecus.dashboard import DashboardECU

engine=EngineECU()
engine.update_rpm(3000)
dashboard=DashboardECU()
message=engine.create_rpm_message()

engine_bus=can.Bus(
    channel="vehichle_network",
    interface="virtual"
)
dashboard_bus=can.Bus(
    channel="vehichle_network",
    interface="virtual"
)
try:
    engine_bus.send(message)
    print("Engine ECU:Message Transmitted")

    recieved=dashboard_bus.recv(timeout=2.0)
    if recieved is not None:
        accepted=dashboard.process_message(recieved)
        print("Dashboard: Message Recieved!")
        if accepted:
            print(f"Dashboard RPM: {dashboard.get_rpm()}")
        else:
            print(f"Dashboard Rejected CAN message")
        
    else:
        print("Dashboard: No message Recieved")
finally:
    engine_bus.shutdown()
    dashboard_bus.shutdown()