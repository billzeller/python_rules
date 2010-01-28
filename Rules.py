import sys
import types

class Wildcard:
    pass

# This is ugly, but let's callers use _ as a wildcard character...
if type(globals()['__builtins__']) == types.ModuleType:
    vars(globals()['__builtins__'])['_'] = Wildcard()
else:
    globals()['__builtins__']['_'] = Wildcard()


class Rules:
    def __init__(self, *args, **kwargs):
        self.rules = []

        if len(args) % 2 == 1:
            raise Exception('Every rule must have a corresponding action')

        # loop over pairs of rules/actions, adding each one
        i = 0
        while i < len(args):
            self.rules.append((args[i], args[i+1]))
            i += 2
    
    """
        Does the given value match the rule?

        We can't use built-in equality because we treat the value Wildcard in a rule as a wildcard

    """    
    def matches(self, rule, args):
        if isinstance(args, types.TupleType) and len(args) == 1:
            value = args[0]
        else:
            value = args
        
        # An object of type Wildcard matches everything
        if isinstance(rule, Wildcard):
            return True
            
        # if rule is callable, let it evaluate the value
        elif callable(rule):
            if value == args:
                return rule(*value)
            else:
                return rule(value)
            
        # two tuples (or lists) are equal if all their elements are equal
        elif isinstance(rule, types.TupleType) or isinstance(rule, types.ListType):
            if type(rule) == type(value) and len(rule) == len(value):
                for i in xrange(len(rule)):
                    if not self.matches(rule[i], value[i]):
                        return False
                return True
            else:
                return False

        # two dicts are equal if all their elements are equal
        elif isinstance(rule, types.DictType):
            if isinstance(value, types.DictType) and len(rule) == len(value):
                for key in rule:
                    if key not in value or not self.matches(rule[key], value[key]):
                        return False
                return True
            else:
                return False
        else:
            return rule == value
    
    def __call__(self, *args):
        for (rule, val) in self.rules:
            if self.matches(rule, args):
                if callable(val):
                    return val(*args)
                else:
                    return val
                    
