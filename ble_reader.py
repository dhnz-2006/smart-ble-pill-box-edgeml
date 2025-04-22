import asyncio
from bleak import BleakClient, BleakScanner

BPM_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"  # Heart Rate Measurement
DEVICE_NAME = "nRF52840_BPM"

class BPMReader:
    def __init__(self):
        self.bpm = 0

    async def read_bpm(self):
        devices = await BleakScanner.discover()
        for d in devices:
            if d.name == DEVICE_NAME:
                async with BleakClient(d.address) as client:
                    if await client.is_connected():
                        bpm = await client.read_gatt_char(BPM_CHAR_UUID)
                        self.bpm = int(bpm[1])  # Byte 1 is BPM in standard format
                        return self.bpm
        return None

bpm_reader = BPMReader()

def get_bpm():
    return asyncio.run(bpm_reader.read_bpm())

# import asyncio
# from bleak import BleakScanner

# async def main():
#     print("Scanning for BLE devices...")
#     devices = await BleakScanner.discover(timeout=5.0)

#     for i, device in enumerate(devices):
#         print(f"[{i}] {device.name} - {device.address}")

# asyncio.run(main())
