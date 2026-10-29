class DashboardECU:
    def __init__(self):
        self.rpm=0
    def update_rpm(self,new_rpm):
        self.rpm=new_rpm
    def get_rpm(self):
        return self.rpm
    def process_message(self,message):
        if message.arbitration_id!=0x100:
            return False
        if message.is_extended_id or len(message.data)!=2:
            return False
        rpm=int.from_bytes(
            message.data,
            byteorder="little"
        )
        if not 0<=rpm<=8000:
            return False
        self.rpm=rpm
        return True