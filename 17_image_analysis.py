"""
Demo 19: Image Analysis Agent with Bedrock
Goal: Analyze images using AWS Bedrock Claude with vision

Key Teaching Points:
- Real image analysis with Bedrock
- Claude 3 vision capabilities
- Multimodal AI integration
- Image understanding and OCR
"""

import os
import base64
from pathlib import Path
from strands import Agent, tool
from dotenv import load_dotenv
import json
import boto3

# Load environment variables
load_dotenv()

# Initialize Bedrock client
try:
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
except Exception as e:
    print(f"⚠️  Warning: Could not initialize Bedrock client: {e}")
    bedrock_runtime = None


@tool
def analyze_image_with_claude(image_path: str, question: str = "Describe this image in detail") -> str:
    """
    Analyze an actual image file using Claude 3 Sonnet vision model on Bedrock.

    Args:
        image_path: Path to the image file (jpg, png, gif, webp)
        question: Question to ask about the image
    """
    if not bedrock_runtime:
        return "Error: Bedrock client not initialized. Check AWS credentials."

    try:
        # Check if file exists
        image_file = Path(image_path)
        if not image_file.exists():
            return f"Error: Image file not found at {image_path}"

        # Read and encode image
        with open(image_path, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode("utf-8")

        # Determine media type from file extension
        ext = image_file.suffix.lower()
        media_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        media_type = media_types.get(ext, 'image/jpeg')

        # Prepare the request for Claude 3 Sonnet with vision
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data
                            }
                        },
                        {
                            "type": "text",
                            "text": question
                        }
                    ]
                }
            ]
        }

        # Call Bedrock
        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=json.dumps(body)
        )

        # Parse response
        response_body = json.loads(response['body'].read())
        analysis = response_body['content'][0]['text']

        return f"Image: {image_file.name}\n\n{analysis}"

    except Exception as e:
        return f"""Error analyzing image: {str(e)}

Make sure:
1. AWS credentials are configured (~/.aws/credentials or environment variables)
2. You have access to Claude 3 Sonnet in Bedrock (enable in AWS Console)
3. Image file exists at: {image_path}
4. Image format is supported (jpg, png, gif, webp)
"""


@tool
def create_sample_image(filename: str = "sample.png") -> str:
    """
    Create a simple sample image for testing (requires PIL/Pillow).
    Returns the path to the created image.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont

        # Create a simple test image
        img = Image.new('RGB', (400, 300), color='white')
        draw = ImageDraw.Draw(img)

        # Draw some shapes
        draw.rectangle([50, 50, 200, 150], fill='blue', outline='black', width=2)
        draw.ellipse([220, 80, 350, 180], fill='red', outline='black', width=2)
        draw.text((150, 220), "Test Image", fill='black')

        # Save image
        output_path = Path(filename)
        img.save(output_path)

        return f"Sample image created at: {output_path.absolute()}"

    except ImportError:
        return "Error: PIL/Pillow not installed. Run: uv add pillow"
    except Exception as e:
        return f"Error creating sample image: {str(e)}"


# Image analysis agent
image_agent = Agent(
    tools=[analyze_image_with_claude, create_sample_image],
    system_prompt="""You are an image analysis assistant powered by Claude 3 vision.

When users want to analyze images:
1. Use analyze_image_with_claude with the image path
2. Ask specific questions about the image if needed
3. Provide detailed, accurate descriptions
4. Extract text, identify objects, describe scenes
5. If no image is provided, you can create_sample_image for testing

Capabilities:
- Scene understanding and description
- Object detection and identification
- Text extraction (OCR)
- Activity and emotion recognition
- Color and composition analysis
- Content description

Be specific and thorough in your analysis.
"""
)


def main():
    """Run the image analysis demo."""
    print("=" * 70)
    print("🖼️  Image Analysis with AWS Bedrock Claude")
    print("=" * 70)
    print()

    # Check if we have sample images in the directory
    sample_images = list(Path('.').glob('*.{jpg,jpeg,png,gif,webp}'))

    if sample_images:
        print(f"Found {len(sample_images)} image(s) in current directory:")
        for img in sample_images[:3]:  # Show first 3
            print(f"  - {img}")
        print()

        # Analyze first image found
        test_image = str(sample_images[0])
        print(f"📸 Analyzing: {test_image}\n")
        print("=" * 70)

        response = image_agent(f"Analyze the image at {test_image}")
        print(response)

    else:
        print("No images found in current directory.")
        print("Creating a sample image for demonstration...\n")

        # Create and analyze a sample image
        response = image_agent("Create a sample image and then analyze it")
        print(response)

    print("\n" + "=" * 70)
    print("✨ Demo complete!")
    print("\n📚 To use with your own images:")
    print("  1. Place image files in the current directory")
    print("  2. Run: uv run python 19_image_analysis.py")
    print("\n💡 Or use the agent interactively:")
    print('  response = image_agent("Analyze path/to/your/image.jpg")')
    print("\n⚙️  Requirements:")
    print("  - AWS credentials configured")
    print("  - Claude 3 Sonnet enabled in Bedrock")
    print("  - (Optional) uv add pillow  # For creating sample images")
    print("=" * 70)


if __name__ == "__main__":
    main()


"""
Setup Instructions:

1. Configure AWS credentials:
   - Set up ~/.aws/credentials with your AWS access key
   - Or set environment variables:
     export AWS_ACCESS_KEY_ID="your-key"
     export AWS_SECRET_ACCESS_KEY="your-secret"
     export AWS_DEFAULT_REGION="us-east-1"

2. Enable Claude 3 in Bedrock:
   - Go to AWS Console > Bedrock > Model access
   - Request access to "Anthropic Claude 3 Sonnet"
   - Wait for approval (usually instant)

3. Install optional dependencies:
   uv add pillow  # For creating test images

4. Run the demo:
   uv run python 19_image_analysis.py

5. Use with your own images:
   # Place images in the same directory, or provide full path
   response = image_agent("Analyze my_photo.jpg")

Example Questions to Ask:
- "Describe this image in detail"
- "What text can you see in this image?"
- "What objects are present in this image?"
- "What is the mood or atmosphere of this scene?"
- "Identify the main colors in this image"
- "What activities are happening in this image?"

Supported Image Formats:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

Image Size Limits:
- Max file size: ~5MB (Bedrock limit)
- Recommended: Resize large images before analysis

Production Enhancements:
- Add image preprocessing (resize, optimize)
- Implement caching for repeated analyses
- Add batch processing for multiple images
- Handle image URLs (download and analyze)
- Add confidence scores for detections
- Implement retry logic for API calls
- Add cost tracking and monitoring
- Support video frame extraction

Alternative Vision Models:
- Claude 3 Opus (more capable, slower)
- Claude 3 Haiku (faster, less expensive)
- Google Gemini Pro Vision
"""


"""Sample output

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run 19_image_analysis.py     
======================================================================
🖼️  Image Analysis with AWS Bedrock Claude
======================================================================

No images found in current directory.
Creating a sample image for demonstration...

I'll create a sample image first and then analyze it for you.
Tool #1: create_sample_image
Now let me analyze the sample image that was created:
Tool #2: analyze_image_with_claude
Perfect! I've created and analyzed a sample image. Here's what the analysis revealed:

**Sample Image Analysis:**

The created sample image is a simple test image containing:

- **Layout**: Clean, minimalist design on a white background
- **Shapes**: Two geometric elements positioned side by side
  - **Left**: A blue rectangle 
  - **Right**: A red oval/ellipse
- **Text**: "Test Image" label appears below the shapes
- **Purpose**: This appears to be a basic test or reference image, commonly used for demonstration purposes

The image demonstrates basic geometric shapes and colors, making it ideal for testing image analysis capabilities. It's a straightforward design that clearly shows how the vision model can identify shapes, colors, positioning, and text elements within an image.

Would you like me to analyze a different image or ask any specific questions about this sample image?Perfect! I've created and analyzed a sample image. Here's what the analysis revealed:

**Sample Image Analysis:**

The created sample image is a simple test image containing:

- **Layout**: Clean, minimalist design on a white background
- **Shapes**: Two geometric elements positioned side by side
  - **Left**: A blue rectangle 
  - **Right**: A red oval/ellipse
- **Text**: "Test Image" label appears below the shapes
- **Purpose**: This appears to be a basic test or reference image, commonly used for demonstration purposes

The image demonstrates basic geometric shapes and colors, making it ideal for testing image analysis capabilities. It's a straightforward design that clearly shows how the vision model can identify shapes, colors, positioning, and text elements within an image.

Would you like me to analyze a different image or ask any specific questions about this sample image?


======================================================================
✨ Demo complete!

📚 To use with your own images:
  1. Place image files in the current directory
  2. Run: uv run python 19_image_analysis.py
"""