import spacy
class resumeP:
    def resumer(self):
        nlp = spacy.load("resume_model/model-best/")
        with open("output2.txt", "r", encoding='utf-8') as f:
            text = f.read()

        doc = nlp(text)

        i = 0
        vals = {}
        for ent in doc.ents:
            vals[i] = {ent.text: ent.label_}
            i += 1
        return vals
