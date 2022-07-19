import re
import sentencepiece
import transformers
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 'cyt5-small-new'
def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

def t5_summarize(model_name, text):
    tokenizer, model = load_model(model_name)
    WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))
    input_ids = tokenizer([WHITESPACE_HANDLER(text)],
    return_tensors="pt", padding="max_length", truncation=True,
    max_length=512
    )["input_ids"]
    
    output_ids = model.generate(input_ids=input_ids, max_length=150,
        no_repeat_ngram_size=3, num_beams=2)[0]

    summary = tokenizer.decode(output_ids,skip_special_tokens=True,
        clean_up_tokenization_spaces=False)
    
    summary_sents = re.sub('<.*>', '', summary).split('. ')
    return("\n".join([f"{sent}." for sent in summary_sents if sent[0].isupper() and len(sent)>5]))
