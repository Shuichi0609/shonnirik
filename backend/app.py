import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

from api_v1 import api_v1
from core.inference import get_model, OPTIMAL_THRESHOLD

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['CORS_HEADERS'] = 'Content-Type'

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize SocketIO with gevent async mode
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent", logger=True, engineio_logger=True)

# Register blueprints
app.register_blueprint(api_v1, url_prefix='/api/v1')

# Root endpoint
@app.route('/')
def index():
    return jsonify({
        "status": "active",
        "message": "PulmonaryAI API Gateway",
        "version": "1.0.0"
    })

# Health endpoint
@app.route('/health')
def health():
    try:
        # Try to load model to see if it's available
        model = get_model()
        model_loaded = model is not None
    except Exception as e:
        logger.warning(f"Health check model load failed: {e}")
        model_loaded = False

    return jsonify({
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "threshold": OPTIMAL_THRESHOLD if model_loaded else None
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # For development only
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)