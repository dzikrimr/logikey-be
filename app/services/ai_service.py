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

        print(f"⏳ Menambahkan Adapter Logiclyst dari HF: {self.adapter_id}...")
        self.model = PeftModel.from_pretrained(base_model, self.adapter_id, token=hf_token)
        
    async def analyze_logic(self, text: str, sensitivity: float = 0.5):
        """
        Analisis teks dengan parameter sensitivity.
        Sensitivity 1.0 (Critical) -> Temperature Rendah (0.1) -> Kaku/Akurat
        Sensitivity 0.1 (Relaxed) -> Temperature Tinggi (1.0) -> Luwes/Kreatif
        """
        # Rumus konversi sensitivity ke temperature
        computed_temp = max(0.1, 1.1 - sensitivity)
        instruction = (
            "Anda adalah ahli logika objektif. Tugas Anda adalah menguji apakah sebuah kalimat mengandung kesesatan logika (fallacy) atau merupakan argumen yang valid.\n"
            "ATURAN OUTPUT:\n"
            "1. Nama Fallacy: Jika ditemukan, tulis di antara bintang dua (contoh: **Nama Jenis Fallacy**). "
            "JIKA ARGUMEN VALID, WAJIB tulis **None**.\n"
            "2. Penjelasan: Berikan analisis teknis. Jika valid, jelaskan mengapa penalaran tersebut benar secara logika.\n"
            "3. Lawan: Berikan 3 sanggahan logis jika ada fallacy. "
            "JIKA ARGUMEN VALID, berikan 3 poin yang mendukung atau memperkuat argumen tersebut.\n"
            "WAJIB diawali dengan kata 'Lawan:' dan gunakan nomor (1., 2., 3.).\n"
            "PENTING: Jangan memaksakan adanya fallacy jika argumen memang logis dan didukung bukti/premis yang kuat."
        )
        
        prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{instruction}\n\nKalimat: {text}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=512,
                temperature=computed_temp, 
                top_p=0.9,
                repetition_penalty=1.1,
                do_sample=True if computed_temp > 0.1 else False,
                pad_token_id=self.tokenizer.eos_token_id 
            )
            
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = decoded.split("assistant")[-1].strip()
        return response

# Inisialisasi Singleton
ai_logic_service = AIService()