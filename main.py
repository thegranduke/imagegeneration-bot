import os
import io
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv("IMAGE_GENERATION_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

def generate_image(prompt):
    """
    Generate an image using Pollinations AI API.
    
    Args:
        prompt (str): Text description for image generation
    
    Returns:
        bytes: Image data, or None if generation fails
    """
    try:
        # Pollinations AI image generation endpoint
        url = f"https://image.pollinations.ai/prompt/{prompt}"
        
        # Send GET request to generate image
        response = requests.get(url)
        response.raise_for_status()
        
        # Return image bytes
        return response.content
    except requests.RequestException as e:
        print(f"Error generating image: {e}")
        return None

@bot.command(name='imagine')
async def imagine(ctx, *, prompt: str):
    """
    Generate and send an image based on the user's prompt.
    
    Args:
        ctx (Context): Command context
        prompt (str): Full text prompt for image generation
    """
    # Send a "thinking" message while processing
    thinking_message = await ctx.send("🤔 Generating image...")
    
    try:
        # Generate the image
        image_data = generate_image(prompt)
        
        if image_data:
            # Create a file-like object from the image bytes
            image_file = discord.File(
                io.BytesIO(image_data), 
                filename="generated_image.png"
            )
            
            # Delete the "thinking" message
            await thinking_message.delete()
            
            # Send the image with the original prompt as a caption
            await ctx.send(f"Image generated for prompt: *{prompt}*", file=image_file)
        else:
            # Error handling if image generation fails
            await thinking_message.edit(content="❌ Failed to generate image. Please try again.")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        await thinking_message.edit(content="❌ An unexpected error occurred.")

bot.run(TOKEN)




