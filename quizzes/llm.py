"""LLM service for generating quizzes from prompts"""
import json
from django.conf import settings
from anthropic import Anthropic


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
    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
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

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        temperature=1.0,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    # Extract JSON from response
    content = response.content[0].text.strip()
    
    # Try to find JSON in the response (in case Claude adds explanation)
    if content.startswith('```'):
        # Remove markdown code blocks
        lines = content.split('\n')
        content = '\n'.join(line for line in lines if not line.startswith('```'))
    
    return json.loads(content)


def regenerate_quiz(original_prompt: str, nudge: str, original_quiz: dict) -> dict:
    """
    Regenerate a quiz with a nudge.
    Editing is just 'nudge it again' with context.
    """
    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
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

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        temperature=1.0,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": combined_prompt
        }]
    )
    
    content = response.content[0].text.strip()
    
    if content.startswith('```'):
        lines = content.split('\n')
        content = '\n'.join(line for line in lines if not line.startswith('```'))
    
    return json.loads(content)
