import spacy
import os
from spacy import displacy
class Model:
    def runMod(self):
        nlp = spacy.load("en_core_web_lg")
        with open("output.txt", "r", encoding='mbcs') as f:
            text = f.read()

        doc = nlp(text)

        ruler = nlp.add_pipe("entity_ruler", before="ner")
        patterns =[
                        {"label": "INDIA_STD_CODE", "pattern": "+91"},
                        {"label": "PAKISTAN_STD_CODE", "pattern": "+92"},
                        {"label": "PHONE_NUMBER", "pattern": [{"TEXT": {"REGEX": "^\d{10}$"}}]},
                        {"label": "Email", "pattern": [{"TEXT": {"REGEX": "[a-z0-9\.\-+]+@[a-z0-9\.\-+]+\.[a-z]+"}}]},
                        {"label": "LATITUDE", "pattern": [{"TEXT": {"REGEX": "([0-9]\d{1,2})\D?\s?([0-9]\d{1,2})\D\s?([0-9]\d{1,2})\D{2}\s?([NnSs])"}}]},
                        {"label": "LONGITUDE","pattern": [{"TEXT": {"REGEX": "([0-9]\d{1,3})\D?\s?([0-9]\d{1,2})\D\s?([0-9]\d{1,2})\D{2}\s?([EeWw])"}}]}
                        ]
        ruler.add_patterns(patterns)

        doc = nlp(text)
        html = displacy.render(doc, style="ent")
        i=0
        vals={}
        for ent in doc.ents:
            vals[i]={ent.text:ent.label_}
            i+=1

        d = os.getcwd()
        d1 = os.path.join(d, "templates")
        l=os.path.join(d1,'datavis.html')
        with open(l, "w",encoding='utf-8') as f:
            f.write(html)
        f.close()

        return vals

