from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_code_file:
        temp_code_file.write(code.encode())
        temp_code_file.close()
        try:
            result = subprocess.run(['python3', temp_code_file.name], capture_output=True, text=True, timeout=10)
            output = result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            output = str(e)
        finally:
            os.remove(temp_code_file.name)

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
