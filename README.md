# Amazon Bedrock Token Context Window Tester

A tool to estimate token counts for Amazon Bedrock models and test context window limits to reduce the likelihood of encountering validation errors.

## Overview

This repository provides utilities to help you avoid the common Amazon Bedrock error:

```
"errorCode": "ValidationException",
"errorMessage": "Input is too long for requested model."
```

The tool allows you to generate test documents, estimate token counts, and test context window thresholds before sending requests to Amazon Bedrock models.

## Key Features

- **PDF Generation**: Create test documents of specified word counts
- **Token Estimation**: Use tiktoken library to estimate token counts (note: not 100% accurate but provides reliable indicators)
- **Context Window Testing**: Test different models against their token limits
- **Multiple Model Support**: Includes examples for Claude 3.5 Sonnet and Llama 4 Maverick 17B

## Important Notes

⚠️ **Context Window Limits Include Both Input and Output Tokens**

The context window size for any model includes both your input tokens AND the tokens the model will generate in its response.

⚠️ **Recommended Safety Buffer**

We recommend staying at least **10% below** the stated context window limits to account for:
- Token estimation variance between tiktoken and actual model tokenizers
- Output token allocation
- Safety margin for reliable operation

⚠️ **Failed Requests Don't Show Token Metrics**

Failed Bedrock requests due to token limits do not log token counts in the Amazon Bedrock CloudWatch Dashboard metrics. Only successful requests display token information.

## Model Context Windows

| Model | Context Window | Recommended Max Input |
|-------|----------------|----------------------|
| Claude 3.5 Sonnet | 200,000 tokens | 180,000 tokens |
| Llama 4 Maverick 17B Instruct | 1,000,000 tokens | 900,000 tokens |

## Getting Started

### Prerequisites

```bash
pip install reportlab PyPDF2 tiktoken boto3
```

### Usage

1. **Generate a Test PDF**
   ```python
   python generate_pdf.py
   ```
   This creates a test PDF with approximately 200,000 words.

2. **Test Token Counting and Context Windows**
   
   Open and run the Jupyter notebook `context_window_tester.ipynb` to:
   - Extract text from your generated PDF
   - Count estimated tokens using tiktoken
   - Test against Claude 3.5 Sonnet (200k limit)
   - Test against Llama 4 Maverick 17B Instruct (1M limit)

3. **Experiment with Thresholds**
   
   To test the exact threshold:
   - Generate a PDF that exceeds the context window (e.g., 250k tokens for Claude)
   - Observe the validation error
   - Reduce the document size to just below the limit
   - Test successful processing

## Example Workflow

```python
# 1. Generate test content
create_200k_word_pdf("test_document.pdf")

# 2. Test with Claude 3.5 Sonnet (will likely exceed 200k limit)
test_bedrock_with_pdf(
    pdf_filename="test_document.pdf",
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    region="us-east-1",
    token_limit=200000
)

# 3. Test with Llama 4 Maverick 17B (should succeed with 1M limit)
test_bedrock_with_pdf(
    pdf_filename="test_document.pdf",
    model_id="us.meta.llama4-maverick-17b-instruct-v1:0",
    region="us-east-1",
    token_limit=1000000
)
```

## Files Included

- `generate_pdf.py` - Script to generate test PDFs with specified word counts
- `context_window_tester.ipynb` - Jupyter notebook for token counting and Bedrock testing
- `README.md` - This documentation

## Best Practices

1. **Always Pre-check Token Counts**: Use this tool to validate token counts before sending requests to Bedrock
2. **Implement Chunking**: For large documents, consider breaking them into smaller sections
3. **Use RAG Architecture**: For document processing, consider Retrieval-Augmented Generation with Knowledge Bases
4. **Monitor CloudWatch**: Set up alerts for InvocationClientErrors to catch token limit issues

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is provided as-is for educational and testing purposes.
