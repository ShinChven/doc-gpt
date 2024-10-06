# doc-gpt

doc-gpt is a powerful Python CLI tool designed to process document files (PDF, DOCX, PPTX, TXT, MD) using Large Language Models (LLMs). It offers a flexible and efficient way to generate content, manage model configurations, and process multiple files asynchronously.

## Features

- Support for multiple file types: PDF, DOCX, PPTX, TXT, MD
- Configurable model settings with multiple providers (e.g., OpenAI, Ollama)
- Batch processing of files with customizable batch size
- Flexible input options: process single files or entire directories
- Customizable prompts and system instructions

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
- `--model_name`: The name of the model (e.g., "gpt-4")
- `--provider`: The provider of the model (e.g., "openai" or "ollama")
- `--key`: The API key (optional, depending on the provider)
- `--api_base`: The API base URL (optional)

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

To generate content using a configured model:

```bash
doc-gpt g --input INPUT_PATH --output OUTPUT_FILE --model_alias MODEL_ALIAS --prompt PROMPT_FILE --instructions INSTRUCTIONS_FILE --batch_size BATCH_SIZE
```

- `--input` or `-i`: Path to the input file or directory (required)
- `--output` or `-o`: Path to the output file (optional, default: input_file_name.doc-gpt.md)
- `--model_alias` or `-m`: The alias of the model to use (optional, uses default if not specified)
- `--prompt` or `-p`: Path to a file containing the prompt (optional)
- `--instructions` or `-s`: Path to a file containing system instructions (optional)
- `--batch_size` or `-b`: Number of tasks to run asynchronously (default is 1)

If a prompt file is not provided, you'll be prompted to enter the prompt manually.

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