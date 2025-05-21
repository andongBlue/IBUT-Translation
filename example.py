# IBUT实际应用示例

from model import LLMModel
from ibut import IBUT
import os

def setup_openai_model():
   
    api_key = ""
    
    model = LLMModel(model_name="gpt-3.5-turbo", api_key=api_key)
    return model

def translate_with_ibut(sentence, source_lang="中文", target_lang="英文"):
    
    model = setup_openai_model()
    
    ibut_translator = IBUT(model, max_iterations=2)
    
    print(f"\Source Sentence({source_lang}): {sentence}")
    print(f"Translating{target_lang}...\n")
    
    translation = ibut_translator.translate(sentence)
    
    print(f"Transltion Results: ({target_lang}): {translation}\n")
    return translation

def batch_translate(sentences, source_lang="中文", target_lang="英文"):
    
    model = setup_openai_model()
    
    ibut_translator = IBUT(model, max_iterations=2)
    
    results = []
    
    print(f"\Translate {len(sentences)} numbers,  from{source_lang}to{target_lang}...\n")
    
    for i, sentence in enumerate(sentences):
        print(f"[{i+1}/{len(sentences)}] source : {sentence}")
        
        # 执行翻译
        translation = ibut_translator.translate(sentence)
        results.append(translation)
        
        print(f"Translation Results: {translation}\n")
    
    return results

def customize_ibut_parameters(sentence, max_iterations=3):

    model = setup_openai_model()
    
    ibut_translator = IBUT(model, max_iterations=max_iterations)
    
    print(f"\n iternation number: (max_iterations={max_iterations})")
    print(f"Source Sentence: {sentence}")
    
    # 执行翻译
    translation = ibut_translator.translate(sentence)
    
    print(f"Translation Result: {translation}\n")
    return translation

def main():
    
    
    sentence = "人工智能技术正在迅速发展，它将彻底改变我们的生活和工作方式。"
    translate_with_ibut(sentence)
    
    sentences = [
        "可持续发展要求我们在满足当代人需求的同时，不损害后代人满足其需求的能力。",
        "新冠疫情凸显了全球卫生系统的脆弱性，各国需要加强合作以应对未来的公共卫生危机。"
    ]
    batch_translate(sentences)
    
    # 示例3: 自定义参数
    sentence = "远程教育在疫情期间得到了广泛应用，但它也暴露出数字鸿沟和教育不平等的问题。"
    customize_ibut_parameters(sentence, max_iterations=1)
    
    print("\n===== Endings =====")

if __name__ == "__main__":
    main()