import click
from pathlib import Path
from .config import update_config, get_config, set_default_model 
from .ai_client import AIClient
from .utils import process_input, write_output

@click.group()
def main():
    pass

@main.command()
@click.option('-a', '--alias', help='Model alias')
@click.option('-m', '--model_name', help='Model name')
@click.option('-p', '--provider', help='Provider name')
@click.option('-k', '--key', help='API key')
@click.option('-b', '--api_base', help='API base URL')
def config(alias, model_name, provider, key, api_base):
    """Configure a new model or update an existing one."""
    try:
        update_config(alias, model_name, provider, key, api_base)
    except click.Abort:
        click.echo("Configuration cancelled.")
    except Exception as e:
        click.echo(f"Error updating configuration: {str(e)}", err=True)

@main.command()
@click.argument('alias')
def set_default(alias):
    """Set the default model."""
    try:
        set_default_model(alias)
    except click.ClickException as e:
        click.echo(str(e), err=True)

def process_task(input_file, output_file, model_alias, prompt_file, instructions_file):
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

@main.command()
@click.option('-i', '--input', 'input_path', required=True, help='Input file or directory')
@click.option('-o', '--output', 'output_file', help='Output file')
@click.option('-m', '--model_alias', help='Model alias')
@click.option('-p', '--prompt', 'prompt_file', help='Prompt file')
@click.option('-s', '--instructions', 'instructions_file', help='Instructions file')
def g(input_path, output_file, model_alias, prompt_file, instructions_file):
    """Generate content using the specified model and input."""
    try:
        path = Path(input_path)
        if path.is_file() and path.suffix in {'.pdf', '.docx', '.txt', '.md', '.pptx'}:
            process_task(path, output_file, model_alias, prompt_file, instructions_file)
        elif path.is_dir():
            for file in path.iterdir():
                if file.is_file() and file.suffix in {'.pdf', '.docx', '.txt', '.md', '.pptx'}:
                    process_task(file, output_file, model_alias, prompt_file, instructions_file)
        else:
            click.echo("Unsupported input type or no valid files in directory.", err=True)
    except click.UsageError as e:
        click.echo(f"Usage error: {str(e)}", err=True)
    except click.ClickException as e:
        click.echo(str(e), err=True)
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)

if __name__ == '__main__':
    main()