import asyncio
from agents.content_director import ContentDirector

async def main():
    # Initialize the Content Director
    director = ContentDirector()
    
    # Example content creation request
    content_request = {
        "topic": "The Future of AI in Construction",
        "platforms": ["linkedin", "x"],
        "tone": "professional",
        "target_audience": "construction industry professionals",
        "keywords": ["AI", "construction", "technology", "innovation", "future"]
    }
    
    print("Creating content...")
    results = await director.create_content(**content_request)
    
    # Print results
    print("\nContent Creation Results:")
    print(f"Content ID: {results['created_at']}")
    print(f"Topic: {results['topic']}")
    print(f"Platforms: {', '.join(results['platforms'])}")
    
    print("\nGenerated Content:")
    for platform, content in results['content'].items():
        print(f"\n{platform.upper()} Content:")
        print("-" * 50)
        print(content)
        print("-" * 50)
    
    # Review the content
    print("\nReviewing content...")
    review_results = await director.review_content(results['created_at'])
    
    print("\nReview Results:")
    for platform, review in review_results['platform_reviews'].items():
        print(f"\n{platform.upper()} Review:")
        print("Recommendations:")
        for rec in review['recommendations']:
            print(f"- {rec}")
        print("\nSEO Suggestions:")
        for suggestion in review['seo_suggestions']:
            print(f"- {suggestion}")

if __name__ == "__main__":
    asyncio.run(main()) 