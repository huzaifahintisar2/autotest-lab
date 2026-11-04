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


def test_dashboard_rejects_remote_frame():
    dashboard=DashboardECU()
    dashboard.update_rpm(3000)
    message=can.Message(
        arbitration_id=0x100,
        is_extended_id=False,
        is_remote_frame=True,
        dlc=2
    )
    result=dashboard.process_message(message)
    assert result is False
    assert dashboard.get_rpm()==3000


def test_dashboard_rejects_error_frame():
    dashboard=DashboardECU()
    dashboard.update_rpm(3000)
    message=can.Message(
        arbitration_id=0x100,
        is_extended_id=False,
        is_error_frame=True,
        data=[0xB8,0x0B]
    )
    result=dashboard.process_message(message)
    assert result is False
    assert dashboard.get_rpm()==3000


def test_dashboard_rejects_one_byte_payload():
    dashboard=DashboardECU()
    dashboard.update_rpm(3000)
    message=can.Message(
        arbitration_id=0x100,
        is_extended_id=False,
        data=[0xB8]
    )
    result=dashboard.process_message(message)
    assert result is False
    assert dashboard.get_rpm()==3000


def test_dashboard_rejects_extended_can_id():
    dashboard=DashboardECU()
    dashboard.update_rpm(3000)
    message=can.Message(
        arbitration_id=0x100,
        is_extended_id=True,
        data=[0xB8,0x0B]
    )
    result=dashboard.process_message(message)
    assert result is False
    assert dashboard.get_rpm()==3000

    
def test_dashboard_rejects_out_of_range_rpm():
    dashboard=DashboardECU()
    dashboard.update_rpm(3000)
    message=can.Message(
        arbitration_id=0x100,
        is_extended_id=False,
        data=[0xFF,0xFF]
    )
    result=dashboard.process_message(message)
    assert result is False
    assert dashboard.get_rpm()==3000
