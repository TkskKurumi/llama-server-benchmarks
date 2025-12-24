|Task|Elapse|Tokens Per Second|Prompt Per Second|Predict Per Second|Prompt|Predict|
|----|-----:|----------------:|----------------:|-----------------:|-----:|------:|
|Document Understanding|38.8|307.9|1027.9|4.68|11827|128|
|Document Understanding|38.6|309.7|700.2|5.89|11827|128|
|Document Understanding|45.9|260.3|427.8|7.00|11826|128|
|Document Understanding|30.8|387.6|768.8|8.28|11827|128|
|Vision Understanding|38.3|58.9|303.1|4.09|2129|128|
|Vision Understanding|38.3|58.9|302.8|4.09|2127|128|
|Vision Understanding|17.6|128.4|360.0|10.96|2128|128|
|Vision Understanding|17.6|128.4|360.2|10.96|2128|128|

`TestConfig(base_url='http://localhost:8090', api_key='llama', model='llama', test_image='../test.jpg', test_document='/root/llama.cpp/src/llama.cpp', test_reading_prompt='简单分析此附件', test_hello_prompt='你好。', repeat=4, parallel=4, output='./result.md', temperature=0.0, vision=True, max_completion_tokens=128)`

Model Size / Quant Size: 106.9 B / 60.9 GB
