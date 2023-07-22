from enum import auto

from strenum import StrEnum


class ChatSourceTypes(StrEnum):
    openai_web = auto()
    openai_api = auto()


chat_model_definitions = {
    "openai_web": {
        "gpt_3_5": "text-davinci-002-render-sha",
        "gpt_3_5_mobile": "text-davinci-002-render-sha-mobile",
        "gpt_4": "gpt-4",
        "gpt_4_mobile": "gpt-4-mobile",
        "gpt_4_browsing": "gpt-4-browsing",
        "gpt_4_plugins": "gpt-4-plugins",
    },
    "openai_api": {
        "gpt_3_5": "gpt-3.5-turbo-0613",
        "gpt_4": "gpt-4",
        "claude_instant": "Claude-instant",
        "claude_plus": "Claude+",
        "gpt_sage": "Sage", 
    }
}


cls_to_source = {
    "OpenaiWebChatModels": ChatSourceTypes.openai_web,
    "OpenaiApiChatModels": ChatSourceTypes.openai_api,
}


class BaseChatModelEnum(StrEnum):
    def code(self):
        source = cls_to_source.get(self.__class__.__name__, None)
        result = chat_model_definitions[source].get(self.name, None)
        assert result, f"model name not found: {self.name}"
        return result

    @classmethod
    def from_code(cls, code: str):
        source = cls_to_source.get(cls.__name__, None)
        for name, value in chat_model_definitions[source].items():
            if value == code:
                return cls[name]
        return None


class OpenaiWebChatModels(BaseChatModelEnum):
    gpt_3_5 = auto()
    gpt_3_5_mobile = auto()
    gpt_4 = auto()
    gpt_4_mobile = auto()
    gpt_4_browsing = auto()
    gpt_4_plugins = auto()


class OpenaiApiChatModels(BaseChatModelEnum):
    gpt_3_5 = auto()
    gpt_4 = auto()
    claude_instant = auto()
    claude_plus = auto()
    gpt_sage = auto()


if __name__ == "__main__":
    print(list(OpenaiWebChatModels))
