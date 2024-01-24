# import os

# from flask import Flask
# from dotenv import load_dotenv
# from flask_cors import CORS
# from openai import openai
# from requests import request

# load_dotenv()

# app = Flask(__name__)
# CORS(app)
# openai.api_key = os.getenv("OPENAI_API_KEY")


# @app.get("/")
# def home():
#     return "Hello, World!"


# if __name__ == "__main__":
#     app.run(debug=True)

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/api/home", methods=["POST"])
def return_home():
    data = request.get_json()
    user_input = data.get("word", "")

    messages = [
        {
            "role": "system",
            "content": "you are a helpful assistant who answers every question",
        },
        {"role": "user", "content": user_input},
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=3333,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        response_text = response["choices"][0]["message"]["content"]
        return jsonify({"message": response_text})

    except openai.error.InvalidRequestError as e:
        return jsonify({"message": f"Invalid request to OpenAI: {e}"})

    except Exception as ex:
        return jsonify({"message": f"An error occurred: {ex}"})


if __name__ == "__main__":
    app.run(debug=True)
