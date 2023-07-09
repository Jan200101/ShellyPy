
class AttributeList(list):

    def __setattr__(self, name, value):
        for item in self:
            setattr(item, name, value)

    def __getattr__(self, name):
        if not len(self):
            raise Exception("no values")

        ret = []

        wrap_callable = True
        for item in self:
            attr = getattr(item, name)
            if wrap_callable:
                wrap_callable = callable(attr)
            ret.append(attr)

        if wrap_callable:
            callable_list = ret
            def _callable_wrapper(*args, **kwargs):
                ret = []
                for func in callable_list:
                    ret.append(func(*args, **kwargs))

                if len(ret) == 1:
                    return ret[0]
                return ret

            return _callable_wrapper

        if len(ret) == 1:
            return ret[0]
        return ret
