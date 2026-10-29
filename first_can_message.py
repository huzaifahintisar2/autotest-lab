
import can

# Create two virtual CAN interfaces on the same channel.
engine_bus = can.Bus(
    channel="vehicle_network",
    interface="virtual"
)

dashboard_bus = can.Bus(
    channel="vehicle_network",
    interface="virtual"
)

try:
    # Create a CAN message containing 3000 RPM.
    message = can.Message(
        arbitration_id=0x200,
        is_extended_id=False,
        data=[0xB8, 0x0B]
    )

    # Engine ECU transmits the message.
    engine_bus.send(message)
    print("Engine ECU: Message sent!")

    # Dashboard ECU waits for a message.
    received = dashboard_bus.recv(timeout=2.0)

    if received is not None:
            if received.arbitration_id==0x100:
                rpm = int.from_bytes(received.data, byteorder="little")

                print(f"CAN ID: {hex(received.arbitration_id)}")
                print(f"Received data: {received.data.hex(' ')}")
                print(f"Dashboard ECU: Engine RPM = {rpm}")
            else:
                 print("Dashboard ECU: Unknown Can Message")
    else:
        print("Dashboard ECU: No message received!")

finally:
    engine_bus.shutdown()
    dashboard_bus.shutdown()
