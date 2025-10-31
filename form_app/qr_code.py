import os
import sys
import qrcode
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django (if needed)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interviewee_form.settings')
django.setup()

print("QR code library is working!")

# URL of your welcome page
form_url = "http:quick-interview.onrender.com/welcome/"


# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(form_url)
qr.make(fit=True)

# Create and save the QR code image
img = qr.make_image(fill_color="black", back_color="white")

# Save to the static directory
static_dir = os.path.join(os.getcwd(), 'form_app', 'static', 'form_app')
os.makedirs(static_dir, exist_ok=True)
img.save(os.path.join(static_dir, 'interviewee_form_welcome.png'))

print(f"QR code saved to {os.path.join(static_dir, 'interviewee_form_welcome.png')}")
