import inspect

from gocd_cli.utils import dasherize_name
from gocd_cli.exceptions import MissingDocumentationError


class BaseCommand(object):
    @classmethod
    def _get_or_raise(cls, attr, exception, message=None):
        value = getattr(cls, attr, None)
        if not value:
            if not message:
                message = 'Command "{0}" has no "{1}" string set.'.format(cls.__name__, attr)

            raise exception(message)

        return value

    @classmethod
    def get_usage(cls):
        usage = cls._get_or_raise('usage', MissingDocumentationError)

        return '{call_documentation}\n\n{usage_summary}\n\n{usage}\n'.format(
            call_documentation=cls.get_call_documentation(),
            usage_summary=cls.get_usage_summary(),
            usage=inspect.cleandoc(usage),
        )

    @classmethod
    def get_usage_summary(cls):
        return cls._get_or_raise('usage_summary', MissingDocumentationError)

    @classmethod
    def get_call_documentation(cls):
        def get_arg_names():
            sig = inspect.signature(cls.__init__)
            params = sig.parameters.values()

            args = [
                p.name for p in params
                if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
                   and p.name != 'self'
            ]
            defaults = [
                p.default for p in params
                if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
                   and p.default is not p.empty
            ]
            varargs = next((p.name for p in params if p.kind == p.VAR_POSITIONAL), None)
            keywords = next((p.name for p in params if p.kind == p.VAR_KEYWORD), None)

            return args, varargs, keywords, defaults or None

        args, varargs, keywords, defaults = get_arg_names()

        # Build usage string
        parts = [dasherize_name(cls.__name__)]

        # Required args: <name>
        parts.extend(f'<{arg}>' for arg in args)

        # *args: *varargs
        if varargs:
            parts.append(f'*{varargs}')

        # **kwargs: [--kwarg ...]
        if keywords:
            parts.append('[--...]')  # Simplified; could list if needed

        return ' '.join(parts).strip()

    def _return_value(self, output, exit_code):
        if isinstance(exit_code, bool):
            exit_code = 0 if exit_code else 2

        return dict(
            exit_code=exit_code,
            output=output,
        )
