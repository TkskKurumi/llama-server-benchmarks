# simple llama-server benchmark  script

以下结果是在auto-dl平台租用3080-20GB x4的结果。
```plain
NVIDIA-SMI 550.78
Driver Version: 550.78
CUDA Version: 12.4
llama build flags: -DGGML_CUDA=ON
llama-cpp: b7522-849d02110
```

服务端设置上下文长度16k，4slots并行。客户端4 requsts并行请求，prompt前加入随机字符串使前缀缓存失效。读取图片或文档作为输入。offload策略为--fit参数自动产生（对于视觉模型，由于mmproj offload到main-gpu，有不平衡问题，暂且放大了--fit-target浪费其余GPU，有待调优）。

文档选用`ggml-org/llama.cpp/src/llama.cpp`，长度约11k tokens。
图片设置`--image-max-tokens 2048 --image-min-tokens 2048`。
图片任务和文档任务交错，可能在batch内混合。
max_completion_tokens = 128。

由于先开始的任务的predict，可能和后开始的任务的prefill在同一batch执行，导致前序的predict可能较慢；大部分任务已结束，最后的任务可以独占算力。所以成绩中最慢和最快的结果可能差异巨大。

我个人主要用途为QQ群聊bot。按经验测试11k前文、最大16k、4并行符合我的需求，注重responsivenesss（一分钟内要有结果），所以没有测试更大RAM offload的模型。GLM-4.6跑得太慢了（可能有bug），所以max_completion_tokens设得很小。

## Qwen3-VL-235B-A22B-Instruct - Unsloth Dynamic Quantization IQ1_M

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

[results.md](Qwen3-VL-235B-IQ1_M/result.md)


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