# IR-Based Factoid Question Answering with BERT
> University of Science - VNUHCM  
> Natural Language Processing and Application - 19CNTT1

**A group project for Natural Language Processing and Application course**  
- Reference: [Speech and Language Processing. Daniel Jurafsky & James H. Martin. Copyright © 2019](https://web.stanford.edu/~jurafsky/slp3/old_oct19/25.pdf)
- Based-on: [Vietnamese IR-Based QA Model - mailong25](https://github.com/mailong25/vietnamese-question-answering)
- IR-Based Factoid question answering system, currently supports questions about person, location, organization.
- Ranking Passages based on features:
  - number of words
  - number of named entities
  - number of keywords
  - length of longest exact sequence of question keywords
  - rank of own document
  - ngram overlap question

# System Architecture
- IR-Based Question Answering
- Use Google Custom Search API for Question Processing phase
- Neural Answer Extraction (BERT)

![alt text]("Image Placeholder")
