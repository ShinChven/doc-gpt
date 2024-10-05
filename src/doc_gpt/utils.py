from pathlib import Path
import PyPDF2
import click
from docx import Document
from pptx import Presentation

from doc_gpt.config import get_config
from .ai_client import AIClient

def process_input(input_path):
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"Error: {input_path} does not exist.")
        return ""
    
    if input_path.is_dir():
        content = ""
        for file in input_path.glob('*'):
            content += process_file(file) + "\n\n"
        return content.strip()
    else:
        return process_file(input_path)

def process_file(file_path):
    ext = file_path.suffix.lower()
    
    try:
        if ext in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == '.pdf':
            return process_pdf(file_path)
        elif ext == '.docx':
            return process_docx(file_path)
        elif ext == '.pptx':
            return process_pptx(file_path)
        else:
            print(f"Warning: Unsupported file type {ext} for {file_path}")
            return ""
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return ""

def process_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join(page.extract_text() for page in reader.pages)

def process_docx(file_path):
    doc = Document(file_path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

def process_pptx(file_path):
    prs = Presentation(file_path)
    text_content = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, 'text'):
                text_content.append(shape.text)
    return "\n".join(text_content)

def write_output(content, output, input_file):
    input_path = Path(input_file)
    output = Path(output or Path.cwd())
    
    # Create the output directory if it's a new path with no extension
    if not output.exists() and output.suffix == "":
        output.mkdir(parents=True, exist_ok=True)

    # If output is a directory, set the output to a file within that directory
    if output.is_dir():
        output = output / f"{input_path.stem}.doc-gpt.md"
        
    # Create the output file if it doesn't exist
    if not output.exists():
        output.touch()

    # Write or append content to the output file
    with open(output, 'a', encoding='utf-8') as f:
        if output.stat().st_size > 0:
            file_divider = f"\n------\n\n"
            f.write(file_divider)
        f.write(content + "\n")
    
    print(f"Output written to {output}")

def process_task(input_file, output_file, model_alias, prompt_file, instructions_file):
    print(f"Processing task for {input_file}")

    try:
        client = AIClient(get_config())
        input_text = process_input(input_file)

        if prompt_file:
            prompt = process_input(prompt_file)
        else:
            default_prompt_file = Path.cwd() / 'prompt.md'
            if default_prompt_file.exists():
                prompt = process_input(default_prompt_file)
            else:
                prompt = click.prompt("Enter your prompt", type=str)

        if not prompt.strip():
            raise click.UsageError("Prompt cannot be empty")

        instructions = ""
        if instructions_file:
            instructions = process_input(instructions_file)
        else:
            default_instructions_file = Path.cwd() / 'instructions.md'
            if default_instructions_file.exists():
                instructions = process_input(default_instructions_file)

        messages = []
        if instructions:
            messages.append({"role": "system", "content": instructions})

        message = """
<ProvidedDocument>
[document]
</ProvidedDocument>

[prompt]
""".replace("[document]", input_text).replace("[prompt]", prompt)
        messages.append({"role": "user", "content": message})
        response = client.request(messages, model_alias)
        write_output(response, output_file, input_file)
        click.echo("Content generation completed successfully.")
    except click.UsageError as e:
        click.echo(f"Usage error: {str(e)}", err=True)
    except click.ClickException as e:
        click.echo(str(e), err=True)
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)