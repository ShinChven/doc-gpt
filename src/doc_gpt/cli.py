import click
from pathlib import Path
from .config import config_command, set_default_model, delete_config_command, show_models_command 
from .utils import process_task

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
    config_command(alias, model_name, provider, key, api_base)

@main.command()
@click.argument('alias')
def set_default(alias):
    """Set the default model."""
    try:
        set_default_model(alias)
    except click.ClickException as e:
        click.echo(str(e), err=True)

@main.command()
@click.argument('alias')
def delete_config(alias):
    """Delete a model configuration by alias."""
    delete_config_command(alias)

@main.command()
def show_models():
    """Show all models with their provider and masked key."""
    show_models_command()



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