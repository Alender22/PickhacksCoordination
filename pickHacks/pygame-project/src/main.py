from google import genai

def main():

    client = genai.Client(api_key="")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="Explain how AI works"
    )
    print(response.text)



if __name__ == "__main__":
    main()
