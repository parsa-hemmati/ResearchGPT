# ResearchGPT

ResearchGPT is a Flask-based web application designed to assist medical researchers in performing systematic reviews and meta-analyses. Utilizing OpenAI's GPT-3.5-turbo model, it evaluates the relevance of articles from PubMed based on a user-specified research question.

## Project Structure

\`\`\`
ResearchGPT/
├── static/
│   ├── css/
│   │   └── main.css
├── templates/
│   ├── index.html
│   └── results.html
└── app.py
\`\`\`

## Features

- **PubMed Search**: Allows users to search for relevant articles from PubMed using a custom query.
- **Relevance Analysis**: Utilizes GPT-3.5-turbo to analyze the relevance of each article based on the research question.
- **Results Display**: Presents the search results, highlighting relevant articles.

## Installation

1. Clone the repository:

    \`\`\`bash
    git clone https://github.com/yourusername/ResearchGPT.git
    \`\`\`

2. Navigate to the project directory:

    \`\`\`bash
    cd ResearchGPT
    \`\`\`

3. Install the required dependencies:

    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

## Usage

1. Run the Flask application:

    \`\`\`bash
    python app.py
    \`\`\`

2. Open your web browser and navigate to [http://localhost:5000](http://localhost:5000).

3. Enter your email, OpenAI API Key, meta-analysis research question, and PubMed search query.

4. Click on the "Search" button to view the relevant articles.

## Dependencies

- Flask
- OpenAI
- Biopython
- Pandas

Make sure to include a \`requirements.txt\` file with the appropriate version numbers for these packages.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details.

## Contributing

Feel free to open issues or pull requests if you want to contribute to this project.

## Acknowledgements

Thanks to OpenAI for providing access to the GPT-3.5-turbo model and to the Biopython community for the tools to interact with PubMed.
