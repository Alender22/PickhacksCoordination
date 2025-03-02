from google import genai
client = genai.Client(api_key="AIzaSyBlOSTfzr2eNn6CnlNnMEheqpdrUyzP_CI")

CHARACTER_COUNT = 0
THRESHOLD = 1500
END_FLAG = False

def main():
    print("Starting conversation with the ghost of Joe Miner....")
    # This feature is direly in the need of further development....

    # giving Gemini context on the setting of the game
    context = """Gemini, for this conversation please pretend to be Joe Miner. You are 
    a ghost who is haunting the University of Missouri Science and Technology campus. You are a friendly ghost who
    wants to answer the players questions on the answeres for the reason the school was abandoned.
    Ironically, the students were summoned away by magic, and the campus itself was teleported to the middle 
    of the magical wilderland. You once were the school mastcot and you are trying to help the player find out what happened to the university."""

    giveGeminiContextInfo(context)

    while not END_FLAG:
        prompt = input("Your input: ")
        getGeminiResponse(context, prompt)

def getGeminiResponse(context, prompt):
    global CHARACTER_COUNT
    global THRESHOLD
    global END_FLAG

    CHARACTER_COUNT += len(prompt)
    if CHARACTER_COUNT > THRESHOLD:
        prompt = f"The context of the setting is[{context}]. The user asked{prompt}. For the story setting, you are now out of time and need to leave after giving the final question a brief answer"

        END_FLAG = True

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    print(response.text) 

def giveGeminiContextInfo(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )

    print(response.text)

if __name__ == "__main__":
    main()