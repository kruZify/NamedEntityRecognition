import spacy
import os
from spacy import displacy
class model_2:
    def runner(self):
        nlp = spacy.load("trained/model-last/")
        with open("output.txt", "r", encoding='utf-8') as f:
            text = f.read()

        doc = nlp(text)

        html = displacy.render(doc, style="ent")
        i = 0
        vals = {}
        for ent in doc.ents:
            vals[i] = {ent.text: ent.label_}
            i += 1

        d = os.getcwd()
        d1 = os.path.join(d, "templates")
        l = os.path.join(d1, 'datavis.html')
        with open(l, "w", encoding='utf-8') as f:
            f.write(html)
        f.close()
