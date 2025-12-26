import re

class LogicParser:
    @staticmethod
    def parse_response(raw_text: str) -> dict:
        # Mencari Label (Nama Fallacy atau status Valid)
        label_match = re.search(r"\*\*(.*?)\*\*", raw_text)
        label = label_match.group(1).strip() if label_match else "Unknown"
        
        # Parsing Penjelasan
        explanation = "Analisis pola argumen selesai."
        if "Penjelasan:" in raw_text:
            explanation_part = re.split(r"Lawan:", raw_text, flags=re.IGNORECASE)
            if len(explanation_part) > 1:
                explanation = explanation_part[0].split("Penjelasan:")[-1].strip()
        
        # Parsing Counter-arguments
        counter_args = []
        if "Lawan:" in raw_text:
            counter_section = raw_text.split("Lawan:")[1].strip()
            pattern = r"\d+\.\s*(.*?)(?=\s*\d+\.\s+|$)"
            items = re.findall(pattern, counter_section, re.DOTALL)
            counter_args = [item.strip() for item in items if len(item.strip()) > 2]

        is_fallacy = label.strip().lower() != "none"

        return {
            "label": label,
            "explanation": explanation,
            "counter_arguments": counter_args[:3],
            "is_fallacy": is_fallacy
        }

logic_parser = LogicParser()