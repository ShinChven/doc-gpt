from pathlib import Path
import click
import threading
import re

from .config import (
    config_command,
    delete_config_command,
    set_default_model,
    show_models_command,
)
from .utils import process_task, is_valid_url, process_input

@click.group()
def main():
    pass

@main.command()
@click.option("-a", "--alias", help="Model alias")
@click.option("-m", "--model_name", help="Model name")
@click.option("-p", "--provider", help="Provider name")
@click.option("-k", "--key", help="API key")
@click.option("-b", "--api_base", help="API base URL")
def config(alias, model_name, provider, key, api_base):
    """Configure a new model or update an existing one."""
    config_command(alias, model_name, provider, key, api_base)

@main.command()
@click.option("-a", "--alias", help="Model alias to set as default")
def set_default(alias):
    """Set the default model."""
    try:
        set_default_model(alias)
    except click.ClickException as e:
        click.echo(str(e), err=True)

@main.command()
@click.option("-a", "--alias", required=False, help="Model alias to delete")
def delete_model(alias):
    """Delete a model configuration by alias."""
    delete_config_command(alias)

@main.command()
def show_models():
    """Show all models with their provider and masked key."""
    show_models_command()

@main.command()
@click.option(
    "-i", "--input", "input_path", required=True, help="Input file, directory, or URL"
)
@click.option("-o", "--output", "output_file", help="Output file")
@click.option("-m", "--model_alias", help="Model alias")
@click.option("-p", "--prompt", "prompt_file", help="Prompt file")
@click.option("-s", "--instructions", "instructions_file", help="Instructions file")
@click.option(
    "-b",
    "--batch_size",
    default=1,
    type=int,
    help="Number of tasks to run asynchronously (default is 1)",
)
@click.option(
    "-wp",
    "--write_prompt",
    is_flag=True,
    help="Include prompt in the saved response"
)
@click.option(
    "-mt",
    "--max_tokens",
    default=None,
    type=int,
    help="Max output tokens for all supported provider's requests (default is None)"
)
def g(input_path, output_file, model_alias, prompt_file, instructions_file, batch_size, write_prompt, max_tokens):
    """Generate content using the specified model and input."""

    def process_file(file, output_file_param):
        if output_file_param is None:
          output_file_param = str(Path.cwd() / (file.stem + ".doc-gpt.md"))
        process_task(str(file), output_file_param, model_alias, prompt_file, instructions_file, write_prompt, max_tokens)

    try:
        if is_valid_url(input_path):
            # If input is a URL, process it directly
            process_task(input_path, output_file, model_alias, prompt_file, instructions_file, write_prompt, max_tokens)
        else:
            path = Path(input_path)
            files = []

            if path.is_file() and path.suffix in {".pdf", ".docx", ".txt", ".md", ".pptx"}:
                files.append(path)
            elif path.is_dir():
                files.extend(
                    file
                    for file in path.iterdir()
                    if file.is_file()
                    and file.suffix in {".pdf", ".docx", ".txt", ".md", ".pptx"}
                )
            else:
                click.echo(
                    "Unsupported input type or no valid files in directory.", err=True
                )
                return

            if not files:
                click.echo("No valid files found.", err=True)
                return

            # Process the files in batches asynchronously
            for i in range(0, len(files), batch_size):
                batch_files = files[i : i + batch_size]
                threads = []

                for file in batch_files:
                    thread = threading.Thread(target=process_file, args=(file, output_file))
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()

    except click.UsageError as e:
        click.echo(f"Usage error: {str(e)}", err=True)
    except click.ClickException as e:
        click.echo(str(e), err=True)
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)


@main.command()
@click.argument("input_path", required=True, type=click.Path(exists=True))
@click.option("-o", "--output", "output_file", help="Output file")
def text(input_path, output_file):
    """Extract text from document and output to .doc-gpt.txt file."""
    try:
        input_path_obj = Path(input_path)
        if output_file is None:
            output_file = str(Path.cwd() / (input_path_obj.stem + ".doc-gpt.txt")) # Changed this line
        extracted_text = process_input(input_path)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        click.echo(f"Text extracted and saved to {output_file}")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)


if __name__ == "__main__":
    main()
