# IBUT主程序演示

from model import LLMModel
from ibut import IBUT
import time

def print_separator(title):

    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def print_understanding(title, understanding):
    
    print(f"\n{title}:")
    print("-" * 50)
    print(understanding)
    print("-" * 50)

def inference_ibut_process(sentence):
    
    print_separator(f"IBUT Translation Demo: '{sentence}'")
    model = LLMModel(model_name="gpt-3.5-turbo")
    ibut_translator = IBUT(model, max_iterations=3)
    
    print_separator("Step 1: Understanding Generation")
    source_understanding, target_understanding = ibut_translator.generate_understanding(sentence)
    
    print_understanding("Source Understanding", source_understanding)
    print_understanding("Target Understanding", target_understanding)
    
    print_separator("Step & 3: Alignment Judgment & Iterative Refinement")
    
    current_source = source_understanding
    current_target = target_understanding
    
    for i in range(ibut_translator.max_iterations):
        print(f"\iteration {i+1}/{ibut_translator.max_iterations}:")
        
        print("\Alignment...")
        
        is_aligned, source_feedback, target_feedback = ibut_translator.alignment_judgment(
            sentence, current_source, current_target
        )
        
        
        if is_aligned:
            print("Bilingual understanding is aligned, no further optimization needed.")
            break
        
        if source_feedback:
            print(f"\Source Feedback: {source_feedback}")
        if target_feedback:
            print(f"\Target Feedback: {target_feedback}")
        
        current_source = ibut_translator._refine_understanding(
            sentence, current_source, source_feedback, is_source=True
        )
        current_target = ibut_translator._refine_understanding(
            sentence, current_target, target_feedback, is_source=False
        )
        
        print_understanding("Refined Source Understanding", current_source)
        print_understanding("Refined Target Understanding", current_target)
        
        time.sleep(1)
    
    print_separator("Step 4: Understanding-Based Translation")
    
    translation = ibut_translator.understanding_based_translation(
        sentence, current_source, current_target
    )
    
    print("-" * 50)
    print(translation)
    print("-" * 50)
    
    return translation

def main():
    """main"""
    
    test_cases = [
        "气候变化是当今人类面临的最严峻挑战之一，我们需要立即采取行动减少温室气体排放，实现碳中和。",
        "人工智能技术正在迅速发展，它将彻底改变我们的生活和工作方式。",
        "可持续发展要求我们在满足当代人需求的同时，不损害后代人满足其需求的能力。"
    ]
    
    for i, sentence in enumerate(test_cases):
        inference_ibut_process(sentence)
        
        if i < len(test_cases) - 1:
            time.sleep(2)
    
    print_separator("Ending")

if __name__ == "__main__":
    main()