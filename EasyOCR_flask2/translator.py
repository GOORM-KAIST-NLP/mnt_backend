# from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class Translator:
    '''
        Install Requirements -
        pip install pickle5 transformers==4.12.2 sentencepiece
        MBart Documentation
        https://huggingface.co/transformers/model_doc/mbart.html
        Get the supported lang codes
        https://huggingface.co/facebook/mbart-large-50-one-to-many-mmt
        Class - Translator
        Initializes MBart Seq2Seq Model and Tokenizer
        Helper func to translate input language to desired target language
        Supported Languages: English, Gujarati, Hindi, Bengali, Malayalam, Marathi, Tamil, Telugu

    '''

    def __init__(self):

#        self.model = M2M100ForConditionalGeneration.from_pretrained('inhee/m2m100_418M-finetuned-ko-to-en4')
#        self.tokenizer = M2M100Tokenizer.from_pretrained('inhee/m2m100_418M-finetuned-ko-to-en4')
        self.model = AutoModelForSeq2SeqLM.from_pretrained('inhee/opus-mt-ko-en-finetuned-ko-to-en')
        self.tokenizer = AutoTokenizer.from_pretrained('inhee/opus-mt-ko-en-finetuned-ko-to-en')
#        self.supported_langs = ['ko', 'en']
        self.supported_langs = ['kor', 'eng']

    def translate(self, input_text, src_lang, tgt_lang):

        if src_lang not in self.supported_langs:
            raise RuntimeError('Unsupported source language.')
        if tgt_lang not in self.supported_langs:
            raise RuntimeError('Unsupported target language.')

        self.tokenizer.src_lang = src_lang
        encoded_text = self.tokenizer(input_text, return_tensors='pt')
        generated_tokens = self.model.generate(**encoded_text)
                                            #  forced_bos_token_id=self.tokenizer.lang_code_to_id[tgt_lang])
        output_text_arr = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

        if len(output_text_arr) > 0:
            return output_text_arr[0]
        else:
            raise RuntimeError('Failed to generate output. Output Text Array is empty.')