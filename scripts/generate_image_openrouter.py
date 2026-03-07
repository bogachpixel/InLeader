"""
Генерация изображений через OpenRouter API (google/gemini-3.1-flash-image-preview).
Запуск: python scripts/generate_image_openrouter.py
"""

import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()


def generate_image(prompt: str, output_filename: str = "output.png") -> None:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found in environment.")
        return

    print(f"Sending request to OpenRouter... Prompt: '{prompt}'")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://cursor.sh",
        "X-Title": "InLeader Image Generator",
    }

    payload = {
        "model": "google/gemini-3.1-flash-image-preview",
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image"],
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        data = response.json()

        choices = data.get("choices") or []
        if not choices:
            print("Error: No choices in API response.", data)
            return
        content = choices[0].get("message", {}).get("content")
        if content is None:
            print("Error: No content in message.", choices[0])
            return

        if "base64," in content:
            base64_string = content.split("base64,", 1)[1].strip()
            with open(output_filename, "wb") as img_file:
                img_file.write(base64.b64decode(base64_string))
            print(f"Done! Image saved as {output_filename}")
        else:
            print("Error: No base64 image in response.")
            print("API response:", content[:500])

    except requests.exceptions.RequestException as e:
        print(f"Network/API error: {e}")
        if "response" in locals() and hasattr(e, "response") and e.response is not None:
            print("Response text:", e.response.text[:500])
    except Exception as e:
        import traceback
        print(f"Unknown error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    user_prompt = input("Enter image prompt: ").strip()
    if user_prompt:
        generate_image(user_prompt)
    else:
        print("Prompt cannot be empty.")
