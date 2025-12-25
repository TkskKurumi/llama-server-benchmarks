# simple llama-server benchmark  script

以下结果是在auto-dl平台租用3080-20GB x4的结果。
```plain
NVIDIA-SMI 550.78
Driver Version: 550.78
CUDA Version: 12.4
llama build flags: -DGGML_CUDA=ON
llama-cpp: b7522-849d02110
48 vCPU Intel(R) Xeon(R) Platinum 8352V CPU @ 2.10GHz
sysbench memory --threads=48 --memory-total-size=96G run -> 8670.82 MiB/sec
```

服务端设置上下文长度16k，4slots并行。客户端4 requsts并行请求，prompt前加入随机字符串使前缀缓存失效。读取图片或文档作为输入。offload策略为--fit参数自动产生（对于视觉模型，由于mmproj offload到main-gpu，有不平衡问题，暂且放大了--fit-target浪费其余GPU，有待调优）。

文档选用`ggml-org/llama.cpp/src/llama.cpp`，长度约11k tokens。
图片设置`--image-max-tokens 2048 --image-min-tokens 2048`。
图片任务和文档任务交错，可能在batch内混合。
max_completion_tokens = 128。

prefill和predict混合在一个batch内时，predict per second可能会显得很慢；大部分任务已结束，最后的任务可以独占算力。所以成绩中最慢和最快的结果可能差异巨大。

我个人主要用途为QQ群聊bot。按经验测试11k前文、最大16k、4并行符合我的需求，注重responsivenesss（一分钟内要有结果），所以没有测试更大RAM offload的模型。GLM-4.6跑得太慢了（可能有bug），所以max_completion_tokens设得很小。

## DeepsSeek-V3.1-Terminus - Unsloth Dynamic Quantization TQ1_0

Model Size / Quant Size: 671.0 B / 152.0 GB

Parallel = 1

|Task|Elapse|Tokens Per Second|Prompt Per Second|Predict Per Second|Prompt|Predict|
|----|-----:|----------------:|----------------:|-----------------:|-----:|------:|
|Document Understanding|220.6|58.3|64.5|5.50|12729|128|
|Document Understanding|225.8|57.0|62.8|5.57|12731|128|
|Document Understanding|222.0|57.9|63.7|5.74|12732|128|
|Document Understanding|223.7|57.5|62.6|6.32|12733|128|

Elapsed Time = 893.7 seconds.

[results.md](DeepSeekV3.1-Terminus-TQ1/result.md)

## Qwen3-VL-235B-A22B-Instruct - Unsloth Dynamic Quantization IQ1_M

Parallel = 4

|Task|Elapse|Tokens Per Second|Prompt Per Second|Predict Per Second|Prompt|Predict|
|----|-----:|----------------:|----------------:|-----------------:|-----:|------:|
|Document Understanding|97.4|124.3|368.4|1.97|11982|128|
|Document Understanding|95.9|126.3|374.7|2.00|11980|128|
|Document Understanding|91.6|132.3|306.7|2.44|11981|128|
|Document Understanding|59.2|204.3|365.3|4.84|11978|128|
|Vision Understanding|71.2|31.8|123.3|2.38|2136|128|
|Vision Understanding|64.1|35.3|113.9|2.82|2136|128|
|Vision Understanding|64.1|35.3|114.0|2.82|2138|128|
|Vision Understanding|32.8|69.0|165.1|6.43|2135|128|

Elapsed Time = 194.8 seconds.

[results.md](Qwen3-VL-235B-IQ1_M/result.md)

Parallel = 1

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

[results-np1.md](Qwen3-VL-235B-IQ1_M/result-np1.md)

## Qwen3-Next-80B - Unsloth Dynamic Quantization Q6_K_XL

详见[results.md](Qwen3-Next-80B/result.md)

## GLM-4.6V - Unsloth Dynamic Quantization Q4_K_XL

详见[results.md](GLM-4.6V/result.md)

## GLM-4.6 - Unsloth Dynamic Quantization TQ1_0

详见[results.md](GLM-4.6/result.md)，**内存占用异常大，可能有问题，见[memory.log](GLM-4.6/memory.log)**

## 目录结构
```plain
└── <MODEL_NAME>
    ├── <MODEL_FILE>.gguf
    ├── download.sh           # 下载模型文件
    ├── run_server.bash       # 启动llama-server服务端
    ├── run_bench_server.bash # 运行客户端测试
    ├── fit_param.cmd         # 从run_server.bash中通过llama-fit-param产生的脚本，用于检查offload策略
    ├── result.md             # run_bench_server.bash产生的throughput性能报告
    ├── memory.log            # run_server.bash结束时从server.log中grep出的memory表
    └── server.log            # llama-server产生的日志文件
```

```bash
cd <MODEL_NAME>
source ./run_server.bash
```

```bash
cd <MODEL_NAME>
source ./run_bench_server.bash
```