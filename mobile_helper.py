"""
Mobile Access Helper - Generate QR Code for Easy Mobile Access
"""

import qrcode
from io import BytesIO
import socket

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def generate_qr_code(url):
    """Generate QR code for the given URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img

if __name__ == "__main__":
    local_ip = get_local_ip()
    url = f"http://{local_ip}:8502"

    print(f"🌐 Your dashboard URL: {url}")
    print(f"📱 Scan the QR code with your mobile phone to access the dashboard\n")

    # Generate QR code
    qr_img = generate_qr_code(url)
    qr_img.save("dashboard_qr_code.png")

    print("✅ QR Code saved as 'dashboard_qr_code.png'")
    print(f"\nTo access from mobile:")
    print(f"1. Make sure your phone is on the same WiFi network")
    print(f"2. Scan the QR code or enter: {url}")
    print(f"3. Click 'Add to Home Screen' to install as an app")
    print(f"\n🚀 The app will work like a native mobile application!")

