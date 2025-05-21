# IBUT: Iterative Bilingual Understanding Translation
from langcodes import Language

class IBUT:
    """
    IBUT (Iterative Bilingual Understanding Translation) Implementation Class
    
    1. Understanding Generation
    2. Alignment Judgment
    3. Iterative Refinement
    4. Understanding-Based Translation
    """
    
    def __init__(self, llm_model, max_iterations=3):
        """
        Initialize IBUT translation system
        
        Args:
            llm_model: Large language model for generating understanding and translation
            max_iterations: Maximum number of iterations, default is 3
        """
        self.model = llm_model
        self.max_iterations = max_iterations
    
    def generate_understanding(self, source_sentence,direction="zh-en"):
        """
        Generate contextual understanding for source and target languages
        
        Args:
            source_sentence: Source language sentence
            
        Returns:
            tuple: (source understanding, target understanding)
        """
        source_lang, target_lang = direction.split("-")
        source_lang = Language.make(language=source_lang).display_name()
        target_lang = Language.make(language=target_lang).display_name()

        # Generate source language contextual understanding
        source_understanding = self._generate_source_understanding(source_sentence,source_lang)
        
        # Generate target language contextual understanding
        target_understanding = self._generate_target_understanding(source_sentence,target_lang)
        
        return source_understanding, target_understanding
    
    def _generate_source_understanding(self, source_sentence,source_lang):
        """
        Generate source language contextual understanding
        
        Args:
            source_sentence: Source language sentence
            
        Returns:
            str: Source language contextual understanding
        """
        # Call LLM to generate source language contextual understanding
        # In actual implementation, appropriate prompts should be used to guide LLM
        prompt = self._create_source_understanding_prompt(source_sentence,source_lang)
        source_understanding = self.model.generate(prompt)
        return source_understanding
    
    def _generate_target_understanding(self, source_sentence,target_lang):
        # Call LLM to generate target language contextual understanding
        prompt = self._create_target_understanding_prompt(source_sentence,target_lang)
        target_understanding = self.model.generate(prompt)
        return target_understanding
    
    def _create_source_understanding_prompt(self, source_sentence,source_lang):
        # Prompts should be adjusted based on specific language pairs and tasks
        prompt = f"""Please fully understand the meaning of the following {source_lang} text and describe your understanding of key concepts, definitions, examples, and explanations of specific terms related to the translation task in {source_lang}:
        
        source_sentence: {source_sentence}
        """
        return prompt
    
    def _create_target_understanding_prompt(self, source_sentence,target_lang):
        # Prompts should be adjusted based on specific language pairs and tasks
        prompt = f"""Please fully understand the meaning of the following {target_lang} text and describe your understanding of key concepts, definitions, examples, and explanations of specific terms related to the translation task in {target_lang}:
        
        source_sentence: {source_sentence}
        """
        return prompt
    
    def alignment_judgment(self, source_sentence, source_understanding, target_understanding,direction):
        # Call LLM as judgment agent (JA) to evaluate consistency
        source_lang, target_lang = direction.split("-")

        source_lang = Language.make(language=source_lang).display_name()
        target_lang = Language.make(language=target_lang).display_name()

        
        prompt = self._create_alignment_judgment_prompt(source_sentence, source_understanding, target_understanding,direction)
        judgment_result = self.model.generate(prompt)
        
        if "True" in judgment_result:
            prompt_source = self._create_alignment_judgment_prompt_source_2(source_sentence, source_understanding, judgment_result, source_lang)
            prompt_target = self._create_alignment_judgment_prompt_target_2(source_sentence, judgment_result, target_understanding, target_lang)
            is_aligned = False
            source_feedback = self.model.generate(prompt_source)
            target_feedback = self.model.generate(prompt_target)
        else:
            is_aligned = True
            source_feedback = ""
            target_feedback = ""
            
        return is_aligned, source_feedback, target_feedback
    
    def _create_alignment_judgment_prompt(self, source_sentence, source_understanding, target_understanding, direction):
        source_lang, target_lang = direction.split("-")
        source_lang = Language.make(language=source_lang).display_name()
        target_lang = Language.make(language=target_lang).display_name()

        prompt = f"""If you are a {source_lang} and {target_lang} linguist, determine whether provided source contextual understanding {source_understanding} and target contextual understanding {target_understanding}, based on the source sentence {source_sentence}, convey different key concepts, definitions, examples, and explanations of specific terms related to the translation task. If so, provide a "True" response; otherwise, give a "False" response."""
        
        return prompt
    
    def _create_alignment_judgment_prompt_source_2(self, source_sentence, source_understanding, judgment_result, language_type):
        prompt = f"""If you are a {language_type} linguist, based on the core meaning of the source sentence {source_sentence}, analyze the contextual understanding {judgment_result}. Generate verbal feedback in the language of {language_type} to correct any current errors in {source_understanding}."""
       
        return prompt
    
    def _create_alignment_judgment_prompt_target_2(self, source_sentence, judgment_result, target_understanding, language_type):
        prompt = f"""If you are a {language_type} linguist, based on the core meaning of the source sentence {source_sentence}, analyze the contextual understanding {judgment_result}. Generate verbal feedback in the language of {language_type} to correct any current errors in {target_understanding}."""
        
        return prompt
    
    def _parse_judgment_result(self, judgment_result):
        lines = judgment_result.strip().split('\n')
        is_aligned = 'True' in lines[0]
        
        source_feedback = ''
        target_feedback = ''
        
        if not is_aligned and len(lines) > 1:
            # Extract source language feedback
            for i, line in enumerate(lines):
                if 'Source feedback:' in line and i+1 < len(lines):
                    source_feedback = line.replace('Source feedback:', '').strip()
                    if not source_feedback and i+1 < len(lines):
                        source_feedback = lines[i+1].strip()
                
                if 'Target feedback:' in line and i+1 < len(lines):
                    target_feedback = line.replace('Target feedback:', '').strip()
                    if not target_feedback and i+1 < len(lines):
                        target_feedback = lines[i+1].strip()
        
        return is_aligned, source_feedback, target_feedback
    
    def iterative_refinement(self, source_sentence, source_understanding, target_understanding,direction):
        current_source_understanding = source_understanding
        current_target_understanding = target_understanding
        
        for iteration in range(self.max_iterations):
            # Perform alignment judgment
            is_aligned, source_feedback, target_feedback = self.alignment_judgment(
                source_sentence, current_source_understanding, current_target_understanding,direction
            )
            
            # If aligned, end iteration
            if is_aligned:
                break
            
            # Optimize source language understanding based on feedback
            current_source_understanding = self._refine_understanding(
                source_sentence, current_source_understanding, source_feedback,direction, is_source=True
            )
            
            # Optimize target language understanding based on feedback
            current_target_understanding = self._refine_understanding(
                source_sentence, current_target_understanding, target_feedback,direction, is_source=False
            )
        
        return current_source_understanding, current_target_understanding
    
    def _refine_understanding(self, source_sentence, current_understanding, feedback, direction, is_source=True):
        source_lang, target_lang = direction.split("-")
        source_lang = Language.make(language=source_lang).display_name()
        target_lang = Language.make(language=target_lang).display_name()
        language_type = source_lang if is_source else target_lang
        
        prompt = f"""If you are a linguist proficient in both {source_lang} and {target_lang}, based on the core meaning of the source sentence {source_sentence} and the opinions from {feedback}, further modify the current {current_understanding}."""
        
        refined_understanding = self.model.generate(prompt)
        return refined_understanding
    
    def understanding_based_translation(self, source_sentence, source_understanding, target_understanding,direction):
        prompt = self._create_translation_prompt(source_sentence, source_understanding, target_understanding,direction)
        translation = self.model.generate(prompt)
        return translation
    
    def _create_translation_prompt(self, source_sentence, source_understanding, target_understanding,direction):
        source_lang, target_lang = direction.split("-")
        source_lang = Language.make(language=source_lang).display_name()
        target_lang = Language.make(language=target_lang).display_name()

        prompt = f"""Based on {source_understanding} and {target_understanding}, translate the following text in {target_lang} without any explanation.
        
        source_sentence: {source_sentence}
        """
        return prompt
    
    def translate(self, source_sentence,direction="zh-en"):
        # 1. Understanding Generation
        source_understanding, target_understanding = self.generate_understanding(source_sentence,direction)
        print("understanding:", source_understanding)
        print("target_understanding:", target_understanding)
        print('1. Understanding generation completed')
        
        # 2 & 3. Alignment Judgment and Iterative Refinement
        refined_source_understanding, refined_target_understanding = self.iterative_refinement(
            source_sentence, source_understanding, target_understanding, direction
        )
        print('refined_source_understanding:', refined_source_understanding)
        print('refined_target_understanding:', refined_target_understanding)
        print('2 & 3. Alignment judgment and iterative refinement completed')
        
        # 4. Understanding-Based Translation
        translation = self.understanding_based_translation(
            source_sentence, refined_source_understanding, refined_target_understanding,direction
        )
        print('4. Understanding-based translation completed')
        print('translation:', translation)
        return translation