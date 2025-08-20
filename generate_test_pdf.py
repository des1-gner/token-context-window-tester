import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import random

def generate_test_content(target_words=200000):
    """Generate test content with approximately the target word count"""
    
    # Sample sentences to create varied content
    sentences = [
        "This is a test document created to evaluate token limits in large language models.",
        "The purpose of this document is to reach approximately 200,000 words for comprehensive testing.",
        "Large language models have context windows that define how much text they can process at once.",
        "Token limits are important considerations when building conversational AI applications.",
        "Testing with realistic document sizes helps identify potential issues before production deployment.",
        "AWS Bedrock provides access to various foundation models including Anthropic's Claude.",
        "Understanding model limitations is crucial for building robust AI-powered applications.",
        "This content is generated programmatically to ensure consistent testing conditions.",
        "Performance testing should include edge cases like maximum context window usage.",
        "Proper error handling becomes essential when working with token-limited models."
    ]
    
    content = []
    word_count = 0
    
    while word_count < target_words:
        # Add a random sentence
        sentence = random.choice(sentences)
        content.append(sentence)
        word_count += len(sentence.split())
        
        # Occasionally add paragraph breaks
        if random.random() < 0.1:
            content.append("\n\n")
    
    return " ".join(content)

def create_200k_word_pdf(filename="test_200k_words.pdf"):
    """Create a PDF with approximately 200,000 words"""
    
    # Create the document
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    
    # Generate content
    print("Generating content...")
    content_text = generate_test_content(200000)
    
    # Split into chunks for better PDF formatting
    words = content_text.split()
    chunk_size = 500  # words per paragraph
    
    story = []
    
    # Add title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
    )
    story.append(Paragraph("200K Word Test Document", title_style))
    story.append(Spacer(1, 12))
    
    print("Creating PDF paragraphs...")
    
    # Add content in chunks
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        para = Paragraph(chunk, normal_style)
        story.append(para)
        story.append(Spacer(1, 12))
        
        # Progress indicator
        if i % 10000 == 0:
            print(f"Processed {i} words...")
    
    # Build PDF
    print("Building PDF...")
    doc.build(story)
    
    # Calculate actual word count
    actual_words = len(words)
    print(f"PDF created: {filename}")
    print(f"Actual word count: {actual_words:,}")
    print(f"File size: {os.path.getsize(filename) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    # Install required package if not already installed
    try:
        import reportlab
    except ImportError:
        print("Installing reportlab...")
        os.system("pip install reportlab")
        import reportlab
    
    create_200k_word_pdf()