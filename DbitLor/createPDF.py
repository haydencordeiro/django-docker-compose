# from urllib.parse import urlencode, quote_plus
import requests


URL = "https://script.google.com/macros/s/AKfycbzm8_19fqeC4sWJEdHSFteRfhGsGFYqff6TDflPPNTRn0iKpff6LlVe/exec"

f = {'invoice_id': '1'}
f['textC'] = '''Theme: The focal point,
from content’s perspective, in a LOR for MS should be the achievements and capabilities of the students. Their interests, skills, emotional traits, etc should form the main theme of the recommendation letter.
Style: Recommendation letters should be written in simple language that could be easily understood by the admissions committee. Provide substantial proof of qualities discussed in the Letter of Recommendation for MS in Canada, Australia, USA, etc by stating examples. Overuse of adjectives or long descriptions should be avoided. Letter of Recommendation must be crisp and concise written in clear and lucid language.
Experience: Any experience or achievements relevant to the field should be discussed in the LOR such as internships, research projects, participation in workshops & seminars, club memberships, etc.
Soft Skills: Applicant’s skills like the ability to communicate effectively, interpersonal skills, teamwork, flexibility, analytical and creative thinking, problem-solving abilities, etc. should also be accentuated in LOR for MS.
Tone: Although the purpose of a recommendation letter is to put the spotlight on all the good qualities of the study abroad aspirants, it shouldn’t be exaggerated or based on prejudices. Perception of recommender should reflect the fair judgment and assessment based on real-time observation.'''
r = requests.get(url=URL, params=f)
data = r.text


print(data)
