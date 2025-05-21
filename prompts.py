# Prompt Templates

class TranslationPrompts:
    """Translation-related prompt templates"""
    
    # Source language understanding prompt
    SOURCE_UNDERSTANDING = """
Please analyze the contextual understanding of the following sentence in the source language.

Sentence: {sentence}

Please provide the following information:
1. Key concepts and their explanations
2. Important terms and their definitions
3. Detailed explanation of terms
4. Related examples

Note: Please ensure the analysis is comprehensive and accurate.
"""
    
    # Target language understanding prompt
    TARGET_UNDERSTANDING = """
Please analyze the contextual understanding of the following sentence in the target language (English).

Sentence: {sentence}

Please provide the following information:
1. Key concepts and their explanations
2. Important terms and their definitions
3. Detailed explanation of terms
4. Related examples

Note: Please ensure the analysis is comprehensive and accurate.
"""
    
    # Alignment judgment prompt
    ALIGNMENT_JUDGMENT = """
Please evaluate the consistency between the following bilingual contextual understandings:

Source language understanding:
{source_understanding}

Target language understanding:
{target_understanding}

Please provide:
1. Consistency judgment (True/False)
2. Areas for improvement in source language understanding (if any)
3. Areas for improvement in target language understanding (if any)
"""
    
    # Refine source understanding prompt
    REFINE_SOURCE = """
Please optimize the source language understanding based on the following feedback:

Original understanding:
{original_understanding}

Feedback:
{feedback}

Please provide the complete refined understanding.
"""
    
    # Refine target understanding prompt
    REFINE_TARGET = """
Please optimize the target language understanding based on the following feedback:

Original understanding:
{original_understanding}

Feedback:
{feedback}

Please provide the complete refined understanding.
"""
    
    # Translation prompt
    TRANSLATION = """
Please translate this sentence based on the following bilingual contextual understanding:

Sentence: {sentence}

Source language understanding:
{source_understanding}

Target language understanding:
{target_understanding}

Please provide accurate English translation.
"""