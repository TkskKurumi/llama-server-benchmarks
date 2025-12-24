python3 ../bench_server.py \
  --test_image ../test.jpg \
  --test_document /root/llama.cpp/src/llama.cpp \
  --parallel 1 \
  --repeat 4 \
  --max_completion_tokens 128 \
  -o ./result-np1.md \
  --vision