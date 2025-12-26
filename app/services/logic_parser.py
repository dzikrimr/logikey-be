import re

class LogicParser:
    @staticmethod
    def parse_response(raw_text: str) -> dict:
        # Mencari label di antara asteris 
        label_match = re.search(r"\*\*(.*?)\*\*", raw_text)
        label = label_match.group(1) if label_match else "Unknown"
        
        # Parsing Penjelasan
        explanation = "Analisis pola argumen selesai."
        if "Penjelasan:" in raw_text:
            explanation = raw_text.split("Penjelasan:")[1].split("Lawan:")[0].strip()
        
        # Parsing Counter-arguments
        counter_args = []
        if "Lawan:" in raw_text:
            counter_section = raw_text.split("Lawan:")[1].strip()
            items = re.findall(r"(?:^|\n)(?:-|\d\.)\s*(.+)", counter_section)
            counter_args = [item.strip() for item in items if item.strip()]

        return {
            "label": label,
            "explanation": explanation,
            "counter_arguments": counter_args[:3],
            "is_fallacy": label.lower() not in ["tidak ada", "unknown", "valid", "none"]
        }

logic_parser = LogicParser()