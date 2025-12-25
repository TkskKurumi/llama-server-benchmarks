model_file="/root/autodl-tmp/DeepSeekV3.1-Terminus-TQ1/DeepSeek-V3.1-Terminus-UD-TQ1_0.gguf"
bindir="/root/llama.cpp/build/bin"
args=(
  -ctk q4_0
  -ctv q4_0
  -c 16384
  -np 1
  -b 2048
  -fa on
  -ub 1024
  -fitt 2560
)

${bindir}/llama-fit-params \
  --model "$model_file" \
  "${args[@]}" > fit_param-np=1.bash
# set -x
${bindir}/llama-server \
  --model "$model_file" \
  --fit on \
  --metrics \
  --port 8090 \
  --log-file server.log \
  -cram 8192 \
  -v \
  "${args[@]}"
# set +x
tail -n100 server.log | grep -P "^llama_memory_breakdown_print" > memory-np=1.log
