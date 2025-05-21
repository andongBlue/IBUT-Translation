# Model Interface

class LLMModel:
    """
    Large Language Model Interface Class
    
    This class provides an interface for interacting with large language models,
    which can be implemented according to the actual model being used.
    For example, it can implement different interfaces like OpenAI, Anthropic, local models, etc.
    """
    
    def __init__(self, model_name="gpt-3.5-turbo", api_key=None):
        """
        Initialize model interface
        
        Args:
            model_name: Model name
            api_key: API key (if needed)
        """
        self.model_name = model_name
        self.api_key = api_key
    
    def generate(self, prompt):
        """
        Generate text
        
        Args:
            prompt: Prompt text
            
        Returns:
            str: Generated text
        """
        import openai
        from openai import OpenAI
        
        # customize any LLM implementation here
        client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
        # client = OpenAI(
        #         # This is the default and can be omitted
        #         api_key = self.api_key
        #     )
        print(f"\n[Model name] model: {self.model_name}\Prompt: {prompt[:100]}...")
        
        try:
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specializing in language understanding and translation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API call error: {str(e)}")
            return f"Error: {str(e)}"
    
    def _extract_sentence(self, prompt):
        """Extract sentence from prompt"""
        if "Sentence:" in prompt:
            parts = prompt.split("Sentence: ")
            if len(parts) > 1:
                sentence_part = parts[1].split("\n")[0].strip()
                return sentence_part
        return ""
    
    def _mock_source_understanding(self, prompt):
        """Mock source language understanding generation"""
        sentence = self._extract_sentence(prompt)
        if "climate change" in sentence.lower():
            return """Key Concepts:
1. Climate Change - Long-term changes in Earth's climate system
2. Global Warming - The phenomenon of rising average temperatures on Earth

Important Terms:
1. Greenhouse Gases - Gases that absorb and emit infrared radiation
2. Carbon Footprint - The amount of carbon dioxide emissions produced by human activities

Term Explanation:
Greenhouse gases are gases that can absorb infrared radiation emitted from Earth's surface and re-radiate it back to the atmosphere, such as carbon dioxide and methane. The increase of these gases in the atmosphere enhances the greenhouse effect, leading to global warming.

Related Examples:
Since the Industrial Revolution, human activities have caused a significant increase in atmospheric carbon dioxide concentration, which is one of the main causes of global warming."""
        else:
            return """Key Concepts:
1. [Source Language Key Concept 1]
2. [Source Language Key Concept 2]

Important Terms:
1. [Source Language Term 1]
2. [Source Language Term 2]

Term Explanation:
[Source Language Term Explanation]

Related Examples:
[Source Language Example]"""
    
    def _mock_target_understanding(self, prompt):
        """Mock target language understanding generation"""
        sentence = self._extract_sentence(prompt)
        if "climate change" in sentence.lower():
            return """Key Concepts:
1. Climate Change - Long-term changes in Earth's climate system
2. Global Warming - The phenomenon of rising average temperatures on Earth

Important Terms:
1. Greenhouse Gases - Gases that absorb and emit infrared radiation
2. Carbon Footprint - The amount of carbon dioxide emissions produced by human activities

Term Explanation:
Greenhouse gases are gases that can absorb infrared radiation emitted from Earth's surface and re-radiate it back to the atmosphere, such as carbon dioxide and methane. The increase of these gases in the atmosphere enhances the greenhouse effect, leading to global warming.

Related Examples:
Since the Industrial Revolution, human activities have caused a significant increase in atmospheric carbon dioxide concentration, which is one of the main causes of global warming."""
        else:
            return """Key Concepts:
1. [Target Language Key Concept 1]
2. [Target Language Key Concept 2]

Important Terms:
1. [Target Language Term 1]
2. [Target Language Term 2]

Term Explanation:
[Target Language Term Explanation]

Related Examples:
[Target Language Example]"""
    
    def _mock_alignment_judgment(self, prompt):
        """Mock alignment judgment"""
        # Simple simulation: returns inconsistent on first call, consistent on subsequent calls
        if "greenhouse gases" in prompt.lower() and "Greenhouse Gases" in prompt:
            return """Consistency: True
Source Language Feedback: None
Target Language Feedback: None"""
        else:
            return """Consistency: False
Source Language Feedback: Source language understanding lacks explanation of 'Carbon Neutrality' concept, suggest adding.
Target Language Feedback: Target language understanding of 'Carbon Neutrality' is not detailed enough, inconsistent with source language understanding."""
    
    def _mock_refined_understanding(self, prompt):
        """Mock refined understanding"""
        if "source language" in prompt.lower():
            return """Key Concepts:
1. [Refined Source Language Key Concept 1]
2. [Refined Source Language Key Concept 2]
3. Carbon Neutrality - Achieving a balance between carbon emissions and absorption through emission reduction and carbon sinks

Important Terms:
1. [Refined Source Language Term 1]
2. [Refined Source Language Term 2]

Term Explanation:
[Refined Source Language Term Explanation]
Carbon neutrality refers to offsetting one's own carbon dioxide emissions through methods such as planting trees and reducing energy consumption, achieving a balance between carbon dioxide emissions and absorption.

Related Examples:
[Refined Source Language Example]"""
        else:
            return """Key Concepts:
1. [Refined Target Language Key Concept 1]
2. [Refined Target Language Key Concept 2]
3. Carbon Neutrality - Achieving a balance between carbon emissions and absorption through emission reduction and carbon sinks

Important Terms:
1. [Refined Target Language Term 1]
2. [Refined Target Language Term 2]

Term Explanation:
[Refined Target Language Term Explanation]
Carbon neutrality refers to offsetting one's own carbon dioxide emissions through methods such as planting trees and reducing energy consumption, achieving a balance between carbon dioxide emissions and absorption.

Related Examples:
[Refined Target Language Example]"""
    
    def _mock_translation(self, prompt):
        """Mock translation result"""
        sentence = self._extract_sentence(prompt)
        if "climate change" in sentence.lower():
            return "Climate change is one of the most serious challenges facing humanity today. We need to take immediate action to reduce greenhouse gas emissions and achieve carbon neutrality."
        else:
            return "[Translation Result]"
