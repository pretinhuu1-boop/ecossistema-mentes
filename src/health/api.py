from flask import Flask, jsonify
from .engine import HealthCheckEngine

class HealthAPI:
    """API para expor status de saúde via HTTP"""
    
    def __init__(self, engine: HealthCheckEngine):
        self.engine = engine
        self.app = Flask(__name__)
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/health', methods=['GET'])
        def health_check():
            status = self.engine.get_status()
            http_status = 200 if status['overall_status'] == 'healthy' else 503
            return jsonify(status), http_status

        @self.app.route('/health/summary', methods=['GET'])
        def health_summary():
            return jsonify(self.engine.get_summary()), 200

        @self.app.route('/health/liveness', methods=['GET'])
        def liveness():
            return jsonify(self.engine.get_liveness()), 200

        @self.app.route('/health/readiness', methods=['GET'])
        def readiness():
            status = self.engine.get_readiness()
            http_status = 200 if status['ready'] else 503
            return jsonify(status), http_status

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)

if __name__ == "__main__":
    engine = HealthCheckEngine()
    api = HealthAPI(engine)
    api.run()
