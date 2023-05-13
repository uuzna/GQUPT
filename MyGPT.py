import openai


class GPT3:
    def __init__(self):
        with open("APIkeys.txt", "r") as file:
            self.api_key = file.readline().strip()

    # 传入一段话,返回结果
    def gpt3(self, sentence):
        prompt = sentence
        # model_engine = 'gpt-3.5-turbo'
        model_engine = 'gpt-4-0314'
        openai.api_key = self.api_key

        response = openai.ChatCompletion.create(
            model = model_engine,
            max_tokens=4000,
            n=1,  # 结果数量
            stop=None,
            temperature=0.5,
            messages = [
            {'role' : 'user', 'content' : prompt},
            ]
        )

        message = response['choices'][0]['message']['content']
        return message

    # input()获取输入,while true循环调用gpt3()
    def auto_chat_gpt3(self):
        while True:
            sentence = input('你想要问些什么:')
            message = self.gpt3(sentence)
            print(message)


if __name__ == "__main__":
    sentence = '666'
    GPT3 = GPT3()
    GPT3.auto_chat_gpt3()
    message = GPT3.gpt3(sentence)
    print(message)
