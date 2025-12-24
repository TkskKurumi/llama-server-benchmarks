|Task|Elapse|Tokens Per Second|Prompt Per Second|Predict Per Second|Prompt|Predict|
|----|-----:|----------------:|----------------:|-----------------:|-----:|------:|
|Document Understanding|44.4|272.9|1051.9|3.88|11981|128|
|Document Understanding|36.7|329.7|873.8|5.56|11979|128|
|Document Understanding|46.5|260.2|376.6|8.70|11980|128|
|Document Understanding|18.3|663.0|1070.3|18.11|11978|128|

`TestConfig(base_url='http://localhost:8090', api_key='llama', model='llama', test_image='../test.jpg', test_document='/root/llama.cpp/src/llama.cpp', test_reading_prompt='简单分析此附件', test_hello_prompt='你好。', repeat=4, parallel=4, output='./result.md', temperature=0.0, vision=False, max_completion_tokens=128)`

Model Size / Quant Size: 79.7 B / 61.2 GB
