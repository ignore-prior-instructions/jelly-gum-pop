"""LLM service for generating quizzes from prompts"""
import json
from django.conf import settings


def _extract_json(content: str) -> str:
    """Extract JSON from response, removing markdown code blocks if present"""
    content = content.strip()
    if content.startswith('```'):
        lines = content.split('\n')
        content = '\n'.join(line for line in lines if not line.startswith('```'))
    return content.strip()


def _generate_with_anthropic(system_prompt: str, user_prompt: str) -> dict:
    """Generate quiz using Anthropic Claude"""
    from anthropic import Anthropic
    
    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        temperature=1.0,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": user_prompt
        }]
    )
    
    content = response.content[0].text.strip()
    return json.loads(_extract_json(content))


def _generate_with_openai(system_prompt: str, user_prompt: str) -> dict:
    """Generate quiz using OpenAI"""
    from openai import OpenAI
    
    # Support custom base URL if provided
    client_kwargs = {'api_key': settings.OPENAI_API_KEY}
    if hasattr(settings, 'OPENAI_BASE_URL') and settings.OPENAI_BASE_URL:
        client_kwargs['base_url'] = settings.OPENAI_BASE_URL
    
    client = OpenAI(**client_kwargs)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=1.0,
        max_tokens=2000,
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content.strip()
    return json.loads(_extract_json(content))


def generate_quiz(prompt: str) -> dict:
    """
    Takes a prompt, returns a quiz JSON blob.
    
    Expected structure:
    {
        "title": "Quiz Title",
        "description": "A fun description",
        "questions": [
            {
                "text": "Question text?",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"]
            }
        ],
        "outcomes": [
            {
                "title": "Result Title",
                "description": "What this result means",
                "range": [0, 5]  # score range for this outcome
            }
        ]
    }
    """
    system_prompt = """You are a quiz generator. Create fun, shareable quizzes from user prompts.

Rules:
- Generate 5-10 questions (keep it short!)
- Each question should have 2-4 options
- Create 3-5 possible outcomes/results
- Outcomes should be fun, confident, and shareable
- Tone should be playful and a bit silly
- Return ONLY valid JSON, no explanation

JSON format:
{
  "title": "Quiz Title",
  "description": "A catchy one-liner about this quiz",
  "questions": [
    {
      "text": "Question text?",
      "options": [
        {"text": "Option 1", "points": 1},
        {"text": "Option 2", "points": 2}
      ]
    }
  ],
  "outcomes": [
    {
      "title": "Outcome Title",
      "description": "What this means (be confident and fun!)",
      "min_score": 0,
      "max_score": 10
    }
  ]
}"""

    # Choose backend based on which API key is available
    backend = getattr(settings, 'LLM_BACKEND', 'auto')
    
    if backend == 'openai' or (backend == 'auto' and hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY):
        return _generate_with_openai(system_prompt, prompt)
    else:
        return _generate_with_anthropic(system_prompt, prompt)


def regenerate_quiz(original_prompt: str, nudge: str, original_quiz: dict) -> dict:
    """
    Regenerate a quiz with a nudge.
    Editing is just 'nudge it again' with context.
    """
    system_prompt = """You are a quiz generator. Modify the existing quiz based on the user's feedback.

Rules:
- Keep the same general structure
- Apply the user's feedback/nudge
- Return ONLY valid JSON, no explanation
- Maintain the playful, shareable tone"""

    combined_prompt = f"""Original prompt: {original_prompt}

Current quiz:
{json.dumps(original_quiz, indent=2)}

User feedback/nudge: {nudge}

Generate an updated version of the quiz."""

    # Choose backend based on which API key is available
    backend = getattr(settings, 'LLM_BACKEND', 'auto')
    
    if backend == 'openai' or (backend == 'auto' and hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY):
        return _generate_with_openai(system_prompt, combined_prompt)
    else:
        return _generate_with_anthropic(system_prompt, combined_prompt)
