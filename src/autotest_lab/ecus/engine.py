import can

class EngineECU:
    MIN_RPM=0
    MAX_RPM=8000
    def __init__(self):
        self.rpm=0
    def update_rpm(self,new_rpm):
        if not isinstance(new_rpm,int) or isinstance(new_rpm,bool):
            raise TypeError("RPM must be an integer")
        if not self.MIN_RPM<=new_rpm <=self.MAX_RPM:
            raise ValueError("RPM must be between 0 and 8000")
        self.rpm=new_rpm
    def get_rpm(self):
        return self.rpm
    def create_rpm_message(self):
        rpm_bytes=self.rpm.to_bytes(
            length=2,
            byteorder="little"
        )
        message=can.Message(
            arbitration_id=0x100,
            is_extended_id=False,
            data=rpm_bytes
        )
        return message
    