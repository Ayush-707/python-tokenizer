import nltk
import re
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from gingerit.gingerit import GingerIt
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Step 1: Tokenization
def tokenize_text(text):
    return word_tokenize(text)

# Step 2: Spell Checking
def correct_spelling(tokens):
    spell = SpellChecker()
    corrected_tokens = [spell.correction(token) for token in tokens]
    return corrected_tokens

# Step 3: Grammar Correction
def correct_grammar(text):
    parser = GingerIt()
    result = parser.parse(text)
    corrected_text = result['result']
    return corrected_text

# Step 4: Missing or Extra Words
def correct_missing_or_extra_words(text):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    input_ids = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(input_ids, max_length=100, num_return_sequences=1, repetition_penalty=1.0, do_sample=True)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract the number of sentences in the original text
    num_sentences = len(re.findall(r'[.!?]', text))
    
    # Extract the same number of sentences from the generated text
    extracted_sentences = re.findall(r'(.*?[.!?])', generated_text)
        
    # Take the first 'num_sentences' sentences
    extracted_sentences = extracted_sentences[:num_sentences]
    
    # Join the extracted sentences to form the corrected text
    corrected_text = ' '.join(sentence.strip() for sentence in extracted_sentences[:num_sentences])
  
    return corrected_text


while True:
    input_text = input("Enter some text (or 'exit' to quit): ")

    if input_text.lower() == 'exit':
        break

    if not input_text.endswith((".", "?", "!")):
        input_text += "."

    # Step 1: Tokenization
    tokens = tokenize_text(input_text)

    # Step 2: Spell Checking
    corrected_tokens = correct_spelling(tokens)

    # Step 3: Grammar Correction
    corrected_text = ' '.join(corrected_tokens)
    corrected_text = correct_grammar(corrected_text)

    # Step 4: Missing or Extra Words
    corrected_text = correct_missing_or_extra_words(corrected_text)

    print("Original text:", input_text)
    print("Corrected text:", corrected_text)
    print()

print("Exiting the program.")