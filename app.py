import os import json import logging from flask import Flask, request, jsonify import requests from dotenv import load_dotenv

load_dotenv()

app = Flask(name)

Configure logging

logging.basicConfig(level=logging.INFO) logger = logging.getLogger(name)

Environment Variables

CIRCLE_API_KEY = os.getenv("CIRCLE_API_KEY") CIRCLE_COMMUNITY_ID = os.getenv("CIRCLE_COMMUNITY_ID") GHL_API_KEY = os.getenv("GHL_API_KEY") # Location API Key

Space Mappings (Loaded from config.json)

with open('config.json') as f: PRODUCT_MAPPING = json.load(f)

def get_circle_headers(): return { "Authorization": f"Token {CIRCLE_API_KEY}", "Content-Type": "application/json" }

def add_to_circle_space(email, name, space_ids): """Adds a user to specific Circle spaces.""" results = [] for space_id in space_ids: url = f"https://api.circle.so/api/v1/space_members" payload = { "email": email, "name": name, "space_id": space_id, "community_id": CIRCLE_COMMUNITY_ID } response = requests.post(url, headers=get_circle_headers(), json=payload) results.append(response.status_code) logger.info(f"Added {email} to space {space_id}: {response.status_code}") return results

def tag_in_ghl(contact_id, tags): """Apply tags to the contact in GoHighLevel for email segmentation.""" url = f"https://rest.gohighlevel.com/v1/contacts/{contact_id}/tags" payload = {"tags": tags} headers = {"Authorization": f"Bearer {GHL_API_KEY}"} response = requests.post(url, headers=headers, json=payload) return response.status_code

@app.route('/webhook/purchase', methods=['POST']) def handle_purchase(): data = request.json

# Extract data from GHL/Stripe Webhook
email = data.get('email')
name = data.get('first_name', 'Customer')
contact_id = data.get('contact_id')
purchased_product_ids = data.get('product_ids', []) # List of IDs from the checkout

if not email or not purchased_product_ids:
    return jsonify({"error": "Missing required data"}), 400

spaces_to_add = set()
tags_to_apply = []

# Conditional Logic for Space Mapping
for prod_id in purchased_product_ids:
    if prod_id in PRODUCT_MAPPING:
        mapping = PRODUCT_MAPPING[prod_id]
        spaces_to_add.update(mapping.get('spaces', []))
        tags_to_apply.extend(mapping.get('tags', []))

# 1. Add to Circle
if spaces_to_add:
    add_to_circle_space(email, name, list(spaces_to_add))

# 2. Tag in GHL (Triggering internal GHL email workflows)
if contact_id and tags_to_apply:
    tag_in_ghl(contact_id, tags_to_apply)

return jsonify({"status": "success", "processed_spaces": list(spaces_to_add)}), 200


if name == 'main': app.run(port=5000)