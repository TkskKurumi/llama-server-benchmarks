|Task|Elapse|Tokens Per Second|Prompt Per Second|Predict Per Second|Prompt|Predict|
|----|-----:|----------------:|----------------:|-----------------:|-----:|------:|
|Document Understanding|244.3|48.9|221.6|0.67|11819|128|
|Document Understanding|203.8|58.6|179.6|0.93|11819|128|
|Document Understanding|150.7|79.3|177.6|1.52|11822|128|
|Document Understanding|95.8|124.7|199.9|3.49|11819|128|

`TestConfig(base_url='http://localhost:8090', api_key='llama', model='llama', test_image='../test.jpg', test_document='/root/llama.cpp/src/llama.cpp', test_reading_prompt='简单分析此附件', test_hello_prompt='你好。', repeat=4, parallel=4, output='./result.md', temperature=0.0, vision=False, max_completion_tokens=128)`

Model Size / Quant Size: 356.8 B / 78.3 GB
