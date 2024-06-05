import openai
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

url = 'mongodb+srv://mnbv7952:hXHFetjGCo06jkTn@cluster0.marjbqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(url)
database = client['ad_storage']
collection = database['ad']

openai.api_key = 'sk-proj-FcANM0iFB2a3jX8EeirYT3BlbkFJT0Cy1RfqdxRjvHVLPuRc'

app = FastAPI()

class AdGenerator:
    def __init__(self, engine='gpt-3.5-turbo'):
        self.engine = engine

    def using_engine(self, prompt):
        system_instruction = 'assistant는 마케팅 문구 작성 도우미로 동작한다. user의 내용을 참고하여 마케팅 문구를 작성해라'
        messages = [{'role':'system', 'content': system_instruction},
                    {'role': 'user', 'content': prompt}]
        response = openai.chat.completions.create(model=self.engine, messages=messages)
        result = response.choices[0].message.content.strip()
        return result

    def generate(self, product_name, details, tone_and_manner):
        prompt = f'제품 이름: {product_name}\n주요 내용: {details}\n광고 문구의 스타일: {tone_and_manner} 위 내용을 참고하여 마케팅 문구를 만들어라'
        result = self.using_engine(prompt=prompt)
        return result

    def create(self, product_name, details, tone_and_manner, ad):
        new_ad = {
            '제품 이름': product_name,
            '주요 내용': details,
            '문구 느낌': tone_and_manner,
            '광고 문구': ad
        }
        collection.insert_one(new_ad)

class Product(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str

@app.post('/create_ad')
async def create_ad(product: Product):
    # print(product)
    ad_generator = AdGenerator()
    ad = ad_generator.generate(product_name=product.product_name,
                               details=product.details,
                               tone_and_manner=product.tone_and_manner)
    return {'ad': ad}

class Ad(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str
    ad: str

@app.post('/store_ad')
async def store_ad(product: Ad):
    ad_generator = AdGenerator()
    ad_list = ad_generator.create(product_name=product.product_name,
                                  details=product.details, tone_and_manner=product.tone_and_manner,
                                  ad=product.ad)
    print('저장 성공')

@app.get('/get_ad')
async def get_ad():
    ads = collection.find()
    result = []
    for ad in ads:
        result.append({
            '제품 이름': ad['제품 이름'],
            '주요 내용': ad['주요 내용'],
            '문구 느낌': ad['문구 느낌'],
            '광고 문구': ad['광고 문구']
        })
    return result