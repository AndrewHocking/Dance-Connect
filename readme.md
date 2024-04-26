# Setup

## Step 1: Create a Python virtual environment

In the DanceConnect folder, run: `python -m venv .venv`

## Step 2: Activate environment

### Mac/Linux

`source .venv/bin/activate`

### Windows

`.venv/Scripts/activate`

## Step 3: Install requirements

`pip install -r requirements.txt`

## Step 4: Run the server

`python main.py`



---

# Alternate Setup within VSCODE

- In VSCODE, press "cmd+shift+p" for macOS or "Ctrl+Shift+P" in windows
- search for "Python: Create Environment..."
- select "venv"
- select your python version
- select install requirements from file and select the "requirements.txt file"
- press the run triangle in the top right corner of the screen while having the main.py file open

---
<br>

## CKeditor Setup

### Setting up the Editor UI

1. Load the CKeditor script via CDN. The basic verison includes most features that we'd use (Bold, Italics, H1/H2/H3, Lists, Link/Imgs)
    ``<script src="https://cdn.ckeditor.com/ckeditor5/41.3.1/classic/ckeditor.js"></script>``
2. Create a `<textarea>` or `<div>` in the HTML with a unique id.
3. Configure the editor using JS (Replace `editor-id` with id of element from step 2): 
    - `items` is the list of toolbar features that the user can use
    - `removedItems` are disabled
    - `|` is used to separate elements in  the toolbar UI into groups
```
ClassicEditor.create(document.getElementById(editor-id), {
    toolbar: {
        items: [
            'undo', 'redo',
            '|', 'heading',
            '|', 'bold', 'italic', 'link',
            '|', 'bulletedList', 'numberedList', 'outdent', 'indent',
            '|',
        ],
        removeItems: ['uploadImage', 'blockQuote', 'mediaEmbed', 'insertTable'],
    }
});

```

### Retrieving User Input
4. Get user input from the `<div>` or `<textarea>` as you normally would using. (Only tried with `<textarea>` so far).
5. Sanitize html input by importing the `sanitize_html` method from `\website\__init__.py`.
    - Note: This basically whitelists a set of acceptable HTML elements and escapes everything else. It works for the config example in step 3, but if additional toolbar items are enabled, you would can pass a list of tags into `additional_tags` to enable them. Ex: `sanitize_html(html_input, ['img', 'br'])`
    - Note 2: Probably best to use as few tags as possible for better security.
6. To validate the input before it is submitted (e.g. making a field required):
    - Load JQuery Validation from CDN: `<script src="https://cdn.ckeditor.com/ckeditor5/41.3.1/classic/ckeditor.js"></script>`
    - Configure the validator in JS:
    ```
    $("form").validate({
        ignore: [],
        rules: {
            input1_name_attribute: { required: true },
            input2_name_attribute: { 
                required: true,
                minlength: 5,
            },
            ...
        }, 
        messages: {
            input1_name_attribute: "This field is mandatory",
            input2_name_attribute: { 
                required: "This field is mandatory.",
                minlength: "This field must have at least 5 characters.",
            },
            ...
        }
    })
    ```
    - `rules` specify how to validate the input
    - `messages` are the error messages the user sees if validation on any field fails

### Display HTML
7. By default Jinja will display the raw HTML text if you use it as any other variable, instead add `|safe` to tell Jinja that this HTML code is safe to be rendered:
    ```{{ variable_containing_html|safe }}```
---


---
# Chat GPT Tutorials

## Setup Pythonanywhere

Setting up a web app on PythonAnywhere using an existing GitHub project involves a series of steps. Here’s a general process to get your web app running:

### 1. Sign up or Log in to PythonAnywhere
Before you start, you need an account on PythonAnywhere. If you don’t have one, you can sign up at [PythonAnywhere's website](https://www.pythonanywhere.com).

### 2. Create a New Web App
Once logged in:
- Go to the "Web" tab.
- Click "Add a new web app".
- Follow the on-screen instructions to configure your domain (you'll be assigned a pythonanywhere.com subdomain initially).
- Choose the manual configuration option (not the "automatic configuration" for Flask/Django) if your project uses a different framework or needs specific settings.

### 3. Clone Your GitHub Repository
You can clone your repository directly into your PythonAnywhere account using the "Consoles" tab:
- Open a Bash console.
- Navigate to the desired directory, usually something like `/home/yourusername`.
- Use the git command to clone your repository:
  ```bash
  git clone https://github.com/yourusername/yourrepository.git
  ```

### 4. Set Up a Virtual Environment
It's a good practice to create a virtual environment for your project:
- Still in the Bash console, navigate to your project directory:
  ```bash
  cd yourrepository
  ```
- Create a virtual environment:
  ```bash
  mkvirtualenv --python=/usr/bin/python3.8 myenv  # Use appropriate Python version
  ```
- Activate the virtual environment:
  ```bash
  workon myenv
  ```

### 5. Install Dependencies
Install any dependencies your project might have using pip. If your project includes a `requirements.txt` file, you can install all dependencies with:
```bash
pip install -r requirements.txt
```

### 6. Configure the WSGI File
PythonAnywhere uses a WSGI file to serve your web app:
- Go to the "Web" tab again.
- Scroll down to the "Code" section and find the link to your WSGI configuration file.
- Edit the WSGI file to point to your web application. You might need to modify the `sys.path` to include your project directory and set the application callable. This depends on whether you’re using Flask, Django, or another framework.

### 7. Reload Your Web App
After configuring your WSGI file:
- Still in the "Web" tab, scroll to the top and click the green "Reload" button next to your domain name.

### 8. Check Your Web App
Visit your .pythonanywhere.com domain to see if your app is running correctly. If there are issues, check the "Error log" in the "Web" tab for clues.

### 9. Debug and Iterate
You might need to return to the Bash console or the WSGI configuration and make adjustments based on the feedback from error logs or the behavior of your app.

This is a basic guide, and depending on the specific needs of your project or the framework you are using, some steps might differ. For instance, Django projects will need settings for static and media files, while Flask might be simpler but require specific app configurations.