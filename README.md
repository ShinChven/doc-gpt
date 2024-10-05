# doc-gpt

doc-gpt is a Python CLI tool that processes document files (pdf, docx, pptx, txt, md) using Large Language Models.

## Installation

To install the package directly from the GitHub repository, use:
```bash
pip install git+https://github.com/ShinChven/doc-gpt.git
```

For updating the package to the latest version, run:
```bash
pip install --upgrade git+https://github.com/ShinChven/doc-gpt.git
```

## Usage

### Configuring a Model

To configure a new model or update an existing one:

```
doc-gpt config --alias model_alias --model_name model_name --provider provider --key api_key --api_base api_base
```

- `--alias`: A unique name for the model configuration
- `--model_name`: The name of the model (e.g., "gpt-4")
- `--provider`: The provider of the model (e.g., "openai" or "ollama")
- `--key`: The API key (optional, depending on the provider)
- `--api_base`: The API base URL (optional)

If you don't provide all options, you'll be prompted to enter the missing information.

### Setting the Default Model

To set the default model:

```
doc-gpt set-default model_alias
```

### Generating Content

To generate content using a configured model:

```
doc-gpt g --input input_file --output output_file --model_alias model_alias --prompt prompt_file --instructions instructions_file
```

- `--input`: Path to the input file or directory (required)
- `--output`: Path to the output file (optional, default: input_file_name.doc-gpt.md)
- `--model_alias`: The alias of the model to use (optional, uses default if not specified)
- `--prompt`: Path to a file containing the prompt (optional)
- `--instructions`: Path to a file containing system instructions (optional)

If a prompt file is not provided, you'll be prompted to enter the prompt manually.

## Supported File Types

doc-gpt supports the following file types:
- PDF (.pdf)
- Microsoft Word (.docx)
- Microsoft PowerPoint (.pptx)
- Text (.txt)
- Markdown (.md)

When processing a directory, doc-gpt will process all supported files in the directory.

## Configuration

doc-gpt stores its configuration in `~/.doc-gpt/config.json`. You can manually edit this file if needed, but it's recommended to use the `config` command to manage your configurations.

## Error Handling

If you encounter any errors while using doc-gpt, the application will provide informative error messages to help you troubleshoot the issue.

## Contributing

Contributions to doc-gpt are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.