# doc-gpt

doc-gpt is a powerful Python CLI tool designed to process document files (PDF, DOCX, PPTX, TXT, MD) using Large Language Models (LLMs). It offers a flexible and efficient way to generate content, manage model configurations, and process multiple files asynchronously.

## Features

- Support for multiple file types: PDF, DOCX, PPTX, TXT, MD
- Configurable model settings with multiple providers (e.g., OpenAI, Azure OpenAI, Ollama, Claude)
- Batch processing of files with customizable batch size
- Flexible input options: process single files or entire directories
- Customizable prompts and system instructions
- **Automatic loading of default prompt from prompt.md in the current working directory**

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

doc-gpt provides several commands to manage configurations and generate content. Here's an overview of the available commands:

### Configuring a Model

To configure a new model or update an existing one:

```bash
doc-gpt config --alias MODEL_ALIAS --model_name MODEL_NAME --provider PROVIDER --key API_KEY --api_base API_BASE
```

- `--alias`: A unique name for the model configuration
- `--model_name`: The name of the model (e.g., "gpt-4" for OpenAI, "claude-3-sonnet-20240229" for Claude)
- `--provider`: The provider of the model (e.g., "openai", "azure-openai", "ollama", or "claude")
- `--key`: The API key (optional, depending on the provider)
- `--api_base`: The API base URL (optional, defaults to https://api.anthropic.com for Claude)

If you don't provide all options, you'll be prompted to enter the missing information.

### Setting the Default Model

To set the default model:

```bash
doc-gpt set-default MODEL_ALIAS
```

### Deleting a Model Configuration

To delete a model configuration:

```bash
doc-gpt delete-config MODEL_ALIAS
```

### Showing All Configured Models

To display all configured models with their provider and masked API key:

```bash
doc-gpt show-models
```

### Generating Content

To generate content with a configured model, use the following command:

```
doc-gpt g --input <INPUT_PATH> --output <OUTPUT_FILE> --model_alias <MODEL_ALIAS> --prompt <PROMPT_FILE> --instructions <INSTRUCTIONS_FILE> --batch_size <BATCH_SIZE>
```

- `--input` or `-i`: Specify the path to the input file or directory (mandatory)
- `--output` or `-o`: Designate the path for the output file (optional, default: input_file_name.doc-gpt.md)
- `--model_alias` or `-m`: Indicate the alias for the model (optional, defaults to the pre-set model)
- `--prompt` or `-p`: Provide the path to the prompt file (optional)
- `--instructions` or `-s`: Specify the path to the system instructions file (optional)
- `--batch_size` or `-b`: Define the number of tasks to process concurrently (default is 1)

**Important: Default Prompt Loading**
If a prompt file is not provided using the `--prompt` option, doc-gpt will automatically look for a file named `prompt.md` in the current working directory and use it as the default prompt. This feature allows you to maintain a consistent prompt across multiple runs without explicitly specifying it each time.

If neither a prompt file is provided nor a `prompt.md` file exists in the current working directory, you'll be prompted to enter the prompt manually.

## Supported File Types

doc-gpt supports the following file types:
- PDF (.pdf)
- Microsoft Word (.docx)
- Microsoft PowerPoint (.pptx)
- Text (.txt)
- Markdown (.md)

When processing a directory, doc-gpt will process all supported files in the directory.

## Batch Processing

doc-gpt supports batch processing of files, allowing you to process multiple files concurrently. Use the `--batch_size` option to specify the number of files to process simultaneously. This can significantly speed up processing when dealing with multiple files.

## Configuration

doc-gpt stores its configuration in `~/.doc-gpt/config.json`. You can manually edit this file if needed, but it's recommended to use the `config` command to manage your configurations.

## Error Handling

If you encounter any errors while using doc-gpt, the application will provide informative error messages to help you troubleshoot the issue.

## Contributing

Contributions to doc-gpt are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.