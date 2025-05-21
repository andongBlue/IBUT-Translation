# IBUT: Iterative Bilingual Understanding Translation

## Project Introduction

IBUT (Iterative Bilingual Understanding Translation) is a novel machine translation approach designed to enhance translation quality by generating bilingual contextual understanding through large language models (LLMs). It leverages dual learning in translation tasks to establish linguistic feedback, iteratively optimizing this understanding.

## Methodology

The IBUT approach consists of four main components:

1. **Understanding Generation**:
   - Uses an LLM to generate contextual understanding in both the source and target languages from the input sentence  
   - Contextual understanding includes key concepts, terminology, explanations, and related examples

2. **Alignment Judgment**:
   - Employs the LLM as a Judgment Agent (JA) to evaluate the consistency of bilingual contextual understanding  
   - If inconsistencies are found, generates explicit linguistic feedback highlighting the differences and offering suggestions for improvement

3. **Iterative Refinement**:
   - Refines the previously generated bilingual contextual understanding based on the feedback signals  
   - Repeats the alignment and refinement process within a predefined maximum number of iterations

4. **Understanding-Based Translation**:
   - Inputs the optimized bilingual contextual understanding along with the sentence to be translated  
   - Performs translation directly via the LLM

## Code Structure

- `model.py`: LLM interface class that provides interaction with the large language model  
- `ibut.py`: IBUT implementation class that contains the full translation process  
- `main.py`: Main script demonstrating the IBUT workflow  
- `test_ibut.py`: Test script with additional test cases and evaluation methods

## Usage

### Basic Usage

```python
# Import necessary classes
from model import LLMModel
from ibut import IBUT

# Initialize model and IBUT
model = LLMModel(model_name="gpt-3.5-turbo")
ibut_translator = IBUT(model, max_iterations=3)

# Perform translation
source_sentence = "气候变化是当今人类面临的最严峻挑战之一。"
translation = ibut_translator.translate(source_sentence)

print(f"Source sentence: {source_sentence}")
print(f"Translation result: {translation}")
```

### Run Demo Script

```python
python main.py
```
### Run Test Script

```python
python test_ibut.py
```

Notes
	•	A real LLM API must be configured for practical use
	•	In model.py, modify the generate method according to the actual model used (e.g., OpenAI, Anthropic)
	•	You can control the maximum number of optimization iterations via the max_iterations parameter

