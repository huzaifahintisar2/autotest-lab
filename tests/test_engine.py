import pytest
from autotest_lab.ecus.engine import EngineECU

def test_engine_starts_at_zero():
    engine=EngineECU()
    assert engine.get_rpm()==0
def test_engine_updates_rpm():
    engine=EngineECU()
    engine.update_rpm(3000)

    assert engine.get_rpm()==3000
def test_engine_rejects_negative_rpm():
    engine=EngineECU()
    with pytest.raises(ValueError):
        engine.update_rpm(-500)
def test_engine_rejects_excessive_rpm():
    engine=EngineECU()
    with pytest.raises(ValueError):
        engine.update_rpm(9000)
def test_invalid_update_preserves_previous_rpm():
    engine=EngineECU()
    engine.update_rpm(3000)
    with pytest.raises(ValueError):
        engine.update_rpm(-500)
    assert engine.get_rpm()==3000
def test_engine_create_can_message():
    engine=EngineECU()
    engine.update_rpm(3000)
    message=engine.create_rpm_message()

    assert message.arbitration_id==0x100
    assert message.is_extended_id==False
    assert message.data==bytes([0xB8, 0x0B])