from typing import Optional


class RuleCommand:
    def __init__(self, actuator_id: str, actuator_state: bool, voice_text: str, email_text: Optional[str]) -> None:
        self.actuator_id = actuator_id
        self.actuator_state = actuator_state
        self.voice_text = voice_text
        self.email_text = email_text

    def __repr__(self) -> str:
        return 'RuleCommand: actuator_id({0}), actuator_state({1}), voice_text({2}), email_text({3})'\
                    .format(self.actuator_id, self.actuator_state, self.voice_text, self.email_text)

    def has_actuator(self):
        return None is not self.actuator_id and '' is not self.actuator_id \
            and None is not self.actuator_state and '' is not self.actuator_state

    def has_voice(self):
        return None is not self.voice_text and self.voice_text is not ''

    def has_email(self):
        return None is not self.email_text and self.email_text is not ''