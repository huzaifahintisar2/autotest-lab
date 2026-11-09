import pytest
from autotest_lab.ecus.brake import BrakeECU

def test_break_start_at_zero():
    brake=BrakeECU()
    assert brake.get_pressure()==0  


def test_brake_update_pressure():
    brake=BrakeECU()
    brake.update_pressure(50)
    assert brake.get_pressure()==50

def test_brake_rejects_negative_pressure():
    brake=BrakeECU()
    with pytest.raises(ValueError):
        brake.update_pressure(-10)
    assert brake.get_pressure()==0

def test_brake_rejects_excessive_pressure():
    brake=BrakeECU()
    brake.update_pressure(70)
    with pytest.raises(ValueError):
        brake.update_pressure(120)
    assert brake.get_pressure()==70

def test_brake_rejects_non_numeric_pressure():
    brake=BrakeECU()
    brake.update_pressure(70)
    with pytest.raises(ValueError):
        brake.update_pressure("high")
    assert brake.get_pressure()==70

def test_brake_pressure_scaling():
    brake=BrakeECU()
    brake.update_pressure(50.5)
    raw_pressure=round(brake.get_pressure()*10)
    assert raw_pressure==505

def test_brake_create_can_message():
    brake=BrakeECU()
    brake.update_pressure(50.5)

    message=brake.create_pressure_message()
    assert message.arbitration_id==0x200
    assert message.is_extended_id is False
    assert message.data==bytes([0xF9,0x01])