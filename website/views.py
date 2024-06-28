from flask import Blueprint, render_template, request, redirect, url_for
from io import BytesIO
import base64
import qrcode

views = Blueprint('views', __name__)

@views.route('/',methods=['GET'])
def linkpage():
    return render_template("linkpage.html")

@views.route('/generate', methods=['POST'])
def generate_qr():
    try:
        url = request.form['url'].strip()  
    except KeyError:
        return "Error: URL field is required.", 400
    
    if not url:
        return "Error: URL field cannot be empty.", 400
    
    try:
        img = qrcode.make(url)
    except Exception as e:
        return f"Error generating QR code: {e}", 500
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return redirect(url_for('views.qrpage', qr_code=img_str))

@views.route('/qrpage')
def qrpage():
    qr_code = request.args.get('qr_code')
    if not qr_code:
        return "Error: QR Code data not found.", 404
    return render_template('qrpage.html', qr_code=qr_code)





  



  
