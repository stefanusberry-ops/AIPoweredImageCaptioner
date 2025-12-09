from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from transformers import pipeline
from PIL import Image
import os
import torch
from flask_cors import CORS

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allow only image files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Initialize the vision-language model
device = 0 if torch.cuda.is_available() else -1
captioner = pipeline(
    "image-to-text",
    model="Salesforce/blip-image-captioning-base",
    device=device
)

# Enable CORS so the frontend (GitHub Pages) can call the API
CORS(app)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle image upload and caption generation"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use PNG, JPG, JPEG, GIF, or WebP'}), 400
        
        # Save file securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Open and process image
        image = Image.open(filepath).convert('RGB')
        
        # Generate caption
        result = captioner(image)
        caption = result[0].get('generated_text') or result[0].get('caption') or str(result)

        # Build a full URL to the uploaded image so a remote frontend can display it
        host = request.host_url.rstrip('/')
        image_url = f"{host}/uploads/{filename}"

        return jsonify({
            'success': True,
            'image_url': image_url,
            'caption': caption,
            'filename': filename
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    """Serve uploaded files"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if os.path.exists(filepath):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
