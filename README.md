# Create Your Style

Create Your Style is an application that allows users to virtually try on garments on a model image using the IDM-VITON API by Yisol.

## Introduction

Create Your Style leverages the IDM-VITON API to enable users to upload an image of a person and overlay various garments onto the image. This allows users to visualize how different clothing items look on different body types before making a purchase decision.

## Features

- *Virtual Try-On*: Upload an image of a person and select a garment to see how it looks on the person.
- *Post Outfits*: Users can post outfits created through the virtual try-on to share with others.
- *View and Rate*: View outfits posted by others and rate them with likes or dislikes.

## Technology Stack

- *API*: IDM-VITON by Yisol
- *Python Libraries*: Gradio for building the user interface, PIL (Python Imaging Library) for image processing, and JSON for managing post data.
- *File Handling*: os and shutil modules for file operations and managing posted outfits.
- *Frontend*: HTML, CSS, and JavaScript (used within Gradio) for building the user interface.
- *Persistence*: JSON file (posts.json) to store posted outfit information.

## Getting Started

To run the application locally:

1. Clone the repository:
   bash
   git clone https://github.com/thrishalaa/create-your-style.git
   cd create-your-style
   
    - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
     
2. **Running the Application**
   - Run the Python script:
     ```
     python app.py
     ```
   
3. *Using the Application*
   - Upload a person's image and select a garment image.
   - Optionally, describe the garment and choose auto-mask and auto-crop options.
   - Click on "Try On" to see the virtual try-on result.
   - If satisfied, click on "Post Outfit" to save and share your creation.

4. *Viewing Posted Outfits*
   - Click on "View Posted Outfits" to see outfits posted by other users.
   - Rate outfits using the like and dislike buttons.

## Credits

- *IDM-VITON Model*: Developed by yisol. API integration facilitated by Gradio client.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
