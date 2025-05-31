# LLM logic for dashboard

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

#Soft SKills
# Prompt logic to generate top 5 SOFT skills from google gemini LLM
def generate_soft_skills(text_blob, job_title):
    prompt = f"""
    Analysera följande platsannons för rollen '{job_title}' 
    och extrahera **de 5 viktigaste mjuka färdigheterna (soft skills)** som efterfrågas.
    **Översätt alla kompetensnamn till svenska.** 
    Returnera resultatet i **giltigt JSON-format**, t.ex. så här:
    {{
    "Skill 1": 7,
    "Skill 2": 6,
    "Skill 3": 9,
    "Skill 4": 5,
    "Skill 5": 8
    }}
    Returnera **endast** JSON-objektet.

    {text_blob}
    """
    return model.generate_content(prompt).text

#HARD Skills
# Prompt logic to generate top 5 HARD skills from google gemini LLM
def generate_hard_skills(text_blob, job_title):
    prompt = f"""
    Analysera följande platsannons för rollen '{job_title}'.
    Identifiera de **5 viktigaste hårda färdigheterna** (hard skills) som en idealisk kandidat bör ha.
    Dessa är **tekniska eller uppgiftsspecifika** färdigheter (inte mjuka färdigheter som kommunikation eller samarbete).
    Returnera och översätt färdighetsnamnen på **svenska** i **JSON-format**, enligt detta exempel:
    {{
    "Skill A": 9,
    "Skill B": 8,
    "Skill C": 6,
    "Skill D": 6,
    "Skill E": 5
    }}

    Endast inkludera färdigheter som tydligt nämns eller starkt antyds i beskrivningen.
    Ge varje färdighet ett värde från 1 till 10 baserat på dess vikt.

    Platsannons:
    {text_blob}
    """
    return model.generate_content(prompt).text

# Summary of candidate profile based on hard skills
# Includes personality prompt for AI HR assistant 'HiRe'
def generate_hard_skills_summary(employer_name, job_title, text_blob):

    prompt = f"""
    Du är en HR-assistent som analyserar platsannonser åt rekryterare.

    Skriv en professionell sammanfattning på 3-4 meningar riktad till en rekryterare.
    Beskriv att **{employer_name}** söker en **{job_title}**,
    och inkludera att kandidaten bör ha följande tekniska färdigheter ("hard skills").
    Använd **fet stil** på de viktigaste tre färdigheterna.

    Målet är att ge en snabb HR-överblick: beskriv vilken typ av teknisk bakgrund, erfarenhet eller
    expertis kandidaten bör ha.
    Formulera svaret på flytande svenska, med en ton som låter som en mänsklig HR-expert.
    
    Platsannons:

    {text_blob}
    """
    return model.generate_content(prompt).text.strip()


# Field average prompt logic
def generate_field_average_soft_skills(text_blob, field):
    prompt = f"""
    Analysera dessa platsannonser för yrkesområdet '{field}'.
    Returnera de **5 mest frekvent betonade mjuka färdigheterna** (soft skills) över alla roller.
    Returnera färdighetsnamnen på **svenska** i **giltigt JSON-format**, enligt detta exempel:
    {{
    "Skill 1": 7,
    "Skill 2": 6,
    "Skill 3": 9,
    "Skill 4": 5,
    "Skill 5": 5
    }}
    
    Returnera endast JSON-objektet.
    
    Platsannonser:
    {text_blob}
    """
    return model.generate_content(prompt).text

# Field prompts return lots of double strings which cause string
# mismatch. So to get the field vs select_job to overlap this mapping
# cleans up mutlilabels such as Teamwork/Collaboration: Teamwork

def clean_skill_labels(skills_dict):
    mapping = {
        "Teamwork/Samarbetsförmåga": "Samarbetsförmåga",
        "Teamwork": "Samarbetsförmåga",
        "Flexibilitet/Anpassningsförmåga": "Anpassningsförmåga",
        "Skriftlig & Muntlig Kommunikation": "Kommunikation",
        "Skriftlig/Muntlig Kommunikation": "Kommunikation",
        "Kommunikationsförmåga": "Kommunikation",
        "Kreativt Tänkande": "Kreativitet",
        "Problemlösning & Beslutsfattande": "Problemlösning",
        "Initiativtagande/Proaktiv": "Initiativtagande"
        # fler varianter kan läggas till vid behov
    }
    # k = original skill name (key)
    # v = skill score
    return {mapping.get(k, k): v for k, v in skills_dict.items()}
    # looks up k(key) in mapping directory above and replaces it, and
    # if not found, keeps as is. Keeps original values intact.

# Static + personality-based greeting phrase from "HiRe - the HR assistant"
def get_ai_intro():
    return (
        "\U0001F9D1\u200D\U0001F4BB **Hej, jag heter HiRe och är din Talent Acquisition-assistent.** "
        "Välj en yrkestitel i rutan nedan så hjälper jag dig att hitta den perfekta kandidaten till jobbet."
    )