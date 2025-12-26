import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel 
from app.core.config import settings

class AIService:
    def __init__(self):
        base_model_id = "meta-llama/Meta-Llama-3-8B-Instruct" 
        self.adapter_id = settings.MODEL_PATH 
        hf_token = os.getenv("HF_TOKEN")

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )

        print(f"⏳ Mendownload/Memuat Base Model: {base_model_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_id, token=hf_token)
        self.tokenizer.padding_side = "left"
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            quantization_config=bnb_config,
            device_map="auto", 
            token=hf_token
        )

        print(f"⏳ Menempelkan Adapter Logiclyst dari HF: {self.adapter_id}...")
        self.model = PeftModel.from_pretrained(base_model, self.adapter_id, token=hf_token)
        
    async def analyze_logic(self, text: str):
        instruction = (
            "Tugas: Analisis sesat logika secara detail. "
            "Aturan Wajib: "
            "1. Nama Fallacy: Tulis di antara bintang dua, contoh: **Ad Hominem**. "
            "2. Penjelasan: Berikan penjelasan detail mengapa kalimat tersebut salah secara logika. Jelaskan mekanisme sesat logikanya dan dampaknya terhadap argumen. "
            "3. Lawan: Berikan minimal 3 poin sanggahan menggunakan nomor (1., 2., 3.). Setiap poin harus berupa argumen tandingan yang kuat dan edukatif untuk mengembalikan diskusi ke jalur yang benar."
        )
        
        prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{instruction}\n\nKalimat: {text}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=512,
                temperature=0.2,   
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id 
            )
            
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = decoded.split("assistant")[-1].strip()
        return response

# Inisialisasi Singleton
ai_logic_service = AIService()