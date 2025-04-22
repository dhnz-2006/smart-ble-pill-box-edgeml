from flask import *
import asyncio
from bleak import BleakClient
from bleak.exc import BleakDeviceNotFoundError , BleakCharacteristicNotFoundError
import struct
import datetime

app = Flask(__name__)

bpm_characteristic_uuid = "00002a37-0000-1000-8000-00805f9b34fb"
alarm_upload_char_uuid = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  # example UUID for custom upload
device_address = "E2:7E:15:9A:CA:0E"

alarm_data = []  # For HTML display
ble_data = []    # For BLE transmission
medicine_per_box = {}  # Box number to medicine name mapping

async def get_bpm():
    async with BleakClient(device_address) as client:
        bpm_value = await client.read_gatt_char(bpm_characteristic_uuid)
        return bpm_value

async def send_alarm_data():
    async with BleakClient(device_address) as client:
        await client.connect()
        await client.get_services()
        for alarm in alarm_data:
            day, hour, minute, box = alarm
            payload = struct.pack("BBBB", day, hour, minute, box)
            await client.write_gatt_char(alarm_upload_char_uuid, payload)
            await asyncio.sleep(0.5)

@app.route('/')
def index():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bpm_value = loop.run_until_complete(get_bpm())
        bpm_value = bpm_value[1]
    except BleakDeviceNotFoundError:
        bpm_value = 0
        return render_template("base.html", message="NRF52840 NOT CONNECTED", alarms=alarm_data, bpm=bpm_value)
    return render_template("base.html", message="CONNECTED", alarms=alarm_data, bpm=bpm_value)

@app.route('/add', methods=["GET", "POST"])
def add_meds():
    print(medicine_per_box)
    if request.method == "POST":
        time = request.form["time"]
        hour, minute = map(int, time.split(":"))
        name = request.form["name"]

        # Find the corresponding box number from medicine_per_box
        box = next((k for k, v in medicine_per_box.items() if v == str(name)), None)
        

        if box:
            # Add the alarm data and BLE data
            alarm_data.append(["Everyday", time, name, box])
            ble_data.append(bytearray([len(ble_data)+1, 0, hour, minute, 0, box, 1]))
            print(alarm_data)
        else:
            # Handle case when box number is not found (shouldn't happen if data is valid)
            pass
        
        return redirect(url_for("index"))

    return render_template("add.html", warning=None, medicines=medicine_per_box)



@app.route('/upload', methods=["POST"])
def upload():
    try:
        ADDRESS = device_address
        CHAR_UUID = "22222222-3333-4444-5555-666666666666"

        async def write_data():
            async with BleakClient(ADDRESS) as client:
                if await client.is_connected():
                    for data in ble_data:
                        await client.write_gatt_char(CHAR_UUID, data)
                        await asyncio.sleep(0.5)

        asyncio.run(write_data())
        return redirect(url_for("index"))

    except Exception as e:
        return render_template("base.html", message=f"Upload failed: {e}", alarms=alarm_data, bpm=0)

@app.route('/sync_time', methods=["POST"])
def sync_time():
    ADDRESS = device_address
    CHAR_UUID = "22222222-3333-4444-5555-666666666666"
    now = datetime.datetime.now()
    day = now.isoweekday()
    hour = now.hour
    minute = now.minute
    second = now.second
    payload = bytearray([0, day, hour, minute, second, 0, 0])

    async def send_time():
        async with BleakClient(ADDRESS) as client:
            if await client.is_connected():
                await client.write_gatt_char(CHAR_UUID, payload)

    asyncio.run(send_time())
    return redirect(url_for("index"))

@app.route('/confirm_delete', methods=["POST"])
def confirm_delete():
    box = int(request.form["box"])
    hour, minute = map(int, request.form["time"].split(":"))
    name = request.form["name"]

    global alarm_data, ble_data
    alarm_data = [row for row in alarm_data if row[3] != box]
    ble_data = [row for row in ble_data if row[5] != box]

    alarm_data.append(["Everyday", f"{hour}:{minute}", name, box])
    ble_data.append(bytearray([len(ble_data)+1, 0, hour, minute, 0, box, 1]))
    return redirect(url_for("index"))

@app.route('/delete/<int:box>')
def delete(box):
    global alarm_data, ble_data
    alarm_data = [row for row in alarm_data if row[3] != box]
    ble_data = [row for row in ble_data if row[5] != box]
    return redirect(url_for('index'))

@app.route('/add_medicine', methods=["GET", "POST"])
def add_medicine():
    warning=""
    if request.method == "POST":
        box = int(request.form["box"])
        name = request.form["name"]
        
        # Check if the box number already exists
        if box in medicine_per_box:
            warning = "Box number already exists"  # Set a warning message
        else:
            # Add the medicine to the box if it doesn't exist
            medicine_per_box[box] = name
            warning = f"Medicine '{name}' added to Box {box}"  # Success message
            #return redirect(url_for("add_meds"))
    return render_template("add_medicine.html",warning=warning)

if __name__ == '__main__':
    app.run(debug=True)
