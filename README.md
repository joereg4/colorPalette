# OpenAI ChatGPT Color Palette Generator

## Overview

This project is a web application that leverages OpenAI's ChatGPT to generate custom color palettes based on user input. Simply type in a theme, mood, or instructions, and receive a beautifully curated set of 2 to 8 colors.

## Features

- **AI-Powered Color Generation**: Utilizes OpenAI's GPT-4 model to interpret user prompts and generate relevant color palettes.
- **Flexible Output**: Generates between 2 to 8 colors per palette, depending on the complexity of the prompt.
- **Interactive UI**: Click on any color's HEX code to copy it to your clipboard for easy use in your projects.
- **Responsive Design**: Works seamlessly on both desktop and mobile devices.

## How to Use

1. Visit the application's main page.
2. Enter a theme, mood, or specific instructions in the provided text input.
3. Click the "Generate" button or press Enter.
4. View your custom color palette displayed on the screen.
5. Hover over any color to see its HEX code.
6. Click on the HEX code to copy it to your clipboard.

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python with Flask
- **AI Model**: OpenAI GPT-4
- **Deployment**: Docker, Nginx

## Local Development

To set up this project locally:

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the Flask development server:
   ```
   flask run
   ```

## Deployment

This project is configured for deployment using Docker and Nginx. Refer to the `Dockerfile` and `docker-compose.yml` for more details on the deployment setup.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your chosen license here]

## Acknowledgements

- OpenAI for providing the GPT-4 model
- Flask community for the excellent web framework
- All contributors and users of this project
