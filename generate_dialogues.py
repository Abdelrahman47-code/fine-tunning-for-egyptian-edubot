import asyncio 
import json 
import logging 
import random 
import re 
from typing import List 
import httpx 
from pydantic import BaseModel, Field, validator 
 
GEMINI_API_KEY = "AIzaSyCoGJokaYHejLGzw39T477gxFgHYk4YO6o"
OUTPUT_FILE = "egyptian_dialogues_.json" 
TOTAL_DIALOGUES = 250
MODEL_NAME = "gemini-2.5-flash" 
 
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s") 
logger = logging.getLogger(__name__) 
 
subjects = [ 
    "تاريخ", "جغرافيا", "أحياء", "فيزياء", "كيمياء", "رياضيات", 
    "لغة عربية", "لغة إنجليزية", "دراسات اجتماعية", "تربية فنية", "فلسفة" 
] 
 
class Turn(BaseModel): 
    role: str = Field(..., pattern="^(student|teacher)$") 
    text: str 
 
class Dialogue(BaseModel): 
    id: int 
    subject: str 
    dialogue: List[Turn] = Field(..., min_length=14, max_length=22) 
 
    @validator('dialogue') 
    def limit_length(cls, v): 
        # Cut the dialogue if it exceeds 22 turns
        if len(v) > 22: 
            return v[:22]  
        return v 
 
async def call_gemini(prompt: str) -> str: 
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent" 
    headers = { 
        "Content-Type": "application/json", 
        "x-goog-api-key": GEMINI_API_KEY, 
    } 
    payload = { 
        "contents": [{"parts": [{"text": prompt}]}], 
        "generationConfig": { 
            "temperature": 0.85, 
            "maxOutputTokens": 3500, 
            "responseMimeType": "application/json" 
        }, 
        "safetySettings": [ 
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}, 
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}, 
        ] 
    } 
 
    async with httpx.AsyncClient(timeout=90.0) as client: 
        for attempt in range(3): 
            try: 
                r = await client.post(url, headers=headers, json=payload) 
                r.raise_for_status() 
                data = r.json() 
                text = data["candidates"][0]["content"]["parts"][0]["text"] 
                return text 
            except Exception as e: 
                logger.warning(f"Attempt {attempt+1} failed: {e}") 
                await asyncio.sleep(2) 
        raise Exception("Gemini API failed after 3 attempts") 
 
async def generate_one(num: int) -> Dialogue: 
    subject = random.choice(subjects) 
     
    prompt = f""" 
أكتب حوار تعليمي واقعي جدًا بالعامية المصرية القاهرية بين مدرس خصوصي وطالب عام في مادة {subject}. 
- عدد التبادلات بالظبط من 16 إلى 20 فقط (مش أكتر). 
- استخدم عامية مصرية طبيعية جدًا (بص، طب، يا معلم، والله، أصل، عشان كده، ماشي، لا مؤاخذة، فاهم ولا لسه؟، هههه، إلخ). 
- المعلومات صحيحة 100%. 
- الجو ودود ومضحك وواقعي زي الدرس في البيت. 
 
رد بـ JSON فقط بدون أي كلام خارجي ولا markdown: 
{{"id": {num}, "subject": "{subject}", "dialogue": [{{"role": "teacher/student", "text": "..."}}, ...]}}""" 
 
    for attempt in range(8): 
        try: 
            raw = await call_gemini(prompt) 
             
            # Clean markdown or unwanted formatting
            json_match = re.search(r'\{.*\}', raw, re.DOTALL) 
            if not json_match: 
                raise ValueError("No JSON found") 
            clean_json = json_match.group(0) 
             
            data = json.loads(clean_json) 
            dialogue = Dialogue(**data) 
            logger.info(f"Success Dialogue {num} – {subject} ({len(dialogue.dialogue)} turns)") 
            return dialogue 
             
        except Exception as e: 
            logger.warning(f"Attempt {attempt+1}/8 failed for dialogue {num}: {str(e)[:80]}") 
            await asyncio.sleep(1.5 ** attempt) 
     
    # Final fallback if all attempts fail
    logger.error(f"FAILED after 8 attempts → creating dummy dialogue {num}") 
    return Dialogue( 
        id=num, 
        subject=subject, 
        dialogue=[Turn(role="teacher", text="Listen, today’s lesson is very important...")] 
    ) 
 
async def main(): 
    all_dialogues = [] 
     
    logger.info(f"Starting generation of {TOTAL_DIALOGUES} perfect dialogues...") 
     
    for i in range(226, 226 + TOTAL_DIALOGUES): 
        dialogue = await generate_one(i) 
        all_dialogues.append(dialogue.model_dump()) 
         
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f: 
            json.dump(all_dialogues, f, ensure_ascii=False, indent=2) 
         
        logger.info(f"Saved: {i}/{TOTAL_DIALOGUES}") 
        await asyncio.sleep(1.3) 
 
    logger.info(f"\nFinished! {len(all_dialogues)} perfect dialogues saved in {OUTPUT_FILE}") 
 
if __name__ == "__main__": 
    asyncio.run(main())