import re
from typing import Optional
from app.schemas import LanguageEnum
from app.llm_provider import get_provider_pool

def detect_bangla_chars(text: str) -> bool:
    return bool(re.search(r'[\u0980-\u09ff]', text))

def detect_language_ai(text: str, use_fallback: bool = True) -> LanguageEnum:
    pool = get_provider_pool()
    
    if not pool or use_fallback:
        return detect_language_rule_based(text)
    
    try:
        def make_detection_call(client, config):
            response = client.chat.completions.create(
                model=config.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a language detector for a Bangladeshi digital finance platform. "
                            "Detect if the text is: 'en' (English only), 'bn' (Bangla/Bengali script), "
                            "or 'mixed' (Banglish/code-switched/romanized Bangla). "
                            "Respond with ONLY one word: en, bn, or mixed"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Detect language: {text}"
                    }
                ],
                temperature=0.0,
                max_tokens=5
            )
            
            result = response.choices[0].message.content.strip().lower()
            
            if result == "bn":
                return LanguageEnum.bn
            elif result == "mixed":
                return LanguageEnum.mixed
            else:
                return LanguageEnum.en
        
        return pool.call_with_failover(make_detection_call, context="language_detection")
        
    except Exception:
        return detect_language_rule_based(text)

def detect_language_rule_based(text: str) -> LanguageEnum:
    has_bangla_unicode = detect_bangla_chars(text)
    
    banglish_keywords = [
        "ami", "tumi", "pathaise", "pathalam", "korsi", "hoise", 
        "kore", "korechi", "diye", "ferot", "den", "koren", "hoyeche",
        "kintu", "kinto", "amar", "tomar", "apnar", "poisa",
        "kete", "gese", "gelo", "chai", "chilo", "ache"
    ]
    
    text_lower = text.lower()
    words = text_lower.split()
    has_banglish = any(word in banglish_keywords for word in words)
    has_english = bool(re.search(r'[a-zA-Z]', text))
    
    if has_bangla_unicode and has_english:
        return LanguageEnum.mixed
    elif has_bangla_unicode:
        return LanguageEnum.bn
    elif has_banglish:
        return LanguageEnum.mixed
    else:
        return LanguageEnum.en

def detect_language(text: str, method: str = "hybrid") -> LanguageEnum:
    if method == "ai":
        return detect_language_ai(text, use_fallback=False)
    elif method == "rules":
        return detect_language_rule_based(text)
    elif method == "hybrid":
        has_unicode_bangla = detect_bangla_chars(text)
        
        if has_unicode_bangla:
            return detect_language_ai(text, use_fallback=True)
        else:
            return detect_language_rule_based(text)
    else:
        return detect_language_rule_based(text)
