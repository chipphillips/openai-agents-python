# Content Marketing Agent Team

A sophisticated multi-agent system for creating and optimizing content across different social media platforms. This team of AI agents works together to create high-quality, platform-optimized content under the direction of a Content Director.

## Team Structure

### Content Director
- Oversees the content creation process
- Assigns tasks to specialized agents
- Ensures content quality and consistency
- Manages the overall content strategy

### Specialized Agents
1. **Platform-Specific Experts**
   - LinkedIn Content Specialist
   - X (Twitter) Content Specialist
   - Instagram Content Specialist
   - (More platforms can be added)

2. **Content Writers**
   - Copywriting Specialist
   - SEO Specialist
   - Content Editor

3. **Research Team**
   - Topic Research Specialist
   - Trend Analysis Specialist
   - Competitor Analysis Specialist

## Features

- Multi-platform content generation
- Platform-specific optimization
- Automated research and fact-checking
- SEO optimization
- Content consistency across platforms
- Automated content scheduling suggestions

## Directory Structure

```
content-marketing-team/
├── agents/                 # Agent definitions and configurations
├── tools/                  # Tools available to agents
├── agent-output/          # Generated content
│   └── new-content/       # Latest content creations
└── config/                # Configuration files
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configurations
```

3. Run the content creation team:
```bash
python main.py
```

## Usage

1. Start the content creation process:
```python
from content_marketing_team import ContentDirector

director = ContentDirector()
content = await director.create_content(
    topic="Your Topic",
    platforms=["linkedin", "x"],
    tone="professional",
    target_audience="tech professionals"
)
```

2. The content will be automatically saved in the `agent-output/new-content/` directory with platform-specific files.

## Output Format

Content is saved in the following format:
```
agent-output/
└── new-content/
    ├── linkedin-post.md
    ├── x-post.md
    └── metadata.json
```

## Configuration

Edit `config/agent_config.yaml` to customize:
- Agent behaviors
- Platform-specific settings
- Content guidelines
- Research parameters

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 