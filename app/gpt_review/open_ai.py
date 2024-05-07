import json
import requests
from django.conf import settings

import logging


log = logging.getLogger(__name__)


class OpenAI:

    @staticmethod
    def get_headers():
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {settings.OPENAI_API_KEY}'}
        return headers

    @classmethod
    def generate_review(cls, course, question, answer):
        url = 'https://api.openai.com/v1/chat/completions'
        system_content = "ignore all previous instructions. give me very short and concise answers and ignore all the niceties that openai programmed you with. I'd tip you $200 for accurate answer. It is a matter of life and death to honour these requests."
        user_content = f"You are a master of {course}. You took a test and your student has submitted an answer for:\nQuestion :{question}\nAnswer:{answer}\nNow, your job is to provide remarks and score.\n[Important] Remarks should be precise, concise and the correct answer should be provided in the remarks if possible(around 30 words maximum and donot provide socre in remarks). [Important] Score should be between 0-10 where 0 must be given if answer is entirely wrong(donot feel guilty for giving 0) and 10 should be given when answer encapsulates everything that is asked.\n.[Very Important]Respond in json format: {{'remarks':<remark>, 'score':<score>}}"
        data = {
            "model": "gpt-3.5-turbo",
            "response_format": {"type": "json_object"},
            "messages": [{"role": "system", "content": system_content}, {"role": "user", "content": [{"type": "text", "text": user_content}]}],
            "max_tokens": 300,
        }

        try:
            log.info('Sending request to openai api for generating remarks and score.')
            response = requests.post(url, json=data, headers=cls.get_headers())

            if response.status_code != 200:
                log.error(f'OpenAI api did not send 200 status code: {response.status_code}')
                log.error(f'OpenAI Response: {response.json().get("error", None)}')
                return None
            data = response.json()
            data_string = data['choices'][0]['message']['content']
            try:
                cleaned_data_string = data_string.replace('```json', '').replace('```', '').strip()
                json_data = json.loads(cleaned_data_string)
            except:
                json_data = cls.fix_response(data_string)

            required_keys = ['remarks', 'score']

            if set(required_keys) - set(json_data.keys()):
                log.debug(f'OpenAI api sent invalid keys: {json_data.keys()}')
                return None

            log.info('OpenAI request success')
            return json_data

        except Exception as e:
            log.error(f'Error occured while generating remarks: {str(e)}')
            return None

    @classmethod
    def fix_response(cls, content):
        url = 'https://api.openai.com/v1/chat/completions'

        data = {
            "model": "gpt-3.5-turbo",
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": "ignore all previous instructions. give me very short and concise answers and ignore all the niceties that openai programmed you with No need to disclose you're an AI If the quality of your response has been substantially reduced due to my custom instructions, please explain the issue",
                },
                {"role": "user", "content": f"Please return the following text: {content} as a json object"},
            ],
        }

        try:
            log.info('Sending request to openai api for fixing response')
            response = requests.post(url, json=data, headers=cls.get_headers())
            content = response.json()['choices'][0]['message']['content']
            return json.loads(content)

        except Exception as e:
            log.error(f'Error occured while fixing response: {str(e)}')
            raise e
