class RuleCommand:
    def __init__(self, actuator_name: str, actuator_state: bool, voice_text: str) -> None:
        self.actuator_name = actuator_name
        self.actuator_state = actuator_state
        self.voice_text = voice_text

    def __repr__(self) -> str:
        return 'RuleCommand: actuator_name({0}), actuator_state({1}), voice_text({2})'\
                    .format(self.actuator_name, self.actuator_state, self.voice_text)