# Ad Creative Pipeline with Nano Banana - Meta Ads Deployment

**Source:** https://www.rabbitmetrics.com/ad-creative-pipeline-with-nano-banana/
**Type:** Technical Automation Pipeline
**Focus:** AI image composition → Meta Ads deployment

## Overview

Creative production is the bottleneck in Meta ads performance. Testing requires multiple variations, but traditional production means photographers, models, and weeks of turnaround.

This playbook extends the Meta Ads automation system with AI image composition, transforming basic product photos into complete campaign creatives in minutes.

## Pipeline Flow

```
Product Selection → AI Composition → Campaign Generation → Human Review → Meta Deployment
```

The system:
1. Takes product indices from a fashion dataset (or your own images)
2. Generates professional marketing creatives using Gemini's image generation
3. Creates targeted campaign structures
4. Deploys to Meta after human approval

## Technical Integration

This extends the original LangGraph workflow with minimal modifications:

```python
# Original workflow
workflow.set_entry_point("generate")
workflow.add_edge("generate", "review")

# Enhanced workflow - adds one node
workflow.add_node("compose", compose_images)
workflow.set_entry_point("compose")
workflow.add_edge("compose", "generate")
```

When `use_composition: false`, the compose node passes through immediately, preserving original behavior.

## API Credentials Required

```
GOOGLE_AI_API_KEY    # Powers image and campaign generation
META_ADS_TOKEN       # Your Meta access token
META_ADS_ACCOUNT_ID  # Format: act_123456789
META_PAGE_ID         # Your Facebook page ID
```

## Configuration File

Upload the following `campaign_input.yaml` file:

```yaml
product_description: "Summer fashion collection"
budget: 50
target_countries: ["US"]
landing_url: "https://yourstore.com"
use_composition: true    # Enable AI generation
product_indices: [0, 5, 10]  # Select from dataset
```

## Image Composition with Fashion Dataset

The system uses Hugging Face's fashion dataset with 44,000+ products.

**Dataset:** `ashraq/fashion-product-images-small`

### Composition Function:

```python
# Load fashion dataset
data = load_dataset("ashraq/fashion-product-images-small", split="train")
images = data["image"]
df = data.to_pandas()

# Create composition function
def create_composition(client, images_list, indices, prompt, output_name):
    selected_images = [images_list[i] for i in indices]
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=selected_images + [prompt],
    )
    
    # Extract and save generated image
    image_parts = [
        part.inline_data.data
        for part in response.candidates[0].content.parts
        if part.inline_data
    ]
    
    if image_parts:
        image = Image.open(BytesIO(image_parts[0]))
        image.save(output_name)
        return output_name
```

## Example Compositions

Starting with four basic product images from the dataset:
- Index 0: Navy Blue Shirt
- Index 5: Grey T-shirt
- Index 10: Casual Shoes
- Index 12: Sandals

### Creative Styles Generated:

**Hero Shot:** 
- Prompt: "Professional e-commerce product shot on white background"
- Use: Clean, minimalist product presentation for primary campaign visuals

**Lifestyle:**
- Prompt: "Model wearing these items in casual urban setting"
- Use: Contextual product usage for higher engagement on social placements

**Flat Lay:**
- Prompt: "Aesthetic arrangement for Instagram"
- Use: Styled product composition optimized for Instagram feed/stories

### Performance:
- Each composition takes ~5 seconds
- Costs ~$0.01 in API usage

## Key Benefits

1. **Speed:** Minutes instead of weeks for creative production
2. **Scale:** Generate dozens of variations from a few base products
3. **Cost:** ~$0.01 per composition vs traditional photography costs
4. **Consistency:** Automated pipeline ensures consistent quality
5. **Testing:** Rapid A/B testing of creative variations
