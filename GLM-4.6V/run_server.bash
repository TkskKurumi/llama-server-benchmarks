model_file="/root/autodl-tmp/GLM-4.6V/GLM-4.6V-UD-Q4_K_XL-00001-of-00002.gguf"
mmproj="/root/autodl-tmp/GLM-4.6V/mmproj-BF16.gguf"
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
  --image-min-tokens 2048 \
  --image-max-tokens 2048 \
  --mmproj "$mmproj" \
)

set -x
${bindir}/llama-fit-params \
  --model "$model_file" \
  "${args[@]}" > fit_param.cmd
${bindir}/llama-server \
  --model "$model_file" \
  --fit on \
  --metrics \
  --port 8090 \
  --log-file server.log \
  --chat-template-kwargs "{\"enable_thinking\": false}" \
  -v \
  "${args[@]}"
set +x
tail -n100 server.log | grep -P "^llama_memory_breakdown_print" > memory.log