import can
from autotest_lab.ecus.dashboard import DashboardECU

def test_dashboard_start_at_zero():
    dashboard=DashboardECU()
    assert dashboard.get_rpm()==0
def test_dashboard_update_rpm():
    dashboard=DashboardECU()
    dashboard.update_rpm(3000)
    assert dashboard.get_rpm()==3000
def test_dashboard_process_valid_can_message():
    dashboard=DashboardECU()
    message=can.Message(
        arbitration_id=0x100,
        is_extended_id=False,
        data=[0xB8,0x0B]
    )
    result=dashboard.process_message(message)
    assert result is True
    assert dashboard.get_rpm()==3000
def test_invalid_can_id_preserves_rpm():
    dashboard=DashboardECU()
    dashboard.update_rpm(3000)

    message=can.Message(
        arbitration_id=0x200,
        is_extended_id=False,
        data=[0xB8,0x0B]
    )
    result=dashboard.process_message(message)
    assert result==False
    assert dashboard.get_rpm()==3000