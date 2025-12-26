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
            load_in_8bit=True,
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
                "Anda adalah ahli logika. Analisis kalimat yang diberikan dengan struktur WAJIB berikut:\n"
                "1. Nama Fallacy: Tulis di antara bintang dua (contoh: **Ad Hominem**).\n"
                "2. Penjelasan: Berikan penjelasan teknis mengapa itu salah. Gunakan minimal 3 kalimat.\n"
                "3. Lawan: Berikan 3 sanggahan logis. WAJIB diawali dengan kata 'Lawan:' dan gunakan nomor (1., 2., 3.).\n"
                "PENTING: Jangan akhiri jawaban sebelum menuliskan bagian 'Lawan:' secara lengkap."
            )
        
        prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{instruction}\n\nKalimat: {text}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=512,
                temperature=0.1,   
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id 
            )
            
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = decoded.split("assistant")[-1].strip()
        return response

# Inisialisasi Singleton
ai_logic_service = AIService()