import os
import requests
import faiss
import numpy as np
import PyPDF2
import re
from django.conf import settings
import json
import uuid
from pathlib import Path
import time

class DocumentProcessor:
    def __init__(self):
        self.vector_dim = 1536
        self.index_path = Path(settings.BASE_DIR) / "faiss_index"
        self.index_path.mkdir(exist_ok=True)
    
    def _get_active_config(self):
        """获取当前激活的配置"""
        try:
            from .models import AIConfig
            active_config = AIConfig.objects.filter(is_active=True).first()
            
            if active_config and active_config.api_key:
                return {
                    'api_key': active_config.api_key,
                    'base_url': active_config.base_url.rstrip('/'),  # 移除末尾斜杠
                    'model_name': active_config.model_name,
                    'embedding_model': active_config.embedding_model,
                    'temperature': active_config.temperature,
                    'max_tokens': active_config.max_tokens,
                    'simulation_mode': False
                }
            else:
                api_key = os.getenv('AIHUBMIX_API_KEY')
                base_url = os.getenv('AIHUBMIX_BASE_URL')
                
                if not api_key or not base_url:
                    print("警告: 未找到AI配置，将使用模拟模式")
                    return {
                        'api_key': '',
                        'base_url': '',
                        'model_name': 'gpt-3.5-turbo',
                        'embedding_model': 'text-embedding-ada-002',
                        'temperature': 0.7,
                        'max_tokens': 2000,
                        'simulation_mode': True
                    }
                else:
                    return {
                        'api_key': api_key,
                        'base_url': base_url.rstrip('/'),
                        'model_name': 'gpt-3.5-turbo',
                        'embedding_model': 'text-embedding-ada-002',
                        'temperature': 0.7,
                        'max_tokens': 2000,
                        'simulation_mode': False
                    }
                    
        except Exception as e:
            print(f"加载AI配置失败: {e}, 使用环境变量")
            api_key = os.getenv('AIHUBMIX_API_KEY')
            base_url = os.getenv('AIHUBMIX_BASE_URL')
            
            return {
                'api_key': api_key or '',
                'base_url': (base_url or '').rstrip('/'),
                'model_name': 'gpt-3.5-turbo',
                'embedding_model': 'text-embedding-ada-002',
                'temperature': 0.7,
                'max_tokens': 2000,
                'simulation_mode': not (api_key and base_url)
            }
    
    def extract_text_from_pdf(self, pdf_path):
        """从PDF提取文本"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"PDF提取错误: {e}")
            return ""
    
    def clean_text(self, text):
        """清洗文本"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\u4e00-\u9fff，。！？；：""''（）《》]', '', text)
        return text.strip()
    
    def chunk_text(self, text, chunk_size=400):
        """文本分段"""
        sentences = re.split(r'[。！？]', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) < chunk_size:
                current_chunk += sentence + "。"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + "。"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def get_embeddings(self, texts):
        """获取文本嵌入向量"""
        config = self._get_active_config()
        
        if config['simulation_mode']:
            print("模拟模式: 生成随机嵌入向量")
            return [np.random.rand(self.vector_dim).tolist() for _ in texts]
            
        try:
            headers = {
                "Authorization": f"Bearer {config['api_key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": config['embedding_model'],
                "input": texts
            }
            
            print(f"调用嵌入API: {config['base_url']}/embeddings")
            response = requests.post(
                f"{config['base_url']}/embeddings",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'data' in result:
                    return [item['embedding'] for item in result['data']]
                else:
                    print(f"嵌入API响应格式异常: {result}")
                    return None
            else:
                print(f"嵌入API错误: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"获取embedding失败: {e}")
            return None
    
    def create_faiss_index(self, document_id, chunks):
        """创建FAISS向量索引"""
        if not chunks:
            return False
        
        embeddings = self.get_embeddings(chunks)
        if not embeddings:
            return False
        
        index = faiss.IndexFlatIP(self.vector_dim)
        embeddings_np = np.array(embeddings).astype('float32')
        index.add(embeddings_np)
        
        index_file = self.index_path / f"{document_id}.index"
        chunks_file = self.index_path / f"{document_id}_chunks.json"
        
        faiss.write_index(index, str(index_file))
        with open(chunks_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False)
        
        return True
    
    def search_similar_chunks(self, document_id, query, top_k=3):
        """搜索相似文本片段"""
        try:
            index_file = self.index_path / f"{document_id}.index"
            chunks_file = self.index_path / f"{document_id}_chunks.json"
            
            if not index_file.exists() or not chunks_file.exists():
                return []
            
            index = faiss.read_index(str(index_file))
            with open(chunks_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            query_embedding = self.get_embeddings([query])
            if not query_embedding:
                return []
            
            query_np = np.array(query_embedding).astype('float32')
            scores, indices = index.search(query_np, top_k)
            
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(chunks):
                    results.append({
                        'text': chunks[idx],
                        'score': float(score)
                    })
            
            return results
            
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def call_llm_api(self, prompt, temperature=None, max_tokens=None):
        """调用LLM API - 专门为AIHubMix优化"""
        config = self._get_active_config()
        
        temp = temperature if temperature is not None else config['temperature']
        tokens = max_tokens if max_tokens is not None else config['max_tokens']
        
        if config['simulation_mode']:
            print("模拟模式: 生成模拟AI响应")
            time.sleep(2)
            
            if "总结要点" in prompt:
                return self._generate_mock_summary()
            elif "详细分析" in prompt:
                return self._generate_mock_analysis()
            elif "出题" in prompt or "题目" in prompt:
                return self._generate_mock_questions()
            else:
                return "这是AI生成的模拟响应。请配置AI API密钥以获取真实结果。"
        
        try:
            # AIHubMix使用OpenAI兼容格式
            headers = {
                "Authorization": f"Bearer {config['api_key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": config['model_name'],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temp,
                "max_tokens": tokens,
                "stream": False
            }
            
            print(f"调用AIHubMix API: {config['base_url']}/chat/completions")
            print(f"使用模型: {config['model_name']}")
            
            response = requests.post(
                f"{config['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            print(f"API响应状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"API响应: {result}")
                
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    return f"API响应格式异常: {result}"
            else:
                error_text = response.text
                print(f"API错误响应: {error_text}")
                
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error']
                        if isinstance(error_msg, dict) and 'message' in error_msg:
                            return f"AIHubMix API错误: {error_msg['message']}"
                        else:
                            return f"AIHubMix API错误: {error_msg}"
                    else:
                        return f"AIHubMix API错误: {error_text}"
                except:
                    return f"AIHubMix API错误: {error_text}"
                
        except requests.exceptions.Timeout:
            return "AIHubMix API请求超时，请稍后重试"
        except requests.exceptions.ConnectionError:
            return "无法连接到AIHubMix API，请检查网络连接"
        except Exception as e:
            return f"调用AIHubMix API失败: {str(e)}"
    
    def _generate_mock_summary(self):
        """生成模拟总结"""
        return """## 主要内容概述
这是一个示例文档的总结。文档主要讨论了现代技术对社会的影响。

## 关键要点
1. 技术发展迅速改变了人们的生活方式
2. 数字化转型已成为企业发展的必然趋势
3. 人工智能在各行各业都有广泛应用
4. 数据安全和个人隐私保护变得日益重要

## 重要结论
技术发展带来了巨大机遇，但也伴随着挑战，需要平衡创新与规范。"""

    def _generate_mock_analysis(self):
        """生成模拟分析"""
        return """## 内容深度解析
文档从多个角度分析了技术发展的影响，包括经济、社会和文化层面。

## 核心观点分析
1. **技术驱动变革**: 文档强调技术是推动社会进步的主要动力
2. **数字化转型**: 企业必须适应数字化趋势以保持竞争力
3. **伦理考量**: 技术创新需要与伦理规范相结合

## 逻辑结构分析
文档采用总分总结构，先提出总体观点，然后分点论述，最后总结升华。

## 价值与意义
本文为理解技术发展趋势提供了重要参考，对政策制定和企业战略具有指导意义。"""

    def _generate_mock_questions(self):
        """生成模拟题目"""
        return """## 选择题（5道）
1. 技术发展的主要驱动力是什么？
   A. 市场需求
   B. 政策支持
   C. 科技创新
   D. 资本投入
   正确答案：C

2. 数字化转型对企业意味着什么？
   A. 增加成本
   B. 提高效率
   C. 减少员工
   D. 降低质量
   正确答案：B

## 判断题（3道）
1. 人工智能可以完全替代人类工作。 (错误)
2. 数据安全是数字化时代的重要议题。 (正确)
3. 技术发展只会带来正面影响。 (错误)

## 简答题（2道）
1. 请简述数字化转型的三个主要优势。
   参考答案：提高效率、优化流程、创新业务模式

## 填空题（3道）
1. 技术创新的核心是__创造性思维__。
2. 数字化转型的关键在于__数据驱动__。
3. 人工智能的基础是__算法和算力__。"""

    def process_document(self, document_id, pdf_path, task_type):
        """处理文档的主要函数"""
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return "无法从PDF提取文本"
        
        cleaned_text = self.clean_text(text)
        chunks = self.chunk_text(cleaned_text)
        
        index_file = self.index_path / f"{document_id}.index"
        if not index_file.exists():
            if not self.create_faiss_index(document_id, chunks):
                return "创建向量索引失败"
        
        if task_type == "summary":
            prompt = self._create_summary_prompt(chunks)
        elif task_type == "analysis":
            prompt = self._create_analysis_prompt(chunks)
        elif task_type == "questions":
            prompt = self._create_questions_prompt(chunks)
        else:
            return "未知的任务类型"
        
        result = self.call_llm_api(prompt)
        return result
    
    def _create_summary_prompt(self, chunks):
        """创建总结要点prompt"""
        context = "\n".join([f"{i+1}. {chunk}" for i, chunk in enumerate(chunks[:10])])
        
        prompt = f"""请基于以下文档内容，生成一个结构化的总结要点：

{context}

请按照以下格式输出：
## 主要内容概述
[简要概述文档的核心内容]

## 关键要点
1. [要点1]
2. [要点2]
3. [要点3]
...

## 重要结论
[总结文档的主要结论或建议]

请确保要点清晰、有条理，涵盖文档的核心信息。"""
        return prompt
    
    def _create_analysis_prompt(self, chunks):
        """创建详细分析prompt"""
        context = "\n".join([f"{i+1}. {chunk}" for i, chunk in enumerate(chunks[:15])])
        
        prompt = f"""请对以下文档内容进行详细分析：

{context}

请按照以下结构进行分析：
## 内容深度解析
[对文档内容进行深入分析和解读]

## 核心观点分析
[分析文档中的主要观点和论据]

## 逻辑结构分析
[分析文档的组织结构和逻辑关系]

## 价值与意义
[分析文档的价值、意义和潜在应用]

请提供深入、专业的分析，突出文档的独特见解和价值。"""
        return prompt
    
    def _create_questions_prompt(self, chunks):
        """创建出题prompt"""
        context = "\n".join([f"{i+1}. {chunk}" for i, chunk in enumerate(chunks[:12])])
        
        prompt = f"""基于以下文档内容，请创建多种题型的测试题目：

{context}

请创建以下类型的题目：

## 选择题（5道）
1. [题目]
   A. [选项A]
   B. [选项B]
   C. [选项C]
   D. [选项D]
   正确答案：[正确选项]

## 判断题（3道）
1. [陈述] (正确/错误)
2. [陈述] (正确/错误)
3. [陈述] (正确/错误)

## 简答题（2道）
1. [问题]
   [参考答案要点]

## 填空题（3道）
1. [包含空格的句子]，正确答案：[填空内容]

请确保题目覆盖文档的核心内容，难度适中，并包含正确答案。"""
        return prompt

def get_processor():
    """获取新的处理器实例"""
    return DocumentProcessor()