import argparse
from dataclasses import dataclass
from typing import Optional, List
from concurrent.futures import Future, ThreadPoolExecutor

import openai
from openai.types.chat import ChatCompletion
from PIL import Image
from io import BytesIO
import base64, time
from math import sqrt
import secrets

NO_CACHE = True

def img2bytes(img: Image.Image, max_bytes=500000):
    if (img.mode == "P"):
        img = img.convert("RGBA")
    if ("A" in img.mode):
        fmt = "PNG"
        kwa = {}
    else:
        fmt = "JPEG"
        kwa = {"quality": 90}
    w, h = img.size
    def to_bytes(ratio):
        w1, h1 = round(ratio*w), round(ratio*h)
        bio = BytesIO()
        img.resize((w1, h1), resample=Image.Resampling.LANCZOS).save(bio, format=fmt, **kwa)
        size = bio.tell()
        
        bio.seek(0)
        data = bio.read()

        bio.seek(0)
        
        return bio, data, size
    
    ratio = 1
    while (ratio*w>1 and ratio*h>1):
        bio, data, size = to_bytes(ratio)
        if (size<=max_bytes):
            return fmt, bio, data, size
        else:
            ratio = min(ratio*0.9, ratio*sqrt(max_bytes/size))

def img2b64url(img: Image.Image, max_bytes=500000):
    fmt, bio, data, size = img2bytes(img, max_bytes=max_bytes)

    if (fmt == "PNG"):
        mime = "image/png"
    elif (fmt == "JPEG"):
        mime = "image/jpeg"
    else:
        raise ValueError("Format="+str(fmt))

    b64 = base64.b64encode(data).decode("ascii")

    url = f"data:{mime};base64,{b64}"
    return url
def img2openai(img: Image.Image, max_bytes=500000):
    return {
        "type": "image_url",
        "image_url": {"url": img2b64url(img, max_bytes)}
    }
def b64url2img(b64):
    if (isinstance(b64, bytes)):
        b64 = b64.decode("ascii")
    if ("base64," in b64):
        b64 = b64.split("base64,")[-1]
    data = base64.b64decode(b64)
    buffer = BytesIO()
    buffer.write(data)
    buffer.seek(0)
    return Image.open(buffer)
@dataclass
class TestConfig:
    """llama-server 性能测试配置"""
    base_url: str = "http://localhost:8090"
    api_key: str = "llama"
    model: str = "llama"
    test_image: str = "./test.png"
    test_document: str = "./doc.txt"
    test_reading_prompt: str = "简单分析此附件"
    test_hello_prompt: str = "你好。"
    repeat: int = 5
    output: str = "result.md"


@dataclass
class TestConfig:
    """Llama服务器性能测试配置类"""
    base_url: str = "http://localhost:8090"
    api_key: str = "llama"
    model: str = "llama"
    test_image: str = "./test.png"
    test_document: str = "./doc.txt"
    test_reading_prompt: str = "简单分析此附件"
    test_hello_prompt: str = "你好。"
    repeat: int = 5
    parallel: int = 1
    output: str = "result.md"
    temperature: float = 0.0
    vision: bool = False
    max_completion_tokens: int = 512


def parse_args() -> TestConfig:
    """解析命令行参数并返回TestConfig实例"""
    parser = argparse.ArgumentParser(
        description="Llama服务器性能测试工具",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # 所有add_argument都在一行内完成，不换行
    parser.add_argument("--base_url", type=str, default="http://localhost:8090", help="服务器基础URL")
    parser.add_argument("--api_key", type=str, default="llama", help="API密钥（llama-server通常不检查）")
    parser.add_argument("--model", type=str, default="llama", help="模型名称（单模型实例通常不检查）")
    parser.add_argument("--test_image", type=str, default="./test.png", help="测试图像文件路径")
    parser.add_argument("--test_document", type=str, default="./doc.txt", help="测试文档文件路径")
    parser.add_argument("--test_reading_prompt", type=str, default="简单分析此附件", help="文档阅读测试提示词")
    parser.add_argument("--test_hello_prompt", type=str, default="你好。", help="简单问候测试提示词")
    parser.add_argument("--repeat", type=int, default=5, help="每个测试的重复次数")
    parser.add_argument("--parallel", type=int, default=1, help="并行请求数")
    parser.add_argument("-o", "--output", type=str, default="result.md", help="输出报告文件路径")
    parser.add_argument("--temperature", type=float, default=0.0, help="采样温度")
    parser.add_argument("--vision", action="store_true", help="启用图像理解功能测试")
    parser.add_argument("--max_completion_tokens", type=int, default=512, help="最大输出token数")
    
    args = parser.parse_args()
    
    # 将Namespace对象转换为TestConfig实例
    return TestConfig(
        base_url=args.base_url,
        api_key=args.api_key,
        model=args.model,
        test_image=args.test_image,
        test_document=args.test_document,
        test_reading_prompt=args.test_reading_prompt,
        test_hello_prompt=args.test_hello_prompt,
        repeat=args.repeat,
        parallel=args.parallel,
        output=args.output,
        temperature=args.temperature,
        vision=args.vision,
        max_completion_tokens=args.max_completion_tokens
    )
class TestResult:
    md_header = "|Task|Elapse|Tokens Per Second|Prompt Per Second|Predict Per Second|Prompt|Predict|\n"\
                "|----|-----:|----------------:|----------------:|-----------------:|-----:|------:|"
    def __init__(self, name: str, resp: ChatCompletion, elapse: float = 0, multimodal: bool = False):
        self.name = name
        self.resp = resp
        if (self.resp):
            self.prompt_tokens    = resp.usage.prompt_tokens
            self.predicted_tokens = resp.usage.completion_tokens
            if (hasattr(resp, "timings")):
                self.prompt_per_second    = resp.timings["prompt_per_second"]
                self.predicted_per_second = resp.timings["predicted_per_second"]
                self.elapse = (resp.timings["prompt_ms"] + resp.timings["predicted_ms"])/1000
            else:
                self.elapse = elapse
                self.prompt_per_second    = 0
                self.predicted_per_second = 0
            self.token_per_second = (self.prompt_tokens + self.predicted_tokens) / self.elapse
            self.multimodal = multimodal
    @property
    def md_table_line(self):
        if (self.resp is not None):
            return f"|{self.name}|{self.elapse:.1f}|{self.token_per_second:.1f}|{self.prompt_per_second:.1f}|{self.predicted_per_second:.2f}|{self.prompt_tokens}|{self.predicted_tokens}|"
        else:
            return f"|{self.name}|FAIL|N/A|N/A|N/A|N/A|N/A|"

def test_image(cfg: TestConfig):
    cl = openai.OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)
    if (NO_CACHE):
        rnd_str = secrets.token_hex(16)
        msgs = [{"role": "system", "content": rnd_str+"\nThis an useless message only to disturb prefix cache for testing performance."}]
    else:
        msgs = []
    msgs.extend([
        {"role": "user", "content": [img2openai(Image.open(cfg.test_image)), {"type": "text", "text": cfg.test_reading_prompt}]}
    ])
    t = time.time()
    try:
        resp = cl.chat.completions.create(model=cfg.model, messages=msgs, temperature=config.temperature,
                                          max_tokens=config.max_completion_tokens, max_completion_tokens=config.max_completion_tokens)
    except Exception as e:
        return TestResult("Vision Understanding", None)
    return TestResult("Vision Understanding", resp, time.time()-t, False)
def test_doc(cfg: TestConfig):
    cl = openai.OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)
    if (NO_CACHE):
        rnd_str = secrets.token_hex(16)
        msgs = [{"role": "system", "content": rnd_str+"\nThis an useless message only to disturb prefix cache for testing performance."}]
    else:
        msgs = []
    with open(cfg.test_document, "r", encoding="utf-8") as f:
        doc = f.read()
    msgs.extend([
        {"role": "user", "content":
            f"{cfg.test_document}\n"
            f"```\n"
            f"{doc}\n"
            f"```"},
        {"role": "user", "content": cfg.test_reading_prompt}
    ])
    t = time.time()
    try:
        resp = cl.chat.completions.create(model=cfg.model, messages=msgs, temperature=config.temperature,
                                          max_tokens=config.max_completion_tokens, max_completion_tokens=config.max_completion_tokens)
    except Exception as e:
        return TestResult("Document Understanding", None)
    return TestResult("Document Understanding", resp, time.time()-t, False)




# 使用示例
if __name__ == "__main__":
    config = parse_args()

    with open(config.output, "w", encoding="utf-8") as f:
        cl = openai.OpenAI(api_key=config.api_key, base_url=config.base_url)
        with ThreadPoolExecutor(max_workers=config.parallel) as pool:
            tasks: List[Future[TestResult]] = []
            for i in range(config.repeat):
                tasks.append(pool.submit(test_doc, config))
                if (config.vision):
                    tasks.append(pool.submit(test_image, config))
            print(TestResult.md_header, file=f)
            results = [t.result() for t in tasks]
            results = sorted(results, key=lambda x:(x.name, getattr(x, "predicted_per_second", 0)))
            for r in results:
                print(r.md_table_line, file=f)
        print(file=f)
        print(f"`{config}`", file=f)
        print(file=f)
        models = cl.models.list()
        model = next(iter(models))
        if (hasattr(model, "meta")):
            model_size = model.meta["n_params"] / 1e9
            model_qsize = model.meta["size"] / (1<<30)
            print(f"Model Size / Quant Size: {model_size:.1f} B / {model_qsize:.1f} GB", file=f)
