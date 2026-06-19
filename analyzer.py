from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import string
from typing import Tuple, Dict

def preprocess_text(text: str) -> str:
    """
    Preprocess text by removing punctuation, converting to lowercase, and normalizing whitespace.
    
    Args:
        text (str): Input text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def calculate_match_score(resume_text: str, job_description: str) -> float:
    """
    Calculate similarity score between resume text and job description using TF-IDF and cosine similarity.
    
    Args:
        resume_text (str): Resume text to analyze
        job_description (str): Job description to compare against
        
    Returns:
        float: Match percentage (0-100)
    """
    if not resume_text or not job_description:
        return 0.0
    
    try:
        documents = [resume_text, job_description]
        
        vectorizer = TfidfVectorizer(stop_words="english")
        
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
        score = similarity[0][0] * 100
        
        return round(score, 2)
        
    except Exception as e:
        print(f"Error calculating match score: {str(e)}")
        return 0.0

SKILL_DB = {
    "data_science": [
        "python","pandas","numpy","matplotlib","seaborn",
        "scikit-learn","machine learning","statistics",
        "data analysis","data visualization","sql"
    ],

    "web_development": [
        "html","css","javascript","react","node","express",
        "mongodb","api","frontend","backend"
    ],

    "ai_ml": [
        "python","machine learning","deep learning",
        "tensorflow","pytorch","nlp","computer vision"
    ],

    "java_developer": [
        "java","spring","spring boot","hibernate",
        "mysql","rest api","oop"
    ],

    "common": [
        "git","github","communication","problem solving"
    ]
}

def detect_domain(jd):
    jd = jd.lower()

    if "data science" in jd or "data analyst" in jd:
        return "data_science"
    elif "web" in jd or "frontend" in jd or "backend" in jd:
        return "web_development"
    elif "machine learning" in jd or "ai" in jd:
        return "ai_ml"
    elif "java" in jd:
        return "java_developer"
    else:
        return "common"

def analyze_resume(resume_text, job_description):
    resume_text = resume_text.lower()
    job_description = job_description.lower()

    domain = detect_domain(job_description)

    domain_skills = SKILL_DB.get(domain, [])
    common_skills = SKILL_DB["common"]

    required_skills = list(set(domain_skills + common_skills))

    detected_skills = [s for s in required_skills if s in resume_text]
    missing_skills = [s for s in required_skills if s not in resume_text]

    if len(required_skills) == 0:
        score = 0
    else:
        score = int((len(detected_skills) / len(required_skills)) * 100)

    recommendations = []

    if missing_skills:
        recommendations.append("Improve your profile by adding these skills:")
        recommendations.append(", ".join(missing_skills[:10]))
        recommendations.append("Work on real projects using these technologies")
    else:
        recommendations.append("Your resume matches most required skills")

    return {
        "match_score": score,
        "detected_skills": detected_skills,
        "missing_keywords": missing_skills,
        "recommendations": recommendations
    }

def find_missing_skills(resume_skills, jd_skills):
    """
    Find skills that are in job description but not in resume.
    
    Args:
        resume_skills (list): Skills extracted from resume
        jd_skills (list): Skills extracted from job description
        
    Returns:
        list: List of missing skills
    """
    missing = []
    
    resume_lower = [s.lower() for s in resume_skills]
    
    for skill in jd_skills:
        if skill.lower() not in resume_lower:
            missing.append(skill)
    
    return missing

def generate_recommendations(match_score, missing_keywords):
    """
    Generate recommendations based on match score and missing skills.
    
    Args:
        match_score (float): Match percentage (0-100)
        missing_keywords (list): Skills missing from resume
        
    Returns:
        list: List of recommendations
    """
    recommendations = []
    
    if match_score >= 70:
        recommendations.append("Excellent match! Your resume aligns well with job requirements.")
        recommendations.append("Consider highlighting your strongest technical skills in your summary.")
        if missing_keywords:
            recommendations.append(f"Minor improvement: Add experience with {', '.join(missing_keywords[:2])} if applicable.")
    elif match_score >= 40:
        recommendations.append("Good match with room for improvement.")
        if missing_keywords:
            skills_text = ', '.join(missing_keywords[:3])
            recommendations.append(f"Focus on gaining experience in: {skills_text}")
            recommendations.append(f"Consider adding projects related to {missing_keywords[0] if missing_keywords else 'key technologies'}")
        recommendations.append("Quantify your achievements with specific metrics.")
    else:
        recommendations.append("Significant improvements needed to align with job requirements.")
        if missing_keywords:
            skills_text = ', '.join(missing_keywords[:5])
            recommendations.append(f"Priority: Develop skills in {skills_text}")
            recommendations.append(f"Add projects related to {missing_keywords[0] if missing_keywords else 'required technologies'}")
            recommendations.append(f"Include relevant experience for {missing_keywords[1] if len(missing_keywords) > 1 else 'key skills'}")
        recommendations.append("Consider taking courses or certifications for missing skills.")
        recommendations.append("Reorganize resume to highlight relevant experience.")
    
    return recommendations

def batch_compare(resumes: list, job_description: str) -> list:
    """
    Compare multiple resumes against a single job description.
    
    Args:
        resumes (list): List of resume texts
        job_description (str): Job description to compare against
        
    Returns:
        list: List of tuples (resume_index, match_score)
    """
    results = []
    
    for i, resume in enumerate(resumes):
        score = calculate_match_score(resume, job_description)
        results.append((i, score))
    
    # Sort by match score (descending)
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results

# Example usage and testing
if __name__ == "__main__":
    # Sample resume and job description for testing
    sample_resume = """
    Experienced software developer with 5 years of experience in Python, Java, and JavaScript.
    Proficient in machine learning frameworks like TensorFlow and PyTorch.
    Strong background in web development using React, HTML, and CSS.
    Experience with SQL databases and cloud platforms like AWS.
    """
    
    sample_job_description = """
    We are looking for a Senior Software Developer with experience in Python and Java.
    The ideal candidate should have experience with machine learning, TensorFlow, and React.
    Knowledge of SQL databases and cloud platforms is required.
    Experience with DevOps tools like Docker is a plus.
    """
    
    # Calculate match score
    score = calculate_match_score(sample_resume, sample_job_description)
    print(f"Match Score: {score}%")
    
    # Get detailed analysis
    analysis = analyze_resume(sample_resume, sample_job_description)
    print("\nDetailed Analysis:")
    print(f"Detected Skills: {analysis['detected_skills']}")
    print(f"Missing Keywords: {analysis['missing_keywords']}")
    print(f"Recommendations: {analysis['recommendations']}")
