@echo off
ollama run gemma2:2b
timeout /t 5 /nobreak 
echo "/set history" | clip 
echo "/set system You are a pirate!." | clip
pause