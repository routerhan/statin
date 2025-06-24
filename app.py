import os
from flask import Flask, render_template, request, jsonify
from statin_logic import get_statin_recommendation # Import the refactored logic

app = Flask(__name__)

# Define app constants for easy updates
APP_VERSION = "v1.0.0"
COPYRIGHT_HOLDER = "National Cheng Kung University Department of Engineering Science"

@app.route('/')
def index():
    """Renders the main HTML page for the Statin tool."""
    return render_template('index.html', version=APP_VERSION, copyright=COPYRIGHT_HOLDER)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    """
    API endpoint to receive clinical data and return statin recommendations.
    Uses AJAX for real-time updates.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': "No input data."}), 400

        # 檢查是否缺少必要的欄位
        required_keys = ['ck_value', 'transaminase', 'bilirubin', 'muscle_symptoms']
        if not all(key in data and data[key] is not None for key in required_keys):
            return jsonify({'success': False, 'error': "Missing required fields。"}), 400

        # 驗證並轉換數值
        ck_value = float(data['ck_value'])
        transaminase = float(data['transaminase'])
        bilirubin = float(data['bilirubin'])
        muscle_symptoms = bool(data['muscle_symptoms'])

        # 檢查數值是否為負數
        if ck_value < 0 or transaminase < 0 or bilirubin < 0:
            return jsonify({'success': False, 'error': "Value cannot be negative。"}), 400

        recommendation = get_statin_recommendation(ck_value, transaminase, bilirubin, muscle_symptoms)

        return jsonify({'success': True, 'recommendation': recommendation})
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': "Input invalid format."}), 400
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({'success': False, 'error': "An unexpected error occurred."}), 500

if __name__ == '__main__':
    # For development, run with debug=True.
    # In production, use a production-ready WSGI server like Gunicorn.
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))