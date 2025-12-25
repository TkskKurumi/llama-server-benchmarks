Model Size / Quant Size: 671.0 B / 152.0 GB

`TestConfig(base_url='http://localhost:8090', api_key='llama', model='llama', test_image='../test.jpg', test_document='/root/llama.cpp/src/llama.cpp', test_reading_prompt='简单分析此附件', test_hello_prompt='你好。', repeat=4, parallel=1, output='./result-np=1.md', temperature=0.0, vision=False, max_completion_tokens=128)`
|Task|Elapse|Tokens Per Second|Prompt Per Second|Predict Per Second|Prompt|Predict|
|----|-----:|----------------:|----------------:|-----------------:|-----:|------:|
|Document Understanding|220.6|58.3|64.5|5.50|12729|128|
|Document Understanding|225.8|57.0|62.8|5.57|12731|128|
|Document Understanding|222.0|57.9|63.7|5.74|12732|128|
|Document Understanding|223.7|57.5|62.6|6.32|12733|128|

Elapsed Time = 893.7 seconds.

server-reported total elapse time = 892.1 seconds.

Parallel ratio = 1.0x
