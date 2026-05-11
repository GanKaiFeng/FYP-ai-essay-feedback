from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import re
from db.essay_repo import save_essay, get_essay_by_id, get_essay_by_title
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR
import base64
import io
import anthropic

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
gpt_client = openai.OpenAI(api_key=os.getenv("OPENAI_TEST_API_KEY"))

# Initialise Claude key
claude_client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

app = Flask(__name__)
CORS(app)

@app.route("/api/feedback", methods=["POST"])
def get_feedback():
    data = request.json
    
    # Extract form data from frontend
    title = data.get("title")
    content = data.get("content")
    essay_type = data.get("type")
    rubric = data.get("rubric", "")
    model = data.get("model", "gpt-4")
    detail = data.get("detail", "high")
    
    # Build the prompt with clearer structure for GPT
    prompt = f"""
    You are a teacher marking essays submitted by students.

    The student has submitted an essay with the following details:
    - Title: {title}
    - Type: {essay_type}
    - Rubric: {rubric if rubric else 'Standard university-level rubric'}

    Essay: {content}

    Provide your feedback in the following structure:
    Overall Score: A number and/or letter grade representing the quality of the essay based on the rubric.
    Strengths: A paragraph highlighting the key strengths of the essay based on the rubric.
    Areas for Improvement: A paragraph identifying areas where the essay could be improved, based on the rubric and in relation to the essay.

    Finish your feedback by adding the following line to the end, along with the score, preferring the number if it is available
    Final Score: [number or letter only]

    Make sure the feedback is in-depth, professional, objective, and actionable. Change the language of your feedback based on the language of the essay content provided.
    """

    try:
        if model == "qwen-3":
            print("hi im cuewen", flush=True)
        elif model == "claude-4":
            message = claude_client.messages.create(
                max_tokens = 20000,
                model="claude-sonnet-4-5-20250929",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature = 1
            )
            model = "claude-4.5-sonnet"
            reply = message.content[0].text
        elif model == "gpt-4":
            completion = gpt_client.chat.completions.create(
                model="gpt-5-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature = 1
            )
            model = "gpt-5-mini"
            reply = completion.choices[0].message.content.strip()
        else:
            return

        

        print("\n--- " + model + " RESPONSE START ---\n", flush=True)
        print(reply)
        print("\n--- " + model + " RESPONSE END ---\n", flush=True)
        
        # Split the output
        parts = reply.strip().split("Final Score:")

        # Full output
        print(reply, flush=True)

        # Debug outputs
        strengths = parts[0].replace("Feedback:", "").strip()
        score = parts[1].strip() if len(parts) > 1 else None

        print("Feedback:", strengths, flush=True)
        print("Score:", score, flush=True)

        # --- Save to Supabase ---
        save_result = save_essay(
            user_id="anonymous",
            title=title,    
            essay_text=content,
            score=score,
            strengths=strengths,
            model_used=model,
            type=essay_type,
            rubric=rubric
        )

        # Return as JSON
        return jsonify({
            "title": title,
            "score": score,
            "strengths": strengths,
        })


    
    except Exception as e:
        print("\n BACKEND ERROR:", str(e), flush=True)
        return jsonify({"error": str(e)}), 500

@app.route("/api/essay", methods=["GET"])
def get_essay():
    essay_id = request.args.get("id")
    title = request.args.get("title")
    if essay_id:
        essay = get_essay_by_id(essay_id)
    elif title:
        essay = get_essay_by_title(title)
    else:
        return jsonify({"error": "请提供id或title"}), 400
    if essay:
        return jsonify(essay)
    else:
        return jsonify({"error": "未找到论文"}), 404

# Initialize PaddleOCR once (no need to reinitialize each time)
ocr = PaddleOCR(
    use_doc_orientation_classify=False, 
    use_doc_unwarping=False, 
    use_textline_orientation=False) # text detection + text recognition

import pymupdf

@app.route('/api/ocr', methods=['POST'])
def ocr_endpoint():
    print("== Received OCR request ==", flush=True)
    data = request.get_json()

    if not data or 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    base64_data = data['image']
    print(len(base64_data), flush=True)

    try:
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]

        file_bytes = base64.b64decode(base64_data)

        # Check for PDF magic bytes
        if file_bytes[:4] == b'%PDF':
            print("== PDF detected with PyMuPDF ==", flush=True)
            pdf_doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            all_text = []

            for i, page in enumerate(pdf_doc):
                pix = page.get_pixmap(dpi=100)
                img = Image.open(io.BytesIO(pix.tobytes("png"))).convert('RGB')
                img_np = np.array(img)
                result = ocr.predict(img_np)

                if result and len(result[0]) > 0:
                    rec_texts = result[0]['rec_texts']
                    page_text = '\n'.join(rec_texts)
                    all_text.append(f"--- Page {i+1} ---\n{page_text}")

            extracted_text = '\n\n'.join(all_text)

        else:
            # Handle as regular image
            image = Image.open(io.BytesIO(file_bytes)).convert('RGB')
            w, h = image.size
            largest = max(w, h)

            if largest > 1000:
                scale = 1000 / largest
                image = image.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

            image_np = np.array(image)
            result = ocr.predict(image_np)

            if not result or len(result[0]) == 0:
                return jsonify({'error': 'No text detected'}), 400

            rec_texts = result[0]['rec_texts']
            extracted_text = '\n'.join(rec_texts)

        print("== OCR Complete ==", flush=True)
        return jsonify({'text': extracted_text})

    except Exception as e:
        print("== OCR Error ==", str(e), flush=True)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5051)  