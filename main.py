from flask import Flask, request, jsonify,render_template,send_from_directory,make_response,redirect
import os
from werkzeug.utils import secure_filename
import whisper
import uuid
import logging
import subprocess
import time
from openai import OpenAI
import re
import requests
from flask_cors import CORS


app = Flask(__name__, template_folder='/var/www/html')
app.config['UPLOAD_FOLDER'] = './uploads'
CORS(app)  # 允许跨域请求
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

logging.basicConfig(level=logging.INFO)

# Qwen 模型的本地API设置
client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="not-needed")

SYSTEM_PROMPT = "你是跨模态诗词专用模型,你的回复是准确、精简高效的"
# 初始化对话历史
history = [{
    "role": "system",
    "content": SYSTEM_PROMPT
}]

@app.route('/favicon')
def favicon():
    return send_from_directory(app.template_folder,'favicon.ico')

@app.route('/background')
def background():
    return send_from_directory(app.template_folder,'background.jpg')

@app.route('/index')
def index1():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/voice_poem')
def voice_poem():
    return render_template('voice_poem.html')

@app.route('/image_poem')
def image_poem():
    return render_template('image_poem.html')

@app.route('/result_poem')
def show_result():
    return render_template('result_poem.html')


def process_string(input_string, s_num=5):
    segments = re.split(r'[，。？！、；：\s.,\\]', input_string)
    segments = [seg for seg in segments if seg]

    result = []
    for i in range(len(segments) - 3):
        if all(len(segments[j]) == s_num for j in range(i, i + 4)):
            result.append(segments[i:i + 4])

    if result:
        poem = ""
        for block in result[-1]:
            poem += "<br>"
            poem += block
        poem += "\n"
        return poem
    else:
        return "<br>请重试"


def qwen_completion(query, poem_format=5):
    payload = {
        "model": "qwen-7b-chat",
        "messages": [{"role": "user", "content": query}]
    }
    try:
        response = requests.post(str(client.base_url) + 'chat/completions', json=payload)
        response.raise_for_status()  # 检查HTTP错误状态
        response_data = response.json()
        if 'choices' in response_data and response_data['choices']:
            content = response_data['choices'][0]['message']['content']
            print(content)
            return process_string(content, poem_format)
        else:
            return "<br>API响应中缺少生成内容，请稍后重试"
    except requests.exceptions.RequestException as e:
        logging.error(f"API 请求失败: {e}")
        return "<br>无法连接生成模型，请稍后重试"
    except (KeyError, ValueError) as e:
        logging.error(f"响应解析失败: {e}")
        return "<br>生成失败，请稍后重试"

@app.route('/contact', methods=['POST'])
def contact():
    # 处理文件上传
    if 'audio' in request.files:
        file = request.files['audio']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                subprocess.run(['python', './whisper-main/demo.py', file_path, 'output_temp.txt'], check=True, capture_output=True, text=True)
                subprocess.run(['python', './translate_chinese_to_english.py', 'output_temp.txt', 'output_temp.txt'])
                subprocess.run(['python', './split_text.py'], check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                logging.error(f"Error during audio processing: {e}")
                return jsonify(error="音频处理失败，请稍后重试"), 500

    elif 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            img_filename = 'image_test.png'  # 设置固定的文件名
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
            image.save(img_path)
            try:
                os.chdir('./BLIP-main')
                subprocess.run(['python', 'demo.py', img_path, './output_temp.txt'], check=True, capture_output=True, text=True)
                os.chdir('..')
                subprocess.run(['python', './translate_chinese_to_english.py', 'output_temp.txt', 'output_temp.txt'])
                subprocess.run(['python', './split_text.py'], check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                logging.error(f"Error during image processing: {e}")
                return jsonify(error="图片处理失败，请稍后重试"), 500

     # 处理文本内容
    input_text = request.form.get('text', '')
    poem_format = int(request.form.get('format', 7))  # 获取格式
    poem_style = request.form.get('style', '当代白话风格')  # 获取风格

    logging.info(f"Received input_text: {input_text}, poem_format: {poem_format}, poem_style: {poem_style}")
    try:
        result = generate_poem(input_text, poem_format, poem_style)
        logging.info(f"Generated poem: {result}")
        # 清空 output_temp.txt 文件内容
        with open('output_key.txt', 'w', encoding='utf-8') as file:
            file.truncate(0)  # 清空文件内容
        return jsonify(result=result)
    except Exception as e:
        logging.error(f"Error in result_poem: {e}")
        return jsonify(error="处理请求时发生错误，请稍后重试"), 500


def generate_poem(input_text, poem_format, poem_style="当代白话风格"):
    p_num = "五" if poem_format == 5 else "七"
    try:
        with open('output_key.txt', 'r', encoding='utf-8') as f:
            keywords = f.read().strip().replace('\n', '、')
    except FileNotFoundError:
        logging.warning("output_temp.txt 文件未找到，使用默认关键词")
        keywords = "无"

    prompt = (f"请用中华新韵、{poem_style}，以{input_text}为主题，"
              f"严格按照{p_num}绝（新韵）平起首句不入韵的格律生成诗词。"
              f"生成诗词实验关键词：{keywords}")
    print(prompt)
    poem = qwen_completion(prompt, poem_format)
    return poem
     
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/Company.html')
def Company():
    return render_template('Company.html')

@app.route('/Contact.html')
def Contact():
    return render_template('Contact.html')

@app.route('/Comment.html')
def Comment():
    return render_template('Comment.html')


@app.route('/Right.html')
def Right_html():
    return render_template('Right.html')

@app.route('/Right1.html')
def Right1_html():
    return render_template('Right1.html')

@app.route('/Right2.html')
def Right2_html():
    return render_template('Right2.html')

@app.route('/Right3.html')
def Right3_html():
    return render_template('Right3.html')

@app.route('/product.html')
def product():
    return render_template('product.html')

@app.route('/Product1.html')
def Product1():
    return render_template('Product1.html')

@app.route('/Product2.html')
def Product2():
    return render_template('Product2.html')

@app.route('/css/bootstrap.min.css')
def bootstrap_min_css():
    return send_from_directory(app.template_folder,'css/bootstrap.min.css')

@app.route('/css/bootstrap.min.css.map')
def bootstrap_min_css_map():
    return send_from_directory(app.template_folder,'css/bootstrap.min.css.map')

@app.route('/css/Animation.css')
def Animation_css():
    return send_from_directory(app.template_folder,'css/Animation.css')

@app.route('/css/css.css')
def css_css():
    return send_from_directory(app.template_folder,'css/css.css')

@app.route('/js/jquery-1.9.1.min.js')
def jquery():
    return send_from_directory(app.template_folder,'js/jquery-1.9.1.min.js')

@app.route('/js/jquery-1.8.3.min.js')
def jquery_1_8_3():
    return send_from_directory(app.template_folder,'js/jquery-1.8.3.min.js')

@app.route('/js/jquery.mobile.custom.min.js')
def jquery_mobile_custom_min_js():
    return send_from_directory(app.template_folder,'js/jquery.mobile.custom.min.js')

@app.route('/css/slider.css')
def slider_css():
    return send_from_directory(app.template_folder,'css/slider.css')

@app.route('/js/common.js')
def js_common():
    return send_from_directory(app.template_folder,'js/common.js')

@app.route('/js/slider.js')
def slider_js():
    return send_from_directory(app.template_folder,'js/slider.js')

@app.route('/js/html5.js')
def html5_js():
    return send_from_directory(app.template_folder,'js/html5.js')

@app.route('/js/jquery.js')
def jquery_js():
    return send_from_directory(app.template_folder,'js/jquery.js')

@app.route('/js/jquery.SuperSlide.2.1.1.js')
def jquery_SuperSlide_js():
    return send_from_directory(app.template_folder,'js/jquery.SuperSlide.2.1.1.js')

@app.route('/js/bootstrap.min.js')
def bootstrap_min_js():
    return send_from_directory(app.template_folder,'js/bootstrap.min.js')

@app.route('/js/wow.min.js')
def wow_min_js():
    return send_from_directory(app.template_folder,'js/wow.min.js')

@app.route('/images/banner_18.png')
def banner_18():
    return send_from_directory(app.template_folder,'images/banner_18.png')

@app.route('/images/logo.png')
def logo_png():
    return send_from_directory(app.template_folder,'images/logo.png')

@app.route('/images/banner_15.png')
def banner_15():
    return send_from_directory(app.template_folder,'images/banner_15.png')

@app.route('/images/resultbg.jpg')
def result_bg():
    return send_from_directory(app.template_folder,'images/resultbg.jpg')

@app.route('/images/logo2.png')
def logo2():
    return send_from_directory(app.template_folder,'images/logo2.png')

@app.route('/images/logo1.png')
def logo1():
    return send_from_directory(app.template_folder,'images/logo1.png')

@app.route('/images/banner_03.png')
def banner_03():
    return send_from_directory(app.template_folder,'images/banner_03.png')

@app.route('/images/icon_phone.png')
def icon_phone():
    return send_from_directory(app.template_folder,'images/icon_phone.png')

@app.route('/images/weixing-ma.jpg')
def weixing_ma_pg():
    return send_from_directory(app.template_folder,'images/weixing-ma.jpg')

@app.route('/images/footer_logo.png')
def footer_logo():
    return send_from_directory(app.template_folder,'images/footer_logo.png')

@app.route('/images/bg_01.jpg')
def bg_01():
    return send_from_directory(app.template_folder,'images/bg_01.jpg')

@app.route('/images/p_bg_02.jpg')
def p_bg_02():
    return send_from_directory(app.template_folder,'images/p_bg_02.jpg')

@app.route('/images/abt_23.png')
def abt_23():
    return send_from_directory(app.template_folder,'images/abt_23.png')

@app.route('/images/abt_26.png')
def abt_26():
    return send_from_directory(app.template_folder,'images/abt_26.png')

@app.route('/images/overlay.png')
def overlay():
    return send_from_directory(app.template_folder,'images/overlay.png')

@app.route('/images/line_one.png')
def line_one():
    return send_from_directory(app.template_folder,'images/line_one.png')

@app.route('/images/line_three.png')
def line_three():
    return send_from_directory(app.template_folder,'images/line_three.png')

@app.route('/images/line_two.png')
def line_two():
    return send_from_directory(app.template_folder,'images/line_two.png')

@app.route('/images/icon_xiangxi_03.png')
def icon_xiangxi_03():
    return send_from_directory(app.template_folder,'images/icon_xiangxi_03.png')

@app.route('/images/detailed_btns.png')
def detailed_btns():
    return send_from_directory(app.template_folder,'images/detailed_btns.png')

@app.route('/images/footer_02.png')
def footer_02():
    return send_from_directory(app.template_folder,'images/footer_02.png')

@app.route('/images/footer_bg_02.png')
def footer_bg_02():
    return send_from_directory(app.template_folder,'images/footer_bg_02.png')

@app.route('/fonts/icomoon.ttf')
def fonts_icomoon_ttf():
    return send_from_directory(app.template_folder,'fonts/icomoon.ttf')

@app.route('/fonts/icomoon.woff')
def fonts_icomoon_woff():
    return send_from_directory(app.template_folder,'fonts/icomoon.woff')

@app.route('/images/detailed_btn.png')
def detailed_btn():
    return send_from_directory(app.template_folder,'images/detailed_btn.png')

@app.route('/images/right_r22.png')
def right_r22():
    return send_from_directory(app.template_folder,'images/right_r22.png')

@app.route('/images/right_r21.png')
def right_r21():
    return send_from_directory(app.template_folder,'images/right_r21.png')

@app.route('/images/software_r1.png')
def software_r1():
    return send_from_directory(app.template_folder,'images/software_r1.png')

@app.route('/images/software_r2.png')
def software_r2():
    return send_from_directory(app.template_folder,'images/software_r2.png')

@app.route('/fonts/FontAwesome/font-awesome.css')
def FontAwesome():
    return send_from_directory(app.template_folder,'fonts/FontAwesome/font-awesome.css')

@app.route('/css/product.css')
def product_css():
    return send_from_directory(app.template_folder,'css/product.css')

@app.route('/presentimg/present_img_03.png')
def present_img_03():
    return send_from_directory(app.template_folder,'presentimg/present_img_03.png')

@app.route('/presentimg/present_img_06.png')
def present_img_06():
    return send_from_directory(app.template_folder,'presentimg/present_img_06.png')

@app.route('/images/logo4.png')
def logo4():
    return send_from_directory(app.template_folder,'images/logo4.png')

@app.route('/presentimg/jf-p_15.png')
def jf_p_15():
    return send_from_directory(app.template_folder,'presentimg/jf-p_15.png')

@app.route('/presentimg/jf-p_21.png')
def jf_p_21():
    return send_from_directory(app.template_folder,'presentimg/jf-p_21.png')

@app.route('/js/jquery.zoombie.js')
def jquery_zoombie():
    return send_from_directory(app.template_folder,'js/jquery.zoombie.js')

@app.route('/presentimg/bg.jpg')
def presentimg_bg_jpg():
    return send_from_directory(app.template_folder,'presentimg/bg.jpg')

@app.route('/images/container_03.png')
def images_container_03_png():
    return send_from_directory(app.template_folder,'images/container_03.png')

@app.route('/images/h19.png')
def h19():
    return send_from_directory(app.template_folder,'images/h19.png')

@app.route('/images/h14.png')
def h14():
    return send_from_directory(app.template_folder,'images/h14.png')

@app.route('/images/h25.png')
def h25():
    return send_from_directory(app.template_folder,'images/h25.png')

@app.route('/images/h15.jpg')
def h15():
    return send_from_directory(app.template_folder,'images/h15.jpg')

@app.route('/js/main.js')
def js_main_js():
    return send_from_directory(app.template_folder,'js/main.js')


if __name__ == '__main__':
    app.run(debug=True)
