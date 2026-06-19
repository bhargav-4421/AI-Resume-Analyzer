from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import traceback

# Import custom modules
from resume_parser import extract_resume_text
from skill_extractor import extract_skills, extract_jd_skills
from analyzer import analyze_resume

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_resume_route():
    try:
        # File check
        if 'resume' not in request.files:
            return jsonify({'success': False, 'error': 'No resume file uploaded'}), 400

        file = request.files['resume']

        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type. Upload PDF or DOCX'}), 400

        # Job description
        job_description = request.form.get('job_description', '').strip()
        if not job_description:
            return jsonify({'success': False, 'error': 'Job description is required'}), 400

        # Extract resume text
        try:
            resume_text = extract_resume_text(file)
            if not resume_text:
                return jsonify({'success': False, 'error': 'Could not extract text from resume'}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

        # Use new dynamic analysis function
        try:
            analysis = analyze_resume(resume_text, job_description)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

        # FINAL RESPONSE
        return jsonify({
            'success': True,
            'match_score': analysis['match_score'],
            'detected_skills': analysis['detected_skills'],
            'missing_keywords': analysis['missing_keywords'],
            'recommendations': analysis['recommendations']
        })

    except Exception as e:
        app.logger.error(f"ERROR: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})


@app.errorhandler(413)
def too_large(e):
    return jsonify({'success': False, 'error': 'File too large'}), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)