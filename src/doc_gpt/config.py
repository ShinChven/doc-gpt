import json
import click
from pathlib import Path

CONFIG_FILE = Path.home() / '.doc-gpt' / 'config.json'

def get_config():
    if not CONFIG_FILE.exists():
        return {"default_model": "", "models": {}}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def update_config(alias, model_name, provider, key, api_base):
    config = get_config()
    
    if not alias:
        alias = click.prompt("Enter model alias")
    if not model_name:
        model_name = click.prompt("Enter model name")
    if not provider:
        provider = click.prompt("Enter provider")
    if key is None:
        key = click.prompt("Enter API key (optional)", default="")
    if api_base is None:
        api_base = click.prompt("Enter API base URL (optional)", default="")
    
    if alias in config['models']:
        if not click.confirm(f"Model alias '{alias}' already exists. Do you want to overwrite it?"):
            click.echo("Configuration update cancelled.")
            return
    
    config['models'][alias] = {
        "model_name": model_name,
        "provider": provider,
        "key": key,
        "api_base": api_base
    }
    
    if not config['default_model']:
        config['default_model'] = alias
    
    save_config(config)
    click.echo(f"Configuration updated for model alias '{alias}'")

def set_default_model(alias):
    config = get_config()
    if alias not in config['models']:
        raise click.ClickException(f"Error: Model alias '{alias}' not found in configuration.")
    
    config['default_model'] = alias
    save_config(config)
    click.echo(f"Default model set to '{alias}'")

def save_config(config):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_model_config(model_alias=None):
    config = get_config()
    if not model_alias:
        model_alias = config['default_model']
    
    if not model_alias:
        raise click.ClickException("No default model specified in configuration")
    
    if model_alias not in config['models']:
        raise click.ClickException(f"Model alias '{model_alias}' not found in configuration")
    
    return config['models'][model_alias]

def config_command(alias, model_name, provider, key, api_base):
    """Configure a new model or update an existing one."""
    try:
        update_config(alias, model_name, provider, key, api_base)
    except click.Abort:
        click.echo("Configuration cancelled.")
    except Exception as e:
        click.echo(f"Error updating configuration: {str(e)}", err=True)

def delete_config_command(alias):
    """Delete a model configuration by alias."""
    config = get_config()
    if alias in config['models']:
        model_config = config['models'][alias]

        # Mask the API key
        masked_key = model_config['key'][:2] + "*" * (len(model_config['key']) - 4) + model_config['key'][-2:]

        click.echo(f"Configuration for alias '{alias}':")
        click.echo(f"  Model Name: {model_config['model_name']}")
        click.echo(f"  Provider: {model_config['provider']}")
        click.echo(f"  API Key: {masked_key}")
        click.echo(f"  API Base: {model_config['api_base']}")

        if click.confirm("Are you sure you want to delete this configuration?"):
            del config['models'][alias]
            save_config(config)
            click.echo(f"Configuration for alias '{alias}' has been deleted.")
        else:
            click.echo("Deletion cancelled.")
    else:
        click.echo(f"Error: No configuration found for alias '{alias}'", err=True)

def show_models_command():
    """Show all models with their provider and masked key."""
    config = get_config()
    if not config['models']:
        click.echo("No models configured.", err=True)
        return

    click.echo("Configured models:")
    for alias, model_config in config['models'].items():
        masked_key = model_config['key'][:2] + "*" * (len(model_config['key']) - 4) + model_config['key'][-2:]
        click.echo(f"- Alias: {alias}")
        click.echo(f"  Model Name: {model_config['model_name']}")
        click.echo(f"  Provider: {model_config['provider']}")
        click.echo(f"  API Key: {masked_key}")
        click.echo(f"  API Base: {model_config['api_base']}")
        click.echo("")  # Blank line for better readability