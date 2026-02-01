# The Ultimate Nano Banana Pro Prompt Guide

**Source:** https://invernessdesignstudio.com/the-ultimate-nano-banana-pro-prompt-guide
**Type:** Comprehensive Prompting Guide
**Focus:** Professional prompt engineering for marketing and ads

## What Is Nano Banana Pro

Released in November 2025, Nano Banana Pro is Google DeepMind's latest flagship image-generation model, built on the Gemini 3 Pro Image foundation and engineered for professional, production-grade visuals rather than casual experimentation.

Key capabilities:
- Output up to 4K resolution
- Can ingest up to 14 reference images in a single prompt
- Tuned specifically for accurate, legible text and brand consistency
- Renders crisp, multi-language text inside images reliably

## The Five Part Prompt Structure

### 1. Task
States the job clearly and concisely. 

Example: "Create a brand identity system for a sustainable coffee company" or "Generate a product mockup showing wireless earbuds in use"

### 2. Context
Supplies relevant facts and constraints including target audience, platform specifications, brand guidelines, or technical requirements.

Example: "Target audience is environmentally conscious millennials aged 25 to 40. Primary use will be social media posts in 16:9 format"

### 3. Instructions
Provide the rules and steps the model should follow.

Example: "Use earth tones and organic shapes" or "Include the tagline in readable text at the bottom third of the image"

### 4. Examples
Act as few-shot guides showing the model exactly what you want.

Example: "Match the lighting style from reference image 1 and the colour palette from reference image 2"

### 5. Output Format
Specifies technical requirements like resolution, aspect ratio, and file specifications.

Example: "4K resolution in 16:9 aspect ratio with high contrast for outdoor billboard printing"

## Advanced Prompting Techniques

### Step-Back Prompting
Ask the model to explain its approach before generating.

Example: "Before creating the image, explain how you would approach designing a minimalist tech startup logo that conveys innovation and trustworthiness."

### Chain-of-Thought Prompting
Walk through the layout logic explicitly.

Example: "First, establish the horizon line at the lower third. Then, position the product at the golden ratio intersection. Finally, add environmental elements that complement but do not distract from the main subject."

### Few-Shot Prompting
Upload multiple reference images (up to 14) for style matching.

Example: "Match the typography and colour system from these references while generating three new hero images."

### JSON-Style Structured Prompts
Treat the prompt like a config object with separate fields for subject, layout regions, text blocks, and brand colours.

## Text Rendering Capabilities

Nano Banana Pro's text rendering represents a breakthrough. It can render crisp, legible text in complex layouts across dozens of languages including:
- English, Spanish, French, German, Italian
- Arabic, Hebrew (right-to-left support)
- Chinese, Japanese, Korean
- Czech (with proper diacritics)

### Best Practice for Text
Always quote your exact copy and specify style explicitly:
"Create a retro concert poster with 'SUMMER NIGHTS' in bold condensed sans-serif at the top and 'Every Friday in July' in cursive script below"

## In-Image Localization for Global Campaigns

Teams can upload English ads and generate Spanish, German, Japanese variants with translated text flowing perfectly around existing layouts – preserving photography, colours, and composition while only swapping language layers.

**This collapses weeks of production into hours for global marketing teams.**

## Character Consistency for Brand Identity

Nano Banana Pro supports:
- Up to 14 reference images
- Identity locking for up to 5 distinct human faces
- Consistent character across different poses, outfits, and environments

### Prompt Example for Consistency
"Using the person from reference image 1, keep their facial features exactly the same but change their expression to excited and surprised"

## Multi-Image Composition

Combine up to 14 reference images into cohesive compositions.

Example: "Combine these images into one cinematic 16:9 composition. Use image 1 as the background landscape, place the product from image 2 in the foreground left, and add the model from image 3 on the right, maintaining natural lighting across all elements"

## Search Grounding for Real-World Accuracy

The model integrates with Google Search to verify facts and generate imagery based on real-time data – valuable for:
- Educational materials
- Infographics
- Data visualization

## Creative Controls

### Lighting Control
"harsh directional spotlight from above with cool blue backlighting" or "soft, diffused golden hour lighting from the left"

### Camera Angle
"low angle heroic shot with wide cinematic lens" or "overhead flat lay composition with shallow depth of field"

### Material and Texture
"matte finish with subtle grain" or "polished chrome with high specular highlights"

## Common Pitfalls to Avoid

1. **Under-specification** - Vague prompts produce poor results
2. **Over-reliance on tag soup** - "4k, ultra detailed, professional" works worse than conversational instructions
3. **Ignoring aspect ratio early** - Specify format from the start
4. **Failing to iterate** - Use conversational editing to refine images

## Platform Comparison

| Platform | Free Tier | Resolution | Best For |
|----------|-----------|------------|----------|
| Gemini App | 3 images/day at 1MP | Up to 4K with Pro | Quick generation |
| Google AI Studio | Pay as you go | Up to 4K | Development |
| Vertex AI | Pay as you go | Up to 4K | Production |
| Google Workspace | Varies | Up to 4K | Business |

## API Pricing
- 4K images: $0.24/image
- 1K or 2K images: $0.134/image
- Input images: $0.0011/each

## Key Takeaway

Treat every Nano Banana Pro prompt like a mini creative brief you'd give a senior designer. Explain the project goal, target audience, emotional tone, references, and deliverable specs.
