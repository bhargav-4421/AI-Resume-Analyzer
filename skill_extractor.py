import spacy
import re
from typing import List

# Load the spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Comprehensive list of technical skills and technologies
TECHNICAL_SKILLS = {
    'programming_languages': [
        'Python', 'Java', 'JavaScript', 'C++', 'C#', 'Ruby', 'Go', 'Rust',
        'PHP', 'Swift', 'Kotlin', 'Scala', 'Perl', 'R', 'MATLAB', 'TypeScript'
    ],
    'web_technologies': [
        'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js',
        'Django', 'Flask', 'Spring Boot', 'ASP.NET', 'Laravel', 'Rails',
        'jQuery', 'Bootstrap', 'Tailwind CSS', 'SASS', 'LESS'
    ],
    'databases': [
        'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQLite',
        'Cassandra', 'Elasticsearch', 'DynamoDB', 'Firebase', 'Supabase'
    ],
    'cloud_platforms': [
        'AWS', 'Azure', 'Google Cloud', 'GCP', 'Heroku', 'DigitalOcean',
        'Vercel', 'Netlify', 'Firebase', 'Alibaba Cloud'
    ],
    'machine_learning': [
        'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Keras',
        'Scikit-learn', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'NLTK',
        'OpenCV', 'Hugging Face', 'XGBoost', 'LightGBM', 'CatBoost',
        'Data Science', 'Data Analysis', 'Statistical Analysis', 'Predictive Modeling',
        'Natural Language Processing', 'Computer Vision', 'Reinforcement Learning',
        'Time Series Analysis', 'Feature Engineering', 'Model Deployment', 'MLOps'
    ],
    'devops_tools': [
        'Docker', 'Kubernetes', 'Jenkins', 'Git', 'GitHub', 'GitLab',
        'CI/CD', 'Terraform', 'Ansible', 'Bash', 'Linux', 'Ubuntu',
        'Nginx', 'Apache', 'Webpack', 'Vite'
    ],
    'mobile_development': [
        'React Native', 'Flutter', 'Swift', 'Kotlin', 'iOS', 'Android',
        'Xamarin', 'Ionic', 'Cordova'
    ],
    'other_technologies': [
        'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum', 'JIRA',
        'Figma', 'Adobe XD', 'Sketch', 'Tableau', 'Power BI', 'Excel',
        'Selenium', 'Cypress', 'Jest', 'Mocha', 'Pytest'
    ]
}

def extract_skills(text: str) -> List[str]:
    """
    Extract technical skills from resume text using spaCy and keyword matching.
    
    Args:
        text (str): Resume text to analyze
        
    Returns:
        List[str]: List of detected technical skills
    """
    if not text or not isinstance(text, str):
        return []
    
    # Process text with spaCy
    doc = nlp(text.lower())
    
    detected_skills = set()
    
    # Method 1: Direct keyword matching
    all_skills = []
    for category, skills in TECHNICAL_SKILLS.items():
        all_skills.extend(skills)
    
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    for skill in all_skills:
        skill_lower = skill.lower()
        # Check for exact word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, text_lower):
            detected_skills.add(skill)
    
    # Method 2: Named Entity Recognition for additional context
    for ent in doc.ents:
        # Check if entity matches any known skill
        ent_text = ent.text.title()
        for skill in all_skills:
            if skill.lower() == ent.text.lower():
                detected_skills.add(skill)
    
    # Method 3: Check noun chunks and tokens for potential skills
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.title()
        for skill in all_skills:
            if skill.lower() in chunk_text.lower():
                detected_skills.add(skill)
    
    # Method 4: Check individual tokens
    for token in doc:
        token_text = token.text.title()
        for skill in all_skills:
            if skill.lower() == token.text.lower():
                detected_skills.add(skill)
    
    # Convert to sorted list
    return sorted(list(detected_skills))

def get_skills_by_category(text: str) -> dict:
    """
    Extract skills grouped by category.
    
    Args:
        text (str): Resume text to analyze
        
    Returns:
        dict: Dictionary with categories as keys and skill lists as values
    """
    detected_skills = extract_skills(text)
    categorized_skills = {}
    
    for category, skills in TECHNICAL_SKILLS.items():
        category_skills = [skill for skill in detected_skills if skill in skills]
        if category_skills:
            categorized_skills[category] = category_skills
    
    return categorized_skills

def get_skill_count(text: str) -> int:
    """
    Get the total count of detected skills.
    
    Args:
        text (str): Resume text to analyze
        
    Returns:
        int: Number of detected skills
    """
    return len(extract_skills(text))

def extract_jd_skills(job_description):
    """
    Extract skills from job description using the same comprehensive skills database.
    
    Args:
        job_description (str): Job description text
        
    Returns:
        list: List of found skills
    """
    if not job_description or not isinstance(job_description, str):
        return []
    
    # Use the same comprehensive skills database as extract_skills
    all_skills = []
    for category, skills in TECHNICAL_SKILLS.items():
        all_skills.extend(skills)
    
    found = []
    jd_lower = job_description.lower()
    
    for skill in all_skills:
        skill_lower = skill.lower()
        # Check for exact word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, jd_lower):
            found.append(skill)
    
    return sorted(found)

# Example usage and testing
if __name__ == "__main__":
    # Sample resume text for testing
    sample_text = """
    I am a software developer with experience in Python, Java, and JavaScript.
    I have worked with Machine Learning frameworks like TensorFlow and PyTorch.
    My web development skills include React, HTML, CSS, and Node.js.
    I am proficient in SQL databases like MySQL and PostgreSQL.
    I have experience with cloud platforms like AWS and Docker for DevOps.
    """
    
    skills = extract_skills(sample_text)
    print("Detected Skills:", skills)
    
    categorized = get_skills_by_category(sample_text)
    print("\nSkills by Category:")
    for category, skill_list in categorized.items():
        print(f"{category}: {skill_list}")
    
    print(f"\nTotal skills detected: {get_skill_count(sample_text)}")