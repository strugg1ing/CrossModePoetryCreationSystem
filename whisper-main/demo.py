import sys
import whisper

def transcribe_file(file_path, output_path):
    # 加载模型，这里已经是base模型
    model = whisper.load_model("base")
    
    # 使用模型转录指定的文件
    result = model.transcribe(file_path)
    
    # 将转录的文本写入到指定的输出文件
    with open(output_path, 'w') as f:
        f.write(result["text"])

    # 也可以选择打印到控制台
    print(result["text"])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_audio_file> <path_to_output_file>")
        sys.exit(1)
    
    # 第一个命令行参数是脚本名称
    # 第二个是音频文件路径
    audio_file_path = sys.argv[1]
    
    # 第三个是输出文件路径
    output_file_path = sys.argv[2]
    
    # 转录文件并将结果写入到输出文件
    transcribe_file(audio_file_path, output_file_path)