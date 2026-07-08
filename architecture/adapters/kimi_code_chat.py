"""Kimi Code API (Anthropic format) — for sk-kimi- prefixed keys.
Endpoint: https://api.kimi.com/coding/
Format: Anthropic messages (not OpenAI)
"""
import requests, json, os

KIMI_CODE_URL = "https://api.kimi.com/coding/v1/messages"

def kimi_code_chat(prompt, model="kimi-for-coding", max_tokens=2048, timeout=60, thinking="disabled"):
    """Call Kimi Code API with Anthropic format."""
    env = {}
    with open(os.path.expanduser('~/.openclaw/.env'), 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                env[k] = v.strip().strip('"').strip("'")
    
    key = env.get('KIMI_API_KEY')
    if not key:
        return "[Kimi Code: no key]"
    
    payload = {
        'model': model,
        'max_tokens': max_tokens,
        'messages': [{'role': 'user', 'content': prompt}],
    }
    if thinking == "disabled":
        payload['thinking'] = {"type": "disabled"}
    
    r = requests.post(
        KIMI_CODE_URL,
        headers={
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        },
        json=payload,
        timeout=timeout
    )
    d = r.json()
    if 'content' in d:
        texts = [b['text'] for b in d['content'] if b.get('type') == 'text']
        if texts:
            return texts[0]
        # Fallback: return thinking content
        for b in d['content']:
            if b.get('type') == 'thinking':
                return f"[Thinking] {b['thinking']}"
    return f"[Kimi Code error: {d.get('error', {}).get('message', 'unknown')}]"
