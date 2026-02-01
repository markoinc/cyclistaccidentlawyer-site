import requests
import json
import sys
import time

API_KEY = "AIzaSyCqkgVGAm6Ki8jN4y42JXxe7Cy5EChGyHk"

def get_video_sop(video_url, title, creator):
    """Get detailed SOP-style content from Gemini about a YouTube video."""
    
    prompt = f"""Please provide an extremely detailed summary of this YouTube video that can serve as a Standard Operating Procedure (SOP): {video_url}

Video Title: {title}
Creator: {creator}

Please structure your response as:

1. VIDEO OVERVIEW
- Main topic and purpose
- Who this tutorial is for
- Expected outcomes

2. STEP-BY-STEP PROCESS
For each major step, provide:
- Step number and title
- Detailed instructions
- Key settings or configurations mentioned
- Tips or warnings shared
- Expected result

3. KEY CONCEPTS EXPLAINED
- Important terms/concepts defined
- Frameworks or models discussed
- Best practices mentioned

4. TOOLS & RESOURCES MENTIONED
- Software/platforms referenced
- Templates or resources shared
- Links or recommendations

5. COMMON MISTAKES TO AVOID
- Pitfalls the creator warns about
- Troubleshooting tips

6. ACTION ITEMS / CHECKLIST
- Concise list of all actionable steps

Be as detailed as possible - someone should be able to follow this as an SOP without watching the video."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 8000,
            "temperature": 0.3
        }
    }
    
    response = requests.post(url, json=payload, timeout=120)
    data = response.json()
    
    try:
        return data['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        return f"Error: {json.dumps(data, indent=2)}"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python get_video_content.py <video_url> <title> <creator>")
        sys.exit(1)
    
    video_url = sys.argv[1]
    title = sys.argv[2]
    creator = sys.argv[3]
    
    result = get_video_sop(video_url, title, creator)
    print(result)
