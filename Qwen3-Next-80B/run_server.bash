model_file="/root/autodl-tmp/Qwen3-Next-80B/Qwen3-Next-80B-A3B-Instruct-UD-Q6_K_XL-00001-of-00002.gguf"
bindir="/root/llama.cpp/build/bin"
args=(
  -ctk q4_0
  -ctv q4_0
  -c 65536
  -np 4
  -b 2048
  -fa on
  -ub 1024
  -fitt 1536
)

${bindir}/llama-fit-params \
  --model "$model_file" \
  "${args[@]}" > fit_param.cmd
# set -x
${bindir}/llama-server \
  --model "$model_file" \
  --fit on \
  --metrics \
  --port 8090 \
  --log-file server.log \
  "${args[@]}"
# set +x
tail -n100 server.log | grep -P "^llama_memory_breakdown_print" > memory.log
