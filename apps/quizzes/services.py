# apps/quizzes/services.py
import os
import json
import openai
from django.core.cache import cache
from apps.core.models import Topic
from apps.quizzes.models import QuestionBank
from django.conf import settings

openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = """
You are an expert educator. Generate ONE high-quality multiple-choice question.

Topic: {topic}
Difficulty: {difficulty}
Language: English only.

Return ONLY valid JSON in this exact format (no markdown, no extra text):

{{
  "question": "Your question here?",
  "options": ["A) Option one", "B) Option two", "C) Option three", "D) Option four"],
  "correct": "B) Option two",
  "explanation": "Brief explanation why this is correct."
}}
"""

def generate_question(topic_id: int, difficulty: str):
    cache_key = f"ai_q_{topic_id}_{difficulty}_{hash(str(topic_id))}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        topic = Topic.objects.get(id=topic_id)
        prompt = PROMPT_TEMPLATE.format(topic=topic.name, difficulty=difficulty.title())

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600
        )

        raw = response.choices[0].message.content.strip()
        # Clean up code blocks
        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "", 1).strip()

        data = json.loads(raw)

        question = QuestionBank.objects.create(
            topic=topic,
            prompt=data["question"],
            choices={"options": data["options"]},
            correct_answer=data["correct"],
            explanation=data["explanation"],
            difficulty=difficulty,
            generated_by_ai=True,
            confidence_score=0.9,  # Simple for now
            created_by=request.user if 'request' in globals() else None
        )

        cache.set(cache_key, question, timeout=60*60*24)  # 24 hours
        return question

    except Exception as e:
        print("AI Generation Failed:", e)
        return None