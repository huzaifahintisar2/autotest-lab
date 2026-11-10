import can
import math
class BrakeECU:
    def __init__(self):
        self.pressure=0

    def get_pressure(self):
        return self.pressure
    def update_pressure(self,pressure):
        if isinstance(pressure,bool) or not isinstance(pressure,(int,float)):
            raise ValueError("Pressure must be a number")
        if not math.isfinite(pressure):
            raise ValueError("Pressure must be finite")
        if pressure<0 or pressure>100:
            raise ValueError("Pressure must be between 0 and 100")
        self.pressure=pressure
    def create_pressure_message(self):
        raw_pressure=round(self.pressure*10)

        message=can.Message(
            arbitration_id=0x200,
            is_extended_id=False,
            data=raw_pressure.to_bytes(2,byteorder="little")
        )
        return message