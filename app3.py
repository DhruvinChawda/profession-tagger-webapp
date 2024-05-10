import streamlit as st
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
from collections import Counter
from gtts import gTTS
import os

def scrape_person_web_results(query):
    encoded_query = quote(query)
    url = f"https://www.bing.com/search?q={encoded_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        web_results = soup.select('li.b_algo')

        descriptions = []
        for result in web_results:
            description = result.select_one('div.b_caption > p, div.b_snippet > p')
            if description:
                descriptions.append(description.text.strip())
            else:
                fallback_description = result.find('p')
                if fallback_description:
                    descriptions.append(fallback_description.text.strip())
                else:
                    descriptions.append("Description not available.")

        return descriptions
    except requests.RequestException as e:
        return [f"An error occurred: {str(e)}"]

def extract_skills(web_results, skills_keywords):
    skills_found = set()
    for description in web_results:
        for skill in skills_keywords:
            if re.search(re.escape(skill), description, re.IGNORECASE):
                skills_found.add(skill)
    return list(skills_found)

def determine_profession(skills_list):
    profession_counter = Counter()

    for profession, skills in profession_skills.items():
        profession_counter[profession] = sum(skill in skills_list for skill in skills)

    max_skills = profession_counter.most_common(1)

    if max_skills[0][1] > 0:
        return max_skills[0][0]
    else:
        return 'Unknown'

# Predefined list of skills to look for
skills_keywords = ['Artificial intelligence','AI','ML', 'Cybersecurity', 'Software Development', 'NPM', 'command-line interface', 'CLI', 'user centric experiences', 'robust and performant software','Computer Science & Engineering',
    'Speech Recognition',
    'Feature Extraction',
    'Real-Time Systems',
    'Coalmine Safety',
    'Academic Research',
    'Internet of Things',
    'Image Classification',
    'Handicapped Aids',
    'Agriculture Technology',
    'Avionics',
    'Behavioural Sciences Computing',
    'Biological Systems',
    'Cloud Computing',
    'Educational Qualification',
    'Ph.D. in Computer Science',
    'Machine Learning',
    'Data Science',
    'AI Ethics',
    'Software Development',
    'Technology Diffusion',
    'Word Ambiguity Resolution','ph.D.','professor','graphic designer','blockchain','Full Stack Developer','batsman','crickter','athelete','batting','bowling',
    'wicket keeper','fielder','chinaman','leg spinner','off-spinner','leg break','pacer','adult film industry','pornographic','batter','bowler',
    'politics','politician','party','BJP','congress','aap','prime minister','chief minister','home minister','minister','lok sabha','parliament','Pokémon','bollywood',
    'hollywood','singer','filmfare','golden globe',"film", "movie", "cinema", "production", "screening", "premiere",
    "festival", "casting", "shoot", "scene", "take", "cut", "edit",
    "sequence", "frame", "soundtrack", "credits", "director's cut", "box office","actor", "actress", "performer", "casting", "role", "character",
    "lead", "supporting role", "cameo", "monologue", "audition", "method acting","football", "soccer", "player", "goal", "assist", "clean sheet", "forward",
    "midfielder", "defender", "goalkeeper", "captain", "free kick", "penalty",
    "corner kick", "tackle", "offside", "dribble", "cross", "header", "league",
    "cup", "championship", "match", "fixture", "season", "transfer", "contract",
    "injury", "recovery", "training", "fitness", "tactics", "formation", "coach",
    "manager", "substitute", "yellow card", "red card", "VAR", "fans", "stadium",
    "club", "team", "international cap", "hat-trick", "brace", "debut", "retirement","database", "DBMS", "SQL", "NoSQL", "MySQL", "PostgreSQL", "Oracle", "SQL Server",
    "MongoDB", "Cassandra", "Redis", "database design", "data modeling", "ERD", "entity-relationship diagram",
    "normalization", "denormalization", "indexing", "query optimization", "transaction", "concurrency control",
    "ACID properties", "replication", "sharding", "partitioning", "backup", "recovery",
    "performance tuning", "stored procedures", "triggers", "views", "data warehousing",
    "ETL", "Extract Transform Load", "data migration", "database administration", "database security",
    "data integrity", "data analysis", "business intelligence", "SQL injection", "database audit",
    "schema", "DDL", "DML", "DCL", "T-SQL", "PL/SQL", "database connectivity", "JDBC", "ODBC",
    "API", "data governance", "data management", "cloud databases", "AWS RDS", "Azure SQL Database",
    "Google Cloud SQL", "data lake", "big data", "Hadoop", "Spark"]

# Sample dictionary of professions and related skills
profession_skills = {
    'Pokémon' : ['Pokémon'],

    'cricketer' : ['batting','bowling','wicket keeper','fielder','chinaman','leg spinner','off-spinner','leg break','pacer','batter','bowler'],

    'Software Developer': ['programming', 'Software Development', 'debugging','Full Stack Developer','React',],

    'Data Scientist': ['machine learning', 'data visualization', 'statistics','AI'],

    'Graphic Designer': ['creativity', 'design', 'Photoshop'],

    'Mechanical Engineer': ['CAD', 'mechanical knowledge', 'problem solving'],

    'Professor' : ['ph.D.','professor'],

    'Designer' : ['graphic designer','canva','figma','digital art'],

    'pornstar' : ['adult film industry','pornographic'],

    'Politician' : ['politics','politician','party','BJP','congress','aap','prime minister','chief minister','home minister','minister','lok sabha','parliament'],

    'Film Industry Artist' : ["actor", "actress", "performer", "casting", "role", "character","lead", "supporting role", "cameo", "monologue", "audition", "method acting","film", "movie", "cinema", "production", "screening", "premiere",
    "festival", "casting", "shoot", "scene", "take", "cut", "edit",
    "sequence", "frame", "soundtrack", "credits", "director's cut", "box office"],
    'Profession Footballer' : ["football", "soccer", "player", "goal", "assist", "clean sheet", "forward",
    "midfielder", "defender", "goalkeeper", "captain", "free kick", "penalty",
    "corner kick", "tackle", "offside", "dribble", "cross", "header", "league",
    "cup", "championship", "match", "fixture", "season", "transfer", "contract",
    "injury", "recovery", "training", "fitness", "tactics", "formation", "coach",
    "manager", "substitute", "yellow card", "red card", "VAR", "fans", "stadium",
    "club", "team", "international cap", "hat-trick", "brace", "debut", "retirement"],

    'Database management role' : ["database", "DBMS", "SQL", "NoSQL", "MySQL", "PostgreSQL", "Oracle", "SQL Server",
    "MongoDB", "Cassandra", "Redis", "database design", "data modeling", "ERD", "entity-relationship diagram",
    "normalization", "denormalization", "indexing", "query optimization", "transaction", "concurrency control",
    "ACID properties", "replication", "sharding", "partitioning", "backup", "recovery",
    "performance tuning", "stored procedures", "triggers", "views", "data warehousing",
    "ETL", "Extract Transform Load", "data migration", "database administration", "database security",
    "data integrity", "data analysis", "business intelligence", "SQL injection", "database audit",
    "schema", "DDL", "DML", "DCL", "T-SQL", "PL/SQL", "database connectivity", "JDBC", "ODBC",
    "API", "data governance", "data management", "cloud databases", "AWS RDS", "Azure SQL Database",
    "Google Cloud SQL", "data lake", "big data", "Hadoop", "Spark"]

}
st.set_page_config(
    page_title="MOSIAC",
    page_icon=":search:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Streamlit UI
st.title('MOSIAC : PROFESSION TAG GENERATOR')

#background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://static4.depositphotos.com/1018174/428/i/450/depositphotos_4288236-stock-photo-spotlight-studio-interior-perfect-background.jpg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Sidebar for user input
query = st.sidebar.text_input('ENTER PERSON NAME :',placeholder='Enter name here...')
st.sidebar.markdown('---')
search = st.sidebar.button('GENERATE RESULTS')


# Main content
if search :
#if st.button('Search'):
    web_results = scrape_person_web_results(query)
    extracted_skills = extract_skills(web_results, skills_keywords)
    profession_tag = determine_profession(extracted_skills)

     # Display description and extracted skills side by side in boxes
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Web Results Descriptions:')
        for i, description in enumerate(web_results, start=1):
            #st.markdown(f'<p style="font-family:sans-serif; font-size:21px; color:#333;">{i}. {description}</p>', unsafe_allow_html=True)
            st.markdown(f'<div style="border: 1px solid #ccc; padding: 5px; margin-bottom: 10px;"><p style="font-family:sans-serif; color:#333;">{i}. {description}</div>', unsafe_allow_html=True)

    with col2:
        st.subheader('Extracted Skills:')
        for skill in extracted_skills:
            #st.text(skill)
            st.markdown(f'<div style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;">{skill}</div>', unsafe_allow_html=True)

    # Display profession tag
    st.success(f'Predicted Profession: {profession_tag}')

    # Text-to-speech functionality
    if st.button(' Audio 🔊 '):
        tts = gTTS(profession_tag)
        tts.save('output.mp3')
        os.system("start output.mp3")
        
