|Task|Elapse|Tokens Per Second|Prompt Per Second|Predict Per Second|Prompt|Predict|
|----|-----:|----------------:|----------------:|-----------------:|-----:|------:|
|Document Understanding|96.4|125.6|370.4|2.00|11980|128|
|Document Understanding|89.7|134.9|312.1|2.49|11980|128|
|Document Understanding|97.3|124.4|255.5|2.54|11982|128|
|Document Understanding|71.8|168.7|304.0|3.95|11978|128|
|Vision Understanding|92.2|24.6|89.8|1.87|2136|128|
|Vision Understanding|92.2|24.6|90.0|1.87|2140|128|
|Vision Understanding|38.4|59.0|113.3|6.54|2137|128|
|Vision Understanding|38.4|58.9|113.3|6.54|2136|128|

`TestConfig(base_url='http://localhost:8090', api_key='llama', model='llama', test_image='../test.jpg', test_document='/root/llama.cpp/src/llama.cpp', test_reading_prompt='简单分析此附件', test_hello_prompt='你好。', repeat=4, parallel=4, output='./result.md', temperature=0.0, vision=True, max_completion_tokens=128)`

Model Size / Quant Size: 235.1 B / 64.8 GB
