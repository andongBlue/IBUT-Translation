# IBUT测试脚本

from model import LLMModel
from ibut import IBUT
import time
from langcodes import Language

import json

def print_separator(title):
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def evaluate_translation(source, translation, reference=None):

    
    result = {
        "source_length": len(source),
        "translation_length": len(translation),
        "length_ratio": len(translation) / len(source) if len(source) > 0 else 0,
    }
    
    # 检测关键词（示例）
    if "气候变化" in source and "climate change" in translation.lower():
        result["keyword_preservation"] = True
    elif "人工智能" in source and "artificial intelligence" in translation.lower():
        result["keyword_preservation"] = True
    elif "可持续发展" in source and "sustainable development" in translation.lower():
        result["keyword_preservation"] = True
    else:
        result["keyword_preservation"] = False
    
    # 如果有参考翻译，可以计算更多指标
    if reference:
        # 简单的词重叠率（实际应用中应使用更复杂的指标）
        source_words = set(source.lower().split())
        translation_words = set(translation.lower().split())
        reference_words = set(reference.lower().split())
        
        overlap_with_ref = len(translation_words.intersection(reference_words))
        result["reference_overlap"] = overlap_with_ref / len(reference_words) if reference_words else 0
    
    return result

def compare_with_baseline(sentence, ibut_translator, baseline_model):
    """    
    Args:
        sentence
        ibut_translator
        baseline_model
    
    Returns:
        dict: compared sresults 
    """
    print_separator(f"IBUT vs baseline: '{sentence[:30]}...'")
    
    print("\Acting Compare...")
    start_time = time.time()
    ibut_translation = ibut_translator.translate(sentence)
    ibut_time = time.time() - start_time
    
    # Baseline
    print("\nBaseline Translate...")
    baseline_prompt = f"Please translate the \n\n{sentence} to English."
    start_time = time.time()
    baseline_translation = baseline_model.generate(baseline_prompt)
    baseline_time = time.time() - start_time
    
    print("\Source:")
    print(sentence)
    print("\IBUT Result:")
    print(ibut_translation)
    print("\Baseline Result:")
    print(baseline_translation)
    
    ibut_eval = evaluate_translation(sentence, ibut_translation)
    baseline_eval = evaluate_translation(sentence, baseline_translation)
    
    comparison = {
        "source": sentence,
        "ibut_translation": ibut_translation,
        "baseline_translation": baseline_translation,
        "ibut_time": ibut_time,
        "baseline_time": baseline_time,
        "ibut_evaluation": ibut_eval,
        "baseline_evaluation": baseline_eval
    }
    
    print(json.dumps(comparison, indent=2, ensure_ascii=False))
    
    return comparison

def test_with_various_domains():
    
    model = LLMModel(model_name="gpt-3.5-turbo",api_key="")
    ibut_translator = IBUT(model, max_iterations=2)
    
    test_sentences = {
        "环境": "气候变化是当今人类面临的最严峻挑战之一，我们需要立即采取行动减少温室气体排放，实现碳中和。",
        "技术": "人工智能技术正在迅速发展，它将彻底改变我们的生活和工作方式。",
        "经济": "可持续发展要求我们在满足当代人需求的同时，不损害后代人满足其需求的能力。",
        "医疗": "新冠疫情凸显了全球卫生系统的脆弱性，各国需要加强合作以应对未来的公共卫生危机。",
        "教育": "远程教育在疫情期间得到了广泛应用，但它也暴露出数字鸿沟和教育不平等的问题。"
    }
    
    results = {}
    
    for domain, sentence in test_sentences.items():
        print(f"\n\Domain: {domain}")
        translation = ibut_translator.translate(sentence)
        
        print(f"Source Sentence: {sentence}")
        print(f"Translated Result: {translation}")
        
        eval_result = evaluate_translation(sentence, translation)
        results[domain] = {
            "source": sentence,
            "translation": translation,
            "evaluation": eval_result
        }
        
        time.sleep(1)
    
    return results

def test_iteration_impact():

    
    test_sentence = "气候变化是当今人类面临的最严峻挑战之一，我们需要立即采取行动减少温室气体排放，实现碳中和。"
    
    results = {}
    
    for iterations in [0, 1, 2, 3]:
        print(f"\n\niteration nums: {iterations}")
        
        model = LLMModel(model_name="gpt-3.5-turbo")
        ibut_translator = IBUT(model, max_iterations=iterations)
        
        translation = ibut_translator.translate(test_sentence)
        
        print(f"源语句: {test_sentence}")
        print(f"翻译结果: {translation}")
        
        eval_result = evaluate_translation(test_sentence, translation)
        results[f"iterations_{iterations}"] = {
            "translation": translation,
            "evaluation": eval_result
        }
        
        time.sleep(1)
    
    return results

def read_common():
    data = []
    # path = "./data/common"
    path = "/Users/chenandong/Documents/哈工大2024-2025/投稿/IBUT生成能力与翻译/code_submitted/data/common"
    src_path = f"{path}/common.zh"
    tgt_path = f"{path}/common.en"
    src_data = [line.strip() for line in open(src_path, "r", encoding="utf-8")]
    tgt_data = [line.strip() for line in open(tgt_path, "r", encoding="utf-8")]

    testset = [{"src_lang":"Chinese", "tgt_lang": "English", "src":src, "tgt":tgt} for src, tgt in zip(src_data, tgt_data)]
    data.extend(testset)
    
    return data
    
def main():
    
    model = ""
    api_key = ""
    # model settings
    max_iterations=1
    model = LLMModel(model_name=model, api_key=api_key)

    # model = LLMModel(model_name="gpt-3.5-turbo")
    ibut_translator = IBUT(model, max_iterations=max_iterations)
    
    # test_sentence = "发明的是一个机器人"
    
    test_data = read_common()
    output_file = '/Users/chenandong/Documents/哈工大2024-2025/投稿/IBUT生成能力与翻译/code_submitted/result/deepseek-common.jsonl'
    with open(output_file, 'a', encoding='utf-8') as file:

        for item in test_data:
            src_lang = item["src_lang"]
            tgt_lang = item["tgt_lang"]
            src = item["src"]
            tgt = item["tgt"]
            ibut_translation = ibut_translator.translate(src)
            
            output_dict = {"src": src,"tgt": tgt,"hyp": ibut_translation}
            line = json.dumps(output_dict, ensure_ascii=False) + "\n"
            file.write(line)
            file.flush()

         
    # ibut_translation = ibut_translator.translate(test_sentence)
    
    print(f"The result of IBUT: {ibut_translation}")
    # comparison = compare_with_baseline(test_sentence, ibut_translator, model)
    
    return {
        # "domain_results": domain_results,
        "iteration_results": ibut_translation
    }

if __name__ == "__main__":
    main()