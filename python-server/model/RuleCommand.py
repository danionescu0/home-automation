class RuleCommand:
    def __init__(self, actuator_id: str, actuator_state: bool, voice_text: str) -> None:
        self.actuator_id = actuator_id
        self.actuator_state = actuator_state
        self.voice_text = voice_text

    def __repr__(self) -> str:
        return 'RuleCommand: actuator_id({0}), actuator_state({1}), voice_text({2})'\
                    .format(self.actuator_id, self.actuator_state, self.voice_text)