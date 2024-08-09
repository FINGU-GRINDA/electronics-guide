import re


def process_markdown(text: str) -> str:
    # Replace multiple periods followed by a space with a single period and a space
    text = re.sub(r'\.\s+', '. ', text)
    
    # Replace misplaced periods with nothing
    text = re.sub(r'\s*\.\s*', '. ', text)
    
    # Remove extra periods at the start of lines
    text = re.sub(r'^\.\s*', '', text, flags=re.MULTILINE)
    
    # Ensure proper spacing after punctuation
    text = re.sub(r'\.(\w)', r'. \1', text)
    
    # Handle newlines after headers and list items (without using look-behind)
    text = re.sub(r'(\*\*|:)(\S)', r'\1 \2', text)
    
    # Correctly format bullet points and lists
    text = re.sub(r'\n\*\s', '\n* ', text)
    text = re.sub(r'\n\d\.\s', '\n1. ', text)
    
    # Remove misplaced newlines before headers and list items
    text = re.sub(r'\n\s*\n\s*(?=\*\*|\*)', '\n', text)
    
    # Handle spacing after bullets and numbers
    text = re.sub(r'(\*\*|\*)\s+', r'\1 ', text)
    text = re.sub(r'(\d\.|\*)\s+', r'\1 ', text)
    
    # Ensure new paragraphs are separated properly
    text = text.replace("\n\n", "</p><p>").replace("\n", "<br>")
    
    return text