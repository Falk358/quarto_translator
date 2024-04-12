import tiktoken
from langchain.schema.document import Document


class TokenCounter:
    """
    class which counts tokens according to openai encodings. Internally tracks and updates token_count
    """

    def __init__(self, model="gpt-3.5-turbo"):
        self.encoding = tiktoken.encoding_for_model(model)
        self.token_counter = 0

    def countTokensInString(self, text):
        num_tokens = len(self.encoding.encode(text))
        self.token_counter += num_tokens
        return num_tokens

    def getCounter(self):
        return self.token_counter

    def resetCounter(self):
        self.token_counter = 0

    # pass the costs per thousand tokens in dollar to this method (take it from here: https://openai.com/pricing) THIS IS ONLY A ROUGH ESTIMATE
    def printCostEstimateTranslation(self, pricing_input, pricing_output):
        if self.token_counter == 0:
            print("Error! token counter is at 0; Aborting")
            return

        token_count_in_1k = self.token_counter / 1000

        # since we should get roughly the same output length as input (due to translation), we just weigh them with their pricing scheme; this is leaving out system messages so actual price will be slightly higher depending on number of requests
        final_price = (
            token_count_in_1k * pricing_input + token_count_in_1k * pricing_output
        )
        print(f"This should cost {final_price}$")
