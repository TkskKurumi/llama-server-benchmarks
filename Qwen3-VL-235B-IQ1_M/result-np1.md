Model Size / Quant Size: 235.1 B / 64.8 GB

`TestConfig(base_url='http://localhost:8090', api_key='llama', model='llama', test_image='../test.jpg', test_document='/root/llama.cpp/src/llama.cpp', test_reading_prompt='简单分析此附件', test_hello_prompt='你好。', repeat=4, parallel=1, output='./result-np1.md', temperature=0.0, vision=True, max_completion_tokens=128)`
|Task|Elapse|Tokens Per Second|Prompt Per Second|Predict Per Second|Prompt|Predict|
|----|-----:|----------------:|----------------:|-----------------:|-----:|------:|
|Document Understanding|36.6|331.0|395.5|20.33|11977|128|
|Document Understanding|36.4|332.5|397.6|20.34|11980|128|
|Document Understanding|36.4|332.5|397.1|20.46|11979|128|
|Document Understanding|36.4|332.8|397.3|20.51|11979|128|
|Vision Understanding|10.9|207.6|319.1|30.32|2135|128|
|Vision Understanding|10.8|208.9|316.7|31.19|2137|128|
|Vision Understanding|10.9|208.7|315.9|31.21|2138|128|
|Vision Understanding|10.8|208.8|316.6|31.21|2134|128|

Elapsed Time = 194.6 seconds.

server-reported total elapse time = 189.2 seconds.

Parallel ratio = 1.0x
