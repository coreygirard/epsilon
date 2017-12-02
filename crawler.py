import requests
from bs4 import BeautifulSoup
import re

def extractLinks(page):
    regex = re.compile(r'wiki/(?P<page>\w+)"')
    matches = regex.findall(str(page))
    return list(set(matches))

def extractText(page):
    soup = BeautifulSoup(page)
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    text = soup.getText()
    text = re.sub(r'\[\d+\]',' ',text)
    text = re.sub(r'[^A-Za-z0-9\-]',' ',text)
    text = re.sub(r'\n',' ',text)
    text = re.sub(r'[ ]{1,}',' ',text)
    #text = text.split(' ')
    #text = [e for e in text if e != '']
    return text

def extractSummary(page):
    soup = BeautifulSoup(page)
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    text = soup.getText()
    text = re.sub(r'\[\d+\]',' ',text)
    text = re.sub(r'[^A-Za-z0-9\-]',' ',text)
    text = re.sub(r'\n',' ',text)
    text = re.sub(r'[ ]{1,}',' ',text)
    #text = text.split(' ')
    #text = [e for e in text if e != '']
    return text


def scrape(url):
    #try:
        page = requests.get('http://en.wikipedia.org/wiki/'+url).text
        return {'links':extractLinks(page),
                'text':extractText(page),
                'summary':extractSummary(page)}
    #except:
    #    return

def scoreText(text):
    d = {}
    for w in text:
        d[w.lower()] = d.get(w.lower(),0) + 1
    return {k:v for k,v in d.items() if v > 5}

def buildCorpus(urls):
    page = []
    for i,e in enumerate(urls):
        print('{0}/{1}'.format(i,len(urls)))

        temp = scrape(e)
        page.append({'text':temp['text'],
                     'summary':temp['summary'],
                     'title':(re.sub('_',' ',e)).title()})

    return page




urls = '''
Formal_science
Logic
Mathematics
Statistics
Theoretical_computer_science
Game_theory
Decision_theory
Information_theory
Systems_theory
Control_theory
Outline_of_physical_science
Physics
Classical_physics
Modern_physics
Applied_physics
Theoretical_physics
Experimental_physics
Computational_physics
Mechanics
Classical_mechanics
Analytical_mechanics
Continuum_mechanics
Fluid_mechanics
Solid_mechanics
Electromagnetism
Thermodynamics
Molecular_physics
Atomic_physics
Nuclear_physics
Particle_physics
Condensed_matter_physics
Plasma_(physics)
Quantum_mechanics
Introduction_to_quantum_mechanics
Quantum_field_theory
Special_relativity
General_relativity
String_theory
Chemistry
Inorganic_chemistry
Organic_chemistry
Analytical_chemistry
Physical_chemistry
Acid-base_reaction
Supramolecular_chemistry
Solid-state_chemistry
Nuclear_chemistry
Environmental_chemistry
Green_chemistry
Theoretical_chemistry
Astrochemistry
Biochemistry
Crystallography
Food_chemistry
Geochemistry
Materials_science
Photochemistry
Radiochemistry
Stereochemistry
Surface_science
Earth_science
Climatology
Ecology
Edaphology
Environmental_science
Geodesy
Geography
Physical_geography
Geology
Geomorphology
Geophysics
Glaciology
Hydrology
Limnology
Meteorology
Oceanography
Paleoclimatology
Paleoecology
Palynology
Pedology_(soil_study)
Volcanology
Astronomy
Astrophysics
Cosmology
Galactic_astronomy
Planetary_geology
Planetary_science
Star
List_of_life_sciences
Biology
Anatomy
Astrobiology
Biochemistry
Biogeography
Biological_engineering
Biophysics
Behavioral_neuroscience
Biotechnology
Botany
Cell_biology
Conservation_biology
Cryobiology
Developmental_biology
Ecology
Ethnobiology
Ethology
Evolutionary_biology
Introduction_to_evolution
Genetics
Introduction_to_genetics
Gerontology
Immunology
Limnology
Marine_biology
Microbiology
Molecular_biology
Neuroscience
Paleontology
Parasitology
Physiology
Radiobiology
Soil_biology
Sociobiology
Systematics
Toxicology
Zoology
Social_science
Anthropology
Archaeology
Criminology
Demography
Economics
Geography
Human_geography
History
International_relations
Jurisprudence
Linguistics
Pedagogy
Political_science
Psychology
Science_education
Sociology
Applied_science
Engineering
Aerospace_engineering
Agricultural_engineering
Biological_engineering
Biomedical_engineering
Chemical_engineering
Civil_engineering
Computer_science
Computer_engineering
Electrical_engineering
Fire_protection_engineering
Genetic_engineering
Industrial_engineering
Mechanical_engineering
Military_engineering
Mining_engineering
Nuclear_engineering
Operations_research
Robotics
Software_engineering
Web_engineering
Outline_of_health_sciences
Medicine
Veterinary_medicine
Dentistry
Midwifery
Epidemiology
Pharmacy
Nursing
Interdisciplinarity
Applied_physics
Artificial_intelligence
Bioethics
Bioinformatics
Biomedical_engineering
Biostatistics
Cognitive_science
Complex_systems
Computational_linguistics
Cultural_studies
Cybernetics
Environmental_science
Environmental_social_science
Environmental_studies
Ethnic_studies
Evolutionary_psychology
Forensic_science
Forestry
Library_science
Mathematical_and_theoretical_biology
Mathematical_physics
Military_science
Network_science
Neural_engineering
Neuroscience
Science_studies
Scientific_modelling
Semiotics
Sociobiology
Statistics
Systems_science
Urban_planning
Web_science
Philosophy_of_science
History_of_science
Basic_research
Citizen_science
Fringe_science
Protoscience
Pseudoscience
Academic_freedom
Science_policy
Funding_of_science
Scientific_method
Sociology_of_scientific_knowledge
Technoscience
'''


urls = [e for e in urls.split('\n') if e != '']


from pprint import pprint
pprint(urls)

data = buildCorpus(urls)


import json
with open('pages.json','w') as outFile:
    json.dump(data,outFile,indent=4)











