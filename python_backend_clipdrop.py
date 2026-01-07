#!/usr/bin/env python3
"""
AleaArt Python Backend for Image Generation (Clipdrop API Version)
Generates images using Clipdrop API with art parameters from blockchain
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import io
import base64
import pymongo
from datetime import datetime
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB connection (for metadata only)
mongo_client = None
db = None

# Clipdrop API configuration
CLIPDROP_API_KEY = os.getenv('CLIPDROP_API_KEY')

# Pinata IPFS configuration
PINATA_API_KEY = os.getenv('PINATA_API_KEY')
PINATA_API_SECRET = os.getenv('PINATA_API_SECRET')
PINATA_JWT = os.getenv('PINATA_JWT')

def connect_mongodb():
    """Connect to MongoDB"""
    global mongo_client, db
    try:
        # MongoDB connection string from environment variable
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            print("❌ MONGODB_URI environment variable not set")
            return False

        mongo_client = pymongo.MongoClient(mongodb_uri)
        db = mongo_client['aleart']
        print("✅ Connected to MongoDB")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return False

def upload_to_pinata(image_bytes, filename, metadata=None):
    """Upload image to IPFS via Pinata"""
    try:
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

        files = {
            'file': (filename, io.BytesIO(image_bytes), 'image/png')
        }

        headers = {
            'Authorization': f'Bearer {PINATA_JWT}'
        }

        data = {}
        if metadata:
            data['pinataMetadata'] = json.dumps({
                'name': filename,
                'keyvalues': metadata
            })

        response = requests.post(url, files=files, headers=headers, data=data)

        if response.status_code == 200:
            result = response.json()
            ipfs_hash = result['IpfsHash']
            print(f"✅ Uploaded to IPFS: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"❌ Failed to upload to IPFS: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ Error uploading to IPFS: {e}")
        return None

def save_image_metadata_to_mongodb(user_id, token_id, ipfs_hash, prompt, parameters):
    """Save image metadata to MongoDB"""
    try:
        if db is None:
            return

        image_data = {
            'userId': user_id,
            'tokenId': token_id,
            'ipfsHash': ipfs_hash,
            'prompt': prompt,
            'parameters': parameters,
            'createdAt': datetime.utcnow(),
            'status': 'completed'
        }

        # Upsert the image data
        db.userImages.update_one(
            {'userId': user_id, 'tokenId': token_id},
            {'$set': image_data},
            upsert=True
        )

        print(f"✅ Saved image metadata to MongoDB for token {token_id}")
    except Exception as e:
        print(f"❌ Failed to save metadata to MongoDB: {e}")

@app.route('/generate-image', methods=['POST'])
def generate_image():
    """Generate image using Clipdrop API with art parameters"""
    try:
        data = request.json

        # Extract parameters
        prompt = data.get('prompt', '')
        token_id = data.get('tokenId', 'unknown')
        user_id = data.get('userId', None)  # Add user ID

        # Extract other parameters for metadata (not used by Clipdrop API)
        steps = data.get('steps', 4)
        cfg_scale = data.get('cfg_scale', 7.5)
        seed = data.get('seed', None)
        width = data.get('width', 512)
        height = data.get('height', 512)

        print(f"Generating image for token {token_id}")
        print(f"Prompt: {prompt}")

        if not CLIPDROP_API_KEY:
            return jsonify({
                'success': False,
                'error': 'Clipdrop API key not configured'
            }), 500

        # Create FormData for Clipdrop API
        files = {
            'prompt': (None, prompt)
        }

        headers = {
            'x-api-key': CLIPDROP_API_KEY
        }

        print("🚀 Sending request to Clipdrop API...")

        # Call Clipdrop API
        response = requests.post(
            'https://clipdrop-api.co/text-to-image/v1',
            files=files,
            headers=headers,
            timeout=60  # 60 second timeout for image generation
        )

        if response.status_code != 200:
            print(f"❌ Clipdrop API error: {response.status_code}")
            print(response.text)
            return jsonify({
                'success': False,
                'error': f'Clipdrop API error: {response.status_code}'
            }), 500

        # Get the image data
        image_bytes = response.content

        print(f"✅ Image generated successfully for token {token_id}")
        print(f"📏 Image size: {len(image_bytes)} bytes")

        # Convert to base64 for response
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        # Prepare image data for IPFS upload
        image_filename = f"art_token_{token_id}_{uuid.uuid4().hex[:8]}.png"

        # Upload to IPFS via Pinata
        ipfs_hash = None
        ipfs_url = None

        if PINATA_JWT:
            metadata = {
                'tokenId': str(token_id),
                'userId': str(user_id) if user_id else 'anonymous',
                'prompt': prompt[:50] + '...' if len(prompt) > 50 else prompt
            }

            ipfs_hash = upload_to_pinata(image_bytes, image_filename, metadata)
            if ipfs_hash:
                ipfs_url = f'https://gateway.pinata.cloud/ipfs/{ipfs_hash}'
                print(f"🌐 IPFS URL: {ipfs_url}")
        else:
            print("⚠️ Pinata JWT not configured, skipping IPFS upload")

        # Save metadata to MongoDB if user_id is provided
        parameters = {
            'steps': steps,
            'cfg_scale': cfg_scale,
            'seed': seed,
            'width': width,
            'height': height,
            'api': 'clipdrop'
        }

        if user_id and ipfs_hash:
            save_image_metadata_to_mongodb(user_id, token_id, ipfs_hash, prompt, parameters)

        return jsonify({
            'success': True,
            'imageData': image_base64,
            'ipfsHash': ipfs_hash,
            'ipfsUrl': ipfs_url,
            'tokenId': token_id,
            'prompt': prompt
        })

    except requests.exceptions.Timeout:
        print(f"❌ Timeout error for token {token_id}")
        return jsonify({
            'success': False,
            'error': 'Image generation timed out'
        }), 504

    except Exception as e:
        print(f"❌ Error generating image for token {token_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AleaArt Python Backend (Clipdrop API)',
        'version': '1.0.0',
        'api': 'clipdrop'
    })

if __name__ == '__main__':
    # Connect to MongoDB on startup
    connect_mongodb()

    # Check for required environment variables
    if not CLIPDROP_API_KEY:
        print("⚠️ CLIPDROP_API_KEY environment variable not set")
        print("   Get your API key from: https://clipdrop.co/apis")

    port = int(os.getenv('PORT', 5000))
    print("🎨 Starting AleaArt Python Backend (Clipdrop API Version)...")
    print(f"🔗 Server will run on port {port}")
    print("📡 Ready to generate images with Clipdrop API!")

    app.run(host='0.0.0.0', port=port, debug=True)
