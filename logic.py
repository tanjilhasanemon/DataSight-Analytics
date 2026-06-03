import pandas as pd
import re

def analyze_career_data(dataset_path, user_skills_input, wfh_only=False):
    """
    Enterprise processor: Calculates skill gaps, salaries, companies, and raw chart data.
    """
    user_skills = [skill.strip().lower() for skill in user_skills_input.split(',') if skill.strip()]
    
    core_skills = [
        "python", "sql", "excel", "tableau", "power bi", "r", 
        "machine learning", "aws", "azure", "spark", "hadoop", 
        "snowflake", "pandas", "statistics", "gcp", "nosql", 
        "data visualization", "git", "java", "scala", "c++", "c#"
    ]
    
    try:
        df = pd.read_csv(dataset_path)
        
        if wfh_only:
            df = df[df['work_from_home'] == True]
            
        if df.empty:
            return {"status": "error", "message": "No jobs found matching these filters."}
            
        df['description'] = df['description'].astype(str).str.lower()
        all_text = " ".join(df['description'])
        
        # Count skills
        skill_counts = {}
        for skill in core_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            count = len(re.findall(pattern, all_text))
            if count > 0:
                skill_counts[skill] = count
                
        top_market_skills_tuples = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        top_market_skills = [skill[0] for skill in top_market_skills_tuples]
        
        # NEW: Save raw dictionary for the charting library
        top_skills_dict = {skill[0]: skill[1] for skill in top_market_skills_tuples}
        
        missing_skills = [skill for skill in top_market_skills if skill not in user_skills]
        matched_skills = [skill for skill in top_market_skills if skill in user_skills]
        match_percentage = (len(matched_skills) / len(top_market_skills)) * 100 if top_market_skills else 0

        # Safely calculate salaries
        df['salary_avg'] = pd.to_numeric(df['salary_avg'], errors='coerce')
        market_avg_salary = df['salary_avg'].mean()
        
        target_salary = market_avg_salary 
        if missing_skills:
            top_missing = missing_skills[0]
            target_jobs = df[df['description'].str.contains(r'\b' + re.escape(top_missing) + r'\b', na=False)]
            if not target_jobs.empty and not pd.isna(target_jobs['salary_avg'].mean()):
                target_salary = target_jobs['salary_avg'].mean()
                
        # Find companies
        top_companies = []
        if matched_skills:
            best_skill = matched_skills[0]
            matched_jobs = df[df['description'].str.contains(r'\b' + re.escape(best_skill) + r'\b', na=False)]
            top_companies = matched_jobs['company_name'].dropna().value_counts().head(5).index.tolist()
        else:
            top_companies = df['company_name'].dropna().value_counts().head(5).index.tolist()

        return {
            "status": "success",
            "top_market_skills": top_market_skills,
            "top_skills_dict": top_skills_dict,
            "user_skills": user_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_percentage": round(match_percentage),
            "market_salary": market_avg_salary,
            "target_salary": target_salary,
            "top_companies": top_companies,
            "total_jobs_analyzed": len(df)
        }
        
    except FileNotFoundError:
        return {"status": "error", "message": f"Dataset file not found at {dataset_path}."}
    except Exception as e:
        return {"status": "error", "message": f"System error: {e}"}