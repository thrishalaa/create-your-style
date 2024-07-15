import gradio as gr
from gradio_client import Client, handle_file
from PIL import Image
import json
import os
import numpy as np
import shutil

# Initialize the client
client = Client("kadirnar/IDM-VTON")

# File to store posts
POSTS_FILE = "posts.json"
POSTS_FOLDER = "posted_outfits"

# Ensure the posts folder exists
if not os.path.exists(POSTS_FOLDER):
    os.makedirs(POSTS_FOLDER)

# Function to load posts from JSON file
def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    return []

# Function to save posts to JSON file
def save_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f)

# Function to add a new post
def add_post(image_path):
    posts = load_posts()
    new_filename = f"outfit_{len(posts)}.jpg"
    new_path = os.path.join(POSTS_FOLDER, new_filename)
    shutil.copy(image_path, new_path)
    new_post = {
        "image": new_path,
        "likes": 0,
        "dislikes": 0
    }
    posts.append(new_post)
    save_posts(posts)

# Function to update likes/dislikes
def update_post(index, action):
    posts = load_posts()
    if action == "like":
        posts[index]["likes"] += 1
    elif action == "dislike":
        posts[index]["dislikes"] += 1
    save_posts(posts)
    return f"Likes: {posts[index]['likes']} | Dislikes: {posts[index]['dislikes']}"

def virtual_try_on(person_image, clothing_image, auto_mask, auto_crop, garment_description):
    # Use the client to perform the virtual try-on
    result = client.predict(
        dict={"background": handle_file(person_image) if person_image else None, "layers": [], "composite": None},
        garm_img=handle_file(clothing_image) if clothing_image else None,
        garment_des=garment_description,
        is_checked=auto_mask,
        is_checked_crop=auto_crop,
        denoise_steps=30,
        seed=42,
        api_name="/tryon"
    )
    
    # The result is a tuple of 2 file paths
    output_image_path, _ = result
    
    # Open and return the results as numpy arrays
    output_image = np.array(Image.open(output_image_path)) if output_image_path else None
    
    return output_image

def post_outfit(output_image):
    if output_image is not None:
        temp_path = "temp_outfit.jpg"
        if isinstance(output_image, np.ndarray):
            img = Image.fromarray(output_image.astype('uint8'), 'RGB')
            img.save(temp_path)
        else:
            output_image.save(temp_path)
        add_post(temp_path)
        os.remove(temp_path)
        return "Outfit posted successfully!"
    return "No outfit to post."

# Define main Gradio interface
with gr.Blocks(title="CREATE YOUR STYLE") as main_interface:
    gr.Markdown(
        "<div style='text-align: center; max-width: 800px; margin: 0 auto;'>"
        "<h1>CREATE YOUR STYLE</h1>"
        "<p>Upload an image of a person and Select the garment 👤</p>"
        "</div>"
    )
    
    view_posts_button = gr.Button("View Posted Outfits")
    
    try_on_interface = gr.Group()
    with try_on_interface:
        with gr.Row(equal_height=True):
            with gr.Column(scale=1):
                person_image = gr.Image(label="Human: Mask with pen or use auto-masking", type="filepath")
                auto_mask = gr.Checkbox(label="Use auto-generated mask (Takes 5 seconds)", value=True)
                auto_crop = gr.Checkbox(label="Use auto crop & resizing")
                person_examples = gr.Examples(
                    examples=["model5.jpg", "model7.png"],
                    inputs=person_image,
                    label="Examples"
                )
            with gr.Column(scale=1):
                clothing_image = gr.Image(label="Garment", type="filepath")
                garment_description = gr.Textbox(label="Description of garment (e.g. Short Sleeve Round Neck T-shirts)")
                garment_examples = gr.Examples(
                    examples=["top1.png", "bottom1.png", "top2.jpg"],
                    inputs=clothing_image,
                    label="Examples"
                )
        
        with gr.Row():
            try_on_button = gr.Button("Try On", size="lg")
        
        with gr.Row(equal_height=True):
            with gr.Column(scale=1):
                final_output = gr.Image(label="Output")
        
        with gr.Row():
            post_button = gr.Button("Post Outfit", size="lg")
        
        post_status = gr.Textbox(label="Post Status")
    
    posts_interface = gr.Group(visible=False)
    with posts_interface:
        gr.Markdown(
            "<div style='text-align: center; max-width: 800px; margin: 0 auto;'>"
            "<h1>Posted Outfits</h1>"
            "<p>View and rate outfits created by other users</p>"
            "</div>"
        )
        
        back_button = gr.Button("Back to Try-On")
        
        posts = load_posts()
        for index, post in enumerate(posts):
            with gr.Row():
                gr.Image(post["image"])
                with gr.Column():
                    likes_display = gr.Markdown(f"Likes: {post['likes']} | Dislikes: {post['dislikes']}")
                    like_button = gr.Button("👍 Like")
                    dislike_button = gr.Button("👎 Dislike")
                    
                    like_button.click(
                        update_post,
                        inputs=[gr.Slider(value=index, visible=False), gr.Textbox(value="like", visible=False)],
                        outputs=[likes_display]
                    )
                    dislike_button.click(
                        update_post,
                        inputs=[gr.Slider(value=index, visible=False), gr.Textbox(value="dislike", visible=False)],
                        outputs=[likes_display]
                    )
    
    try_on_button.click(
        fn=virtual_try_on,
        inputs=[person_image, clothing_image, auto_mask, auto_crop, garment_description],
        outputs=[final_output]
    )
    
    post_button.click(
        fn=post_outfit,
        inputs=[final_output],
        outputs=[post_status]
    )
    
    def switch_to_posts():
        return gr.update(visible=False), gr.update(visible=True)

    def switch_to_main():
        return gr.update(visible=True), gr.update(visible=False)
    
    view_posts_button.click(
        switch_to_posts,
        outputs=[try_on_interface, posts_interface]
    )
    
    back_button.click(
        switch_to_main,
        outputs=[try_on_interface, posts_interface]
    )

# Launch the Gradio interface
main_interface.launch()