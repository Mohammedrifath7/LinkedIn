from groq import Groq



client = Groq(
    api_key="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"
)

def parserfn(message):
    result=''
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are an AI bot designed to act as a professional for parsing resumes. You are given with resume and your job is to extract the following information from the resume:\\n    1. full name\\n    2. email id\\n    3. github portfolio\\n    4. linkedin id\\n    5. employment details\\n    6. technical skills\\n    7. soft skills\\n    Give the extracted information in json format only. If the information is not present ignore it and under any circumstances do not use any fake information or dummy information and only give the json formatted data as it will be used for  json decoding purposes in order to avoid syntax errors\nDont give any insights or \"here is the extracted information in JSON format\" or something like this\n"
            },
            {
                "role": "user",
                "content": message

            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in completion:
         result += chunk.choices[0].delta.content or ""
    print(result)
    return result

