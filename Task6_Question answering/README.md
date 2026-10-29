# Task 6: Question Answering with Transformers

My solution for Task 6 of the Elevvo NLP internship.

Given a passage and a question, the model finds the part of the passage that answers the question. I used SQuAD v1.1, loaded from Hugging Face (`rajpurkar/squad`): 87,599 training questions and 10,570 validation questions.

## What I did

1. Explored the data: passage length, question length, answer length, and the most common first words of questions ("what", "who", "when", ...).
2. Looked at how a transformer reads the input: the question and the passage are joined into one sequence, and the tokenizer keeps the character position of every token, so a predicted token range can be turned back into text.
3. Wrote the answer extraction myself. For every question, the model gives a start score and an end score for each token. I take the best 20 start and end positions, drop impossible pairs (end before start, or an answer longer than 30 tokens), and pick the best pair. Long passages are split into overlapping windows (384 tokens, with an overlap of 128).
4. Wrote the metrics myself: Exact Match (EM) and F1, with the same text normalization as the official SQuAD script (lowercase, remove punctuation and the words a/an/the). I checked the functions with small examples before using them.
5. Evaluated on **1,000 random validation questions** (not all 10,570), on a CPU.
6. For the bonus, I compared four pre-trained models fine-tuned for question answering.

## Results

| Model | EM | F1 | Parameters (M) | Seconds / question |
|---|---|---|---|---|
| DistilBERT | 78.4 | 86.42 | 65.2 | 0.684 |
| BERT | 79.9 | 87.18 | 108.9 | 1.322 |
| **RoBERTa** | **81.2** | **88.65** | 124.1 | 1.313 |
| ALBERT | 42.7 | 54.14 | 11.1 | 1.677 |

RoBERTa was the best. It is 2.2 F1 points above DistilBERT, but it is almost twice as big and about twice as slow, so DistilBERT is a good choice when speed matters.

The ALBERT checkpoint (`twmkn9/albert-base-v2-squad2`) was fine-tuned on SQuAD v2.0, not v1.1, so its low score does not mean that ALBERT is a weak model. It is not a fair comparison.

F1 is always higher than EM because many answers are partly correct (for example, the span is a few words longer or shorter than the gold answer) and F1 gives partial credit.

## Error analysis

For RoBERTa: 81.2% of the answers were an exact match, 12.7% were partly correct, and 6.1% were completely wrong. Only 17 of the 1,000 questions were completely wrong in all four models.

By question type, "when" questions were the easiest (EM 94.1%) and "what" questions were harder (EM 78.4%), probably because "what" can ask for many different kinds of answers.

## Try it on my own text

At the end of the notebook I ask RoBERTa three questions about a short passage on the Nile. It answered "6,650 km long" (how long), "Khartoum" (where the two Niles meet) and "Mediterranean Sea" (which sea), with confidence 0.24, 0.74 and 0.58.

## Limitations

- Only 1,000 questions were evaluated, so the numbers can change by a point or two with another sample.
- I did not fine-tune a model myself. I used models that were already fine-tuned for question answering.
- I did not build a command-line or Streamlit interface.

## How to run

```
pip install torch transformers datasets pandas matplotlib jupyter
```

Then run all cells. The dataset and the models are downloaded automatically from Hugging Face (the first run takes a few minutes).

Tools: Python, Hugging Face Transformers, PyTorch, Pandas, Matplotlib
