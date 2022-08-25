import spacy
import json
import os
from spacy.tokens import DocBin
from spacy.cli.train import train
class Sama:
    def SamaModel(self):
        nlp = spacy.load("en_core_web_lg")
        db = DocBin() # create a DocBin object

        with open("updateTrainer.json", "r", encoding="utf-8") as json_file:
            data=json.loads(json_file.read())
            for text in data:
                # json_object = json.loads(str(data))
                print(text)
                doc = nlp.make_doc(text["text"])
                ents = []
                for start, end, label in text["label"]:  # add character indexes
                    span = doc.char_span(start, end, label=label, alignment_mode="strict")
                    if span is None:
                        print("Skipping entity")
                    else:
                        ents.append(span)
                doc.ents = ents  # label the text with the ents
                db.add(doc)

        os.chdir(r'D:\API\fastAPI\NER')
        db.to_disk("./train.spacy") # save the docbin object



        train("./config.cfg", "./trained", overrides={"paths.train": "./train.spacy", "paths.dev": "./train.spacy"})
