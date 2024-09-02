<center>

```
Qrysis
```

</center>

### QRIS Data

**Example:**
00020101021126570011ID.DANA.WWW011893600915318061166302091806116630303UMI51440014ID.CO.QRIS.WWW0215ID10211078638670303UMI5204561153033605802ID5904XRCE6016Kab. Tokyo Kidul61054206963048D6C


ID | Length | Description     | Data
-- | ------ | --------------- | ----
00 | 02     | QRIS Version    | 01
01 | 02     | QRIS Type       | 11 (Static, replace to 12 for dynamic QRIS)
26 | 57     | Merchant Info   | 0011ID.DANA.WWW011893600915318061166302091806116630303UMI
51 | 44     | Detailed Info   | 0014ID.CO.QRIS.WWW0215ID10211078638670303UMI
52 | 04     | Category        | 5611
53 | 03     | Currency        | 360 (IDR)
58 | 02     | Country         | ID
59 | 04     | Merchant Name   | XRCE
60 | 16     | Merchant Region | Kab. Tokyo Kidul
61 | 05     | Postal Code     | 42069
63 | 04     | Checksum        | 8D6C

### Usage
Move your QRIS to `baseqr.jpeg` and victim QRIS to `victim.jpeg`, then type:
```
python3 qrysis.py
```