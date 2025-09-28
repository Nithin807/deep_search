import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from app.config import *
from app.retrieval import Retrieval
from openai import OpenAI


class Generation:
    def __init__(self):
        self.retrieval = Retrieval()
        self.gpt_model = LLM_MODEL
        self.client = OpenAI()

    def generate_answer(self,query, top_k=5):
        contexts = self.retrieval.retrieve(query, top_k)
        context_text = "\n\n".join([f"Source: {src}, Chunk ID: {cid}\nContent: {text}" for _, src, cid, text in contexts])
        prompt = f"Use the following context to answer the question:\n\n{context_text}\n\nQuestion: {query}\nAnswer:"
        
        response = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Don't exceed more than 200 words."},
                {"role": "user", "content": prompt}
            ],
        )
        answer = response.choices[0].message.content.strip()
        return answer
    
    def generate_with_history(self,query,history_conversation,top_k=5):
        contexts = self.retrieval.retrieve(query, top_k)
        contexts_text = "\n\n".join([f"Source: {src}, Chunk ID: {cid}\nContent: {text}" for _, src, cid, text in contexts])
        user_prompts = f"Use the following context to answer the question:\n\n{contexts_text}\n\nQuestion: {query}\nAnswer:"
        messages = [{"role": "system", "content": "You are a helpful assistant. Don't exceed more than 200 words."}] + history_conversation + [{"role": "user", "content": user_prompts}]
        response = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=messages
        )
        answer = response.choices[0].message.content.strip()
        return answer
