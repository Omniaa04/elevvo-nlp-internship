# Task 4: Named Entity Recognition (NER) from News Articles

My solution for Task 4 of the Elevvo NLP internship.

The goal is to find people (PER), organizations (ORG), locations (LOC) and other names (MISC) in news text. I used the CoNLL-2003 dataset, loaded from Hugging Face (`lhoestq/conll2003`): 14,041 training, 3,250 validation and 3,453 test sentences.

## What I did

1. Converted the BIO tags (`B-PER`, `I-PER`, `O`, ...) into entity spans, and explored the tag counts with Pandas.
2. **Rule-based NER:** built a dictionary of names from the training set (every entity seen at least twice: about 1,177 PER, 1,075 ORG, 603 LOC and 366 MISC names) and matched it with spaCy's `PhraseMatcher`. I added two hand-written patterns: a title like "Mr." or "President" followed by a capitalized name is a person, and capitalized words followed by a word like "Inc.", "Bank" or "University" are an organization.
3. **Model-based NER:** ran two pre-trained spaCy models, `en_core_web_sm` and `en_core_web_md`.
4. Mapped the spaCy labels to the CoNLL labels (for example `PERSON` to `PER`, and `GPE` to `LOC`), because the models were trained on a different dataset with different label names.
5. Evaluated all three systems with exact-match precision, recall and F1: an entity is correct only if its words and its type are both right.
6. Showed the entities with displaCy and saved the result as `ner_displacy_spacy_md.html` (bonus).
7. Compared the two spaCy models (bonus).

## Results

Evaluated on the first 3,000 test sentences.

| System | Precision | Recall | F1 |
|---|---|---|---|
| Rule-based | 0.829 | 0.466 | 0.596 |
| spaCy sm | 0.672 | 0.574 | 0.619 |
| spaCy md | 0.680 | 0.620 | 0.648 |

F1 per entity type:

| Type | Rule-based | spaCy sm | spaCy md |
|---|---|---|---|
| PER | 0.195 | 0.654 | 0.707 |
| ORG | 0.577 | 0.389 | 0.409 |
| LOC | 0.811 | 0.769 | 0.773 |
| MISC | 0.701 | 0.618 | 0.646 |

## Things I noticed

- `md` is better than `sm` (0.648 compared with 0.619), mostly for person names. Its word vectors help it with names it has not seen before.
- The rule-based system is very precise but misses a lot. It can only find names that are in its dictionary, so it is bad at person names (F1 0.195), because there are too many people to list.
- The rule-based system is good on ORG, LOC and MISC. This is partly because its dictionary comes from the same dataset as the test set, which gives it an advantage over the spaCy models.
- ORG is the hardest type for the spaCy models (F1 about 0.4). The models were trained on a different corpus, and they label things like sports teams differently from CoNLL, so my label mapping can only approximate it.
- CoNLL headlines are written in capital letters (for example `SOCCER - JAPAN GET LUCKY WIN`). The spaCy models depend on capitalization, so words like "SURPRISE" were wrongly tagged as locations.

## Limitations and ideas

- The dictionary only knows names from the training set. A bigger dictionary or fuzzy matching would raise recall.
- Fine-tuning a spaCy model directly on CoNLL-2003 would remove the label mismatch.
- I could add the transformer model `en_core_web_trf` as a third comparison.

## How to run

```
pip install spacy pandas matplotlib datasets jupyter
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
```

Then run all cells. The dataset is downloaded automatically from Hugging Face.

Tools: Python, spaCy, Pandas, Matplotlib
