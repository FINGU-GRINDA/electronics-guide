from enum import Enum

class Prompts(Enum):
    GENERATE_SECTION_CONTENT = """
    You are an expert in creating detailed and user-friendly project tutorials. Please generate content for the following section of a project tutorial:

    **Project Name:** {project}
    **Section Title:** {section}

    **Context from Previous Sections:**
    {history_text}

    **Content Requirements:**
    - Use clear and concise language that guides the user through each step.
    - Begin with a relevant and engaging header for the section title.
    - Include lists, bullet points, or steps where applicable for better readability.
    - For code sections, provide complete, fully functional, and well-commented code examples within triple backticks (```).
    - Ensure that the code is not truncated or incomplete. If the code is lengthy, break it into logical segments, but ensure each segment is fully functional and runnable on its own.
    - For wiring instructions, provide detailed, step-by-step written instructions, specifying each connection clearly without relying on circuit diagrams. Describe the wiring process using text only.
    - Ensure the content is formatted properly with appropriate Markdown syntax for headings, lists, and code blocks.
    - Reference relevant details from previous sections for continuity.
    - Tailor the content to be under 1000 words while covering all necessary information comprehensively.

    **Goal:** Provide actionable and easy-to-follow instructions that empower the user to complete this part of the project confidently.
    """

    GENERATE_SUMMARY = """
    Please provide a concise summary of the following content for the section "{section}" of the project "{project}". 
    The summary should be about 2-3 sentences long and capture the key points:

    {full_content}
    """

    PROVIDE_PROJECT_DETAILS = """
    Provide a Project Title and a very short description for this project: {project}
   
    -Ensure the content is formatted properly with appropriate Markdown syntax for headings
    
    """
