import nltk
from nltk import word_tokenize, pos_tag, ne_chunk

# Downloads
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('maxent_ne_chunker')
nltk.download('words')

sentence = "Apple Inc. is planning to open a new store in Berlin on 15th January 2025. Tim Cook, the CEO of Apple, announced it in a press conference."

tokens = word_tokenize(sentence)
tagged = pos_tag(tokens)
tree = ne_chunk(tagged)

def extract_entities(tree):
    entities = []
    for subtree in tree:
        if hasattr(subtree, 'label'):
            entity = " ".join([token for token, pos in subtree.leaves()])
            entity_type = subtree.label()
            entities.append({
                "text": entity,
                "label": entity_type
            })
    return entities

entities = extract_entities(tree)

for e in entities:
    print(f"{e['text']} --> {e['label']}")