from botocore.exceptions import ClientError
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai import Stream
from structure import RequestInput, ResponseOutput, ServiceProvider, Region
from Utilities import Utilities
import logging
import openai
import tiktoken
import time
logging.basicConfig(level=logging.INFO)

class StreamingRequestHandler:
    def __init__(self, provider:ServiceProvider, region:Region = Region.Global):        
        self.provider = provider
        self.client = Utilities.getClient(provider, region)
        self.encoder = tiktoken.get_encoding("cl100k_base")
        
    def score(self, req:RequestInput) -> ResponseOutput:
        model_version:str = Utilities.get_model_version(req.model_version, self.provider)
        if model_version is None:
            return None
        back_off = 5.0
        while True:
            try:
                samples = []
                finish_reason:str = None
                byteTimes = []

                inputmessage = [
                    {
                        "role": "user",
                        "content": req.Prompt,
                    },
                ]

                if req.image_url != None:
                    inputmessage = [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": req.Prompt,
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": req.image_url
                                    }
                                }
                            ]
                        }
                    ]

                start = start_for_ttlt = time.time()        
                response:Stream[ChatCompletionChunk] = self.client.chat.completions.create(
                    model=model_version,
                    messages=inputmessage,
                    max_tokens=req.max_token,
                    stream=req.stream,
                )

                for chunk in response:
                    if not chunk.choices:
                        continue
                    choice = chunk.choices[0]
                    if choice.delta.content is None:
                        finish_reason = choice.finish_reason
                        break
                    elif choice.delta.role is None:
                        end = time.time()
                        samples.append(choice.delta.content)
                        byteTimes.append(end-start)
                        start=end

                ttft = byteTimes[0]
                ttlt = end-start_for_ttlt
                ttbt = (ttlt-ttft)/len(samples)

                ttft = '%.6f'%(ttft)
                #tbt = ['%.6f'%(bt) for bt in byteTimes[1:]]
                ttlt = '%.6f'%(ttlt)
                ttbt = '%.6f'%(ttbt)

                prompt_encoded = self.encoder.encode(req.Prompt)
                samples_str = ' '.join(samples)
                samples_str = ' '.join(samples_str.splitlines())
                samples_str = samples_str.replace('\t', ' ')
                if req.image_url != None:
                    logging.info(samples_str)
                result = ResponseOutput(samples_str, ttft, [ttbt], ttbt, ttlt, finish_reason, len(prompt_encoded), len(samples), 0) #TODO: calculate edit distance
                return result
            except openai.RateLimitError as e:
                logging.info(f"A 429 status code was received; backing off {back_off=} {e}")
                time.sleep(back_off)
                back_off = back_off * 1.5

class AWSStreamingRequestHandler(StreamingRequestHandler):
    def __init__(self, region:Region):
        super().__init__(ServiceProvider.AWS, region)

    def score(self, req:RequestInput) -> ResponseOutput:
        model_version:str = Utilities.get_model_version(req.model_version, self.provider)
        if model_version is None:
            return None
        back_off = 5.0
        while True:
            try:
                samples = []
                finish_reason:str = None
                byteTimes = []

                inputmessage = [
                    {
                        "role": "user",
                        "content": [{"text":  req.Prompt}],
                    },
                ]

                start = start_for_ttlt = time.time()
                response = self.client.converse_stream(
                    modelId=model_version,
                    messages=inputmessage,
                    inferenceConfig={
                        "maxTokens": req.max_token,
                    }
                )

                for chunk in response["stream"]:
                    if "contentBlockDelta" in chunk:
                        text = chunk["contentBlockDelta"]["delta"]["text"]
                        end = time.time()
                        samples.append(text)
                        byteTimes.append(end-start)
                        start=end
                    elif "messageStop" in chunk:
                        finish_reason = chunk["messageStop"]["stopReason"]
                    elif "metadata" in chunk:
                        inputTokens = chunk["metadata"]["usage"]["inputTokens"]
                        outputTokens = chunk["metadata"]["usage"]["outputTokens"]

                ttft = byteTimes[0]
                ttlt = end-start_for_ttlt
                ttbt = (ttlt-ttft)/outputTokens

                ttft = '%.6f'%(ttft)
                #tbt = ['%.6f'%(bt) for bt in byteTimes[1:]]
                ttlt = '%.6f'%(ttlt)
                ttbt = '%.6f'%(ttbt)

                samples_str = ' '.join(samples)
                samples_str = ' '.join(samples_str.splitlines())
                samples_str = samples_str.replace('\t', ' ')
                if req.image_url != None:
                    logging.info(samples_str)
                result = ResponseOutput(samples_str, ttft, [ttbt], ttbt, ttlt, finish_reason, inputTokens, outputTokens, 0) #TODO: calculate edit distance
                return result
            except (ClientError, Exception) as e:
                logging.error(repr(e))
                time.sleep(back_off)
                back_off = back_off * 1.5