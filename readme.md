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