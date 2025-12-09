# AI-Powered Image Captioner

A Flask web application that allows users to upload images and automatically generate captions using a pre-trained Hugging Face vision-language model.

## Features

- 🖼️ Drag-and-drop or click-to-upload image interface
- 🤖 AI-powered caption generation using Salesforce BLIP model
- 🎨 Beautiful, responsive UI with gradient design
- ⚡ Real-time processing with loading indicators
- 🛡️ Secure file handling with validation
- 📱 Mobile-friendly responsive design
- ✅ Support for PNG, JPG, JPEG, GIF, and WebP formats

## Installation

1. **Clone the repository** (if not already done):
```bash
git clone <repository-url>
cd AIPoweredImageCaptioner
```

2. **Create a virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

1. **Start the Flask application**:
```bash
python app.py
```

2. **Open your browser** and navigate to:
```
http://localhost:5000
```

3. **Upload an image**:
   - Click the upload area or drag and drop an image
   - Wait for the AI to generate a caption
   - View the image and caption together

## Project Structure

```
.
├── app.py                 # Flask application and routes
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # HTML template with UI and JavaScript
├── uploads/              # Directory for uploaded images (auto-created)
└── README.md             # This file
```

## Technical Details

### Model
The application uses the **Salesforce BLIP (Bootstrapping Language-Image Pre-training)** model for image captioning:
- Model: `Salesforce/blip-image-captioning-base`
- Architecture: Vision-Language transformer
- Automatically uses GPU if available, falls back to CPU

### Backend
- **Framework**: Flask
- **File Handling**: Werkzeug with security validation
- **Image Processing**: Pillow (PIL)
- **ML Pipeline**: Hugging Face Transformers

### Frontend
- **Design**: Responsive HTML/CSS with gradient backgrounds
- **Interactivity**: Vanilla JavaScript
- **Features**: Drag-and-drop, file validation, real-time feedback

## API Endpoints

### `GET /`
Returns the main HTML page.

### `POST /upload`
Handles image upload and caption generation.

**Request**: 
- Form data with `file` field containing the image

**Response**:
```json
{
  "success": true,
  "image_url": "/static/uploaded/filename.jpg",
  "caption": "Generated caption text",
  "filename": "filename.jpg"
}
```

## Configuration

### File Size Limit
Maximum upload size: **16MB** (configurable in `app.py`)

### Allowed Extensions
PNG, JPG, JPEG, GIF, WebP

### Model Inference
- Uses GPU (CUDA) if available
- Falls back to CPU otherwise
- First run will download the model (~1.5GB)

## Performance Notes

- **First run**: Model download takes a few minutes (~1.5GB)
- **Caption generation**: 2-10 seconds depending on hardware
- **GPU inference**: 2-3 seconds typical
- **CPU inference**: 10-30 seconds typical

## Troubleshooting

### Model download issues
```bash
# Pre-download the model
python -c "from transformers import pipeline; pipeline('image-to-text', model='Salesforce/blip-image-captioning-base')"
```

### Port already in use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### Memory issues
The app will automatically use CPU if GPU memory is insufficient.

## Requirements

- Python 3.8+
- 2GB RAM minimum (4GB+ recommended)
- GPU optional but recommended for better performance
- 2GB disk space for the model

## Future Enhancements

- [ ] Support for batch image uploads
- [ ] Caption length customization
- [ ] Model selection (different vision-language models)
- [ ] Image history and download
- [ ] API key authentication
- [ ] Database integration for storing results

## License

This project is open source and available under the MIT License.

## Credits

- **BLIP Model**: Salesforce Research
- **Transformers**: Hugging Face
- **Flask**: Pallets

## Deploying to Render (serve frontend + backend together)

You can deploy the entire application (Flask backend that also serves the static frontend) to Render so both the API and the UI live on the same domain.

1. Create a Render account and connect your GitHub repository.
2. Create a new **Web Service** and point it at the `main` branch of this repo.
  - **Environment**: `Python`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
3. You can also include the provided `render.yaml` in the repo and use Render's "Create a new service from render.yaml" workflow.
4. The app will serve the static UI at `/` and the API at `/upload`. Uploaded images are served from `/uploads/<filename>`.

Notes:
- We included a `Procfile` so other PaaS systems (Heroku-like) can also use the `gunicorn` start command.
- If you want a separate static frontend served from GitHub Pages, set `BACKEND_URL` in `templates/index.html` to the Render service URL (e.g. `https://your-service.onrender.com`). For a combined deployment you can leave `BACKEND_URL` as an empty string so the JS uses the same origin.
- For security, restrict CORS to your frontend domain when ready for production (see `app.py`).
