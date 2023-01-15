# Import the qrcode library
import qrcode

# Create a qr code instance
qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_L,
    box_size = 10,
    border = 4,
)

# The data that you want to encode
data = "192.168.1.19:8765"

# Add the data
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save it somewhere, change the extension as needed:
img.save("./image_name.png")
# img.save("image_name.bmp")
# img.save("image_name.jpeg")
