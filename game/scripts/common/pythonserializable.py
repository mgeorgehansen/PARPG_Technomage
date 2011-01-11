class PythonSerializable(object):
    """
    
    @note: Only works for objects which contain exclusively read-only
        attributes, since any change in state will not be recorded.
    """
    def __init__(self, *args, **kwargs):
        self._init_args = (args, kwargs)
    
    def _get_state(self):
        return self._init_args
