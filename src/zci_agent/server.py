from flask import Flask, request, jsonify
from .core import ZCIAgent

app = Flask(__name__)
agent = ZCIAgent()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "ZCI Agent"}), 200

@app.route('/api/zci/generate', methods=['POST'])
def generate_description():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    product_name = data.get('product_name')
    attributes = data.get('attributes', [])
    
    if not product_name:
        return jsonify({"error": "product_name is required"}), 400
        
    description = agent.generate_description(product_name, attributes)
    return jsonify({"description": description}), 200

@app.route('/api/zci/seo', methods=['POST'])
def optimize_seo():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    text = data.get('text')
    keywords = data.get('keywords', [])
    
    if not text:
        return jsonify({"error": "text is required"}), 400
        
    optimized_text = agent.optimize_seo(text, keywords)
    return jsonify({"optimized_text": optimized_text}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
