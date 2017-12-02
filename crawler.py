import requests
from bs4 import BeautifulSoup
import re




def cleanText(text):
    text = re.sub(r'\n',' ',text)
    text = re.sub(r'\[\d+\]',' ',text)
    text = re.sub(r'[^A-Za-z0-9\-.]',' ',text)
    text = re.sub(r'[ ]{1,}',' ',text)
    return text

def extractLinks(page):
    regex = re.compile(r'wiki/(?P<page>\w+)"')
    matches = regex.findall(str(page))
    return list(set(matches))

def extractText(page):
    soup = BeautifulSoup(page)
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    text = soup.getText()
    text = cleanText(text)
    return text

def extractSummary(page):
    text = extractText(page)
    text = text[:text.find(' ',300)] + ' ...'
    return text


def scrape(url):
    #try:
        page = requests.get('http://en.wikipedia.org/wiki/'+url).text
        return {'links':extractLinks(page),
                'text':extractText(page),
                'summary':extractSummary(page)}
    #except:
    #    return

def buildCorpus(urls):
    page = []
    for i,e in enumerate(urls):
        print('{0}/{1}'.format(i,len(urls)))

        temp = scrape(e)
        page.append({'text':temp['text'],
                     'summary':temp['summary'],
                     'title':(re.sub('_',' ',e)).title()})

    return page



urls = ['Formal_science', 'Logic', 'Mathematics', 'Statistics', 'Theoretical_computer_science', 'Game_theory', 'Decision_theory', 'Information_theory', 'Systems_theory', 'Control_theory', 'Outline_of_physical_science', 'Physics', 'Classical_physics', 'Modern_physics', 'Applied_physics', 'Theoretical_physics', 'Experimental_physics', 'Computational_physics', 'Mechanics', 'Classical_mechanics', 'Analytical_mechanics', 'Continuum_mechanics', 'Fluid_mechanics', 'Solid_mechanics', 'Electromagnetism', 'Thermodynamics', 'Molecular_physics', 'Atomic_physics', 'Nuclear_physics', 'Particle_physics', 'Condensed_matter_physics', 'Plasma_(physics)', 'Quantum_mechanics', 'Introduction_to_quantum_mechanics', 'Quantum_field_theory', 'Special_relativity', 'General_relativity', 'String_theory', 'Chemistry', 'Inorganic_chemistry', 'Organic_chemistry', 'Analytical_chemistry', 'Physical_chemistry', 'Acid-base_reaction', 'Supramolecular_chemistry', 'Solid-state_chemistry', 'Nuclear_chemistry', 'Environmental_chemistry', 'Green_chemistry', 'Theoretical_chemistry', 'Astrochemistry', 'Biochemistry', 'Crystallography', 'Food_chemistry', 'Geochemistry', 'Materials_science', 'Photochemistry', 'Radiochemistry', 'Stereochemistry', 'Surface_science', 'Earth_science', 'Climatology', 'Ecology', 'Edaphology', 'Environmental_science', 'Geodesy', 'Geography', 'Physical_geography', 'Geology', 'Geomorphology', 'Geophysics', 'Glaciology', 'Hydrology', 'Limnology', 'Meteorology', 'Oceanography', 'Paleoclimatology', 'Paleoecology', 'Palynology', 'Pedology_(soil_study)', 'Volcanology', 'Astronomy', 'Astrophysics', 'Cosmology', 'Galactic_astronomy', 'Planetary_geology', 'Planetary_science', 'Star', 'List_of_life_sciences', 'Biology', 'Anatomy', 'Astrobiology', 'Biochemistry', 'Biogeography', 'Biological_engineering', 'Biophysics', 'Behavioral_neuroscience', 'Biotechnology', 'Botany', 'Cell_biology', 'Conservation_biology', 'Cryobiology', 'Developmental_biology', 'Ecology', 'Ethnobiology', 'Ethology', 'Evolutionary_biology', 'Introduction_to_evolution', 'Genetics', 'Introduction_to_genetics', 'Gerontology', 'Immunology', 'Limnology', 'Marine_biology', 'Microbiology', 'Molecular_biology', 'Neuroscience', 'Paleontology', 'Parasitology', 'Physiology', 'Radiobiology', 'Soil_biology', 'Sociobiology', 'Systematics', 'Toxicology', 'Zoology', 'Social_science', 'Anthropology', 'Archaeology', 'Criminology', 'Demography', 'Economics', 'Geography', 'Human_geography', 'History', 'International_relations', 'Jurisprudence', 'Linguistics', 'Pedagogy', 'Political_science', 'Psychology', 'Science_education', 'Sociology', 'Applied_science', 'Engineering', 'Aerospace_engineering', 'Agricultural_engineering', 'Biological_engineering', 'Biomedical_engineering', 'Chemical_engineering', 'Civil_engineering', 'Computer_science', 'Computer_engineering', 'Electrical_engineering', 'Fire_protection_engineering', 'Genetic_engineering', 'Industrial_engineering', 'Mechanical_engineering', 'Military_engineering', 'Mining_engineering', 'Nuclear_engineering', 'Operations_research', 'Robotics', 'Software_engineering', 'Web_engineering', 'Outline_of_health_sciences', 'Medicine', 'Veterinary_medicine', 'Dentistry', 'Midwifery', 'Epidemiology', 'Pharmacy', 'Nursing', 'Interdisciplinarity', 'Applied_physics', 'Artificial_intelligence', 'Bioethics', 'Bioinformatics', 'Biomedical_engineering', 'Biostatistics', 'Cognitive_science', 'Complex_systems', 'Computational_linguistics', 'Cultural_studies', 'Cybernetics', 'Environmental_science', 'Environmental_social_science', 'Environmental_studies', 'Ethnic_studies', 'Evolutionary_psychology', 'Forensic_science', 'Forestry', 'Library_science', 'Mathematical_and_theoretical_biology', 'Mathematical_physics', 'Military_science', 'Network_science', 'Neural_engineering', 'Neuroscience', 'Science_studies', 'Scientific_modelling', 'Semiotics', 'Sociobiology', 'Statistics', 'Systems_science', 'Urban_planning', 'Web_science', 'Philosophy_of_science', 'History_of_science', 'Basic_research', 'Citizen_science', 'Fringe_science', 'Protoscience', 'Pseudoscience', 'Academic_freedom', 'Science_policy', 'Funding_of_science', 'Scientific_method', 'Sociology_of_scientific_knowledge', 'Technoscience']
#urls = urls[:5]


from pprint import pprint
data = buildCorpus(urls)

import json
with open('pages.json','w') as outFile:
    json.dump(data,outFile,indent=4)





'''
</ul>
</td>
</tr>
<tr>
<td style="text-align:right;font-size:115%">
<div class="plainlinks hlist navbar mini">
<ul>
<li class="nv-view"><a href="/wiki/Template:Economics_sidebar" title="Template:Economics sidebar"><abbr title="View this template">v</abbr></a></li>
<li class="nv-talk"><a href="/wiki/Template_talk:Economics_sidebar" title="Template talk:Economics sidebar"><abbr title="Discuss this template">t</abbr></a></li>
<li class="nv-edit"><a class="external text" href="//en.wikipedia.org/w/index.php?title=Template:Economics_sidebar&amp;action=edit"><abbr title="Edit this template">e</abbr></a></li>
</ul>
</div>
</td>
</tr>
</table>
<p>




                <div id="siteSub" class="noprint">From Wikipedia, the free encyclopedia</div>               <div id="contentSub"></div>
                                <div id="jump-to-nav" class="mw-jump">
                    Jump to:                    <a href="#mw-head">navigation</a>,                  <a href="#p-search">search</a>
                </div>
                <div id="mw-content-text" lang="en" dir="ltr" class="mw-content-ltr"><div class="mw-parser-output"><div role="note" class="hatnote navigation-not-searchable">This article is about an area of scientific study. For other uses, see <a href="/wiki/Mechanic_(disambiguation)" class="mw-disambig" title="Mechanic (disambiguation)">Mechanic (disambiguation)</a>.</div>
<p






ransactions_2016_12312.png/440px-Silsesquioxane_3D_interpenetrated_network_Dalton_Transactions_2016_12312.png 2x" data-file-width="1675" data-file-height="1384" /></a>
<div class="thumbcaption">
<div class="magnify"><a href="/wiki/File:Silsesquioxane_3D_interpenetrated_network_Dalton_Transactions_2016_12312.png" class="internal" title="Enlarge"></a></div>
3D interpenetrated network in the crystal structure of silsesquioxane.<sup id="cite_ref-7" class="reference"><a href="#cite_note-7">[7]</a></sup></div>
</div>
</div>
<p>


'''












































'''


</p>
<p></p>
<div id="toc" class="toc">
<div class="toctitle">
<h2>Contents</h2>
</div>
<ul>
<li class="toclevel-1 tocsection-1"><a href="#History"><span class="tocnumber">1</span> <span class="toctext">History</span></a>
<ul>
<li class="toclevel-2 tocsection-2"><a href="#Prize-winning_achievements"><span class="tocnumber">1.1</span> <span class="toctext">Prize-winning achievements</span></a></li>
</ul>
</li>
<li class="toclevel-1 tocsection-3"><a href="#Game_types"><span class="tocnumber">2</span> <span class="toctext">Game types</span></a>
<ul>




</p>
<p></p>
<div id="toc" class="toc">
<div class="toctitle">
<h2>Contents</h2>
</div>
<ul>
<li class="toclevel-1 tocsection-1"><a href="#Classical_versus_quantum"><span class="tocnumber">1</span> <span class="toctext">Classical versus quantum</span></a></li>
<li class="toclevel-1 tocsection-2"><a href="#Relativistic_versus_Newtonian"><span class="tocnumber">2</span> <span class="toctext">Relativistic versus Newtonian</span></a></li>
<li class="toclevel-1 tocsection-3"><a href="#General_relativistic_versus_quantum"><span class="tocnumber">3</span> <span class="toctext">General relativistic versus quantum</span></a></li>
<li class="toclevel-1 tocsection-4"><a href="#History"><span class="tocnumber">4</span> <span class="toctext">History</span></a>
<ul>










</p>
<p></p>
<div id="toc" class="toc">
<div class="toctitle">
<h2>Contents</h2>
</div>
<ul>
<li class="toclevel-1 tocsection-1"><a href="#History"><span class="tocnumber">1</span> <span class="toctext">History</span></a></li>
<li class="toclevel-1 tocsection-2"><a href="#Control"><span class="tocnumber">2</span> <span class="toctext">Control</span></a>
<ul>
<li class="toclevel-2 tocsection-3"><a href="#Thermodynamics"><span class="tocnumber">2.1</span> <span class="toctext">Thermodynamics</span></a></li>
<li class="toclevel-2 tocsection-4"><a href="#Environment"><span class="tocnumber">2.2</span> <span class="toctext">Environment</span></a></li>
</ul>
</li>








'''
