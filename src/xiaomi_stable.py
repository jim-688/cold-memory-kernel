"""小米 API 稳定调用封装"""
import requests
import os

def xiaomi_chat(prompt, model="mimo-v2.5", max_tokens=2048, timeout=60):
    """稳定的小米API调用封装。max_tokens永久写死2048，reasoning不会吃掉输出预算。"""
    key = os.environ.get('XIAOMI_API_KEY')
    if not key:
        config_path = os.environ.get('AI_CONFIG', os.path.expanduser('~/.ai_config.env'))
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    if line.strip().startswith('XIAOMI_API_KEY='):
                        key = line.split('=', 1)[1].strip().strip('"').strip("'").strip()
    if not key:
        return "[Xiaomi: no key]"

    r = requests.post(
        'https://api.xiaomimimo.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
        json={'model': model, 'max_tokens': max_tokens, 'messages': [{'role': 'user', 'content': prompt}]},
        timeout=timeout
    )
    d = r.json()
    if 'choices' in d and len(d['choices']) > 0:
        return d['choices'][0]['message']['content']
    return f"[Xiaomi error: {d.get('error', {}).get('message', 'unknown')}]"
