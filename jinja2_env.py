import re

from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils import formats, timezone
from django.urls import reverse
from django.utils.translation import gettext, ngettext

from dateutil.parser import parse as parse_dt
from jinja2 import Environment, evalcontextfilter, Markup, escape
from names_translator.name_utils import parse_and_generate, generate_all_names

_paragraph_re = re.compile(r"(?:\r\n|\r|\n){2,}")


def updated_querystring(request, params):
    """Updates current querystring with a given dict of params, removing
    existing occurrences of such params. Returns a urlencoded querystring."""
    original_params = request.GET.copy()
    for key in params:
        if key in original_params:
            original_params.pop(key)
    original_params.update(params)
    return original_params.urlencode()


@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u"\n\n".join(
        u"<p>%s</p>" % p.strip().replace("\n", Markup("<br>\n"))
        for p in _paragraph_re.split(escape(value))
    )
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


def identify_relation(rel):
    rel = rel.lower().strip()
    if rel in ["дружина", "чоловік"]:
        return "spouse"

    if rel in [
        "брат",
        "сестра",
        "двоюрідний брат",
        "двоюрідна сестра",
        "рідний брат",
        "рідна сестра",
    ]:
        return "sibling"

    if rel in ["мати", "батько"]:
        return "parent"

    if rel in ["син", "дочка", "донька", "пасинок"]:
        return "children"

    return "knows"


def curformat(value):
    value = str(value)
    if value and value != "0":
        currency = ""
        if "$" in value:
            value = value.replace("$", "")
            currency = "USD "

        if "£" in value:
            value = value.replace("£", "")
            currency = "GBP "

        if "€" in value or "Є" in value:
            value = value.replace("€", "").replace("Є", "")
            currency = "EUR "

        try:
            return (
                "{}{:,.2f}".format(currency, float(value.replace(",", ".")))
                .replace(",", " ")
                .replace(".", ",")
            )
        except ValueError:
            return value
    else:
        return ""

def ensure_aware(dt):
    if timezone.is_aware(dt):
        return dt
    else:
        return timezone.make_aware(dt)


def environment(**options):
    env = Environment(**options)
    env.globals.update({"static": staticfiles_storage.url, "url": reverse})
    env.install_gettext_callables(gettext=gettext, ngettext=ngettext, newstyle=True)

    env.filters.update(
        {
            "datetime": lambda dt: formats.date_format(
                timezone.localtime(
                    ensure_aware(parse_dt(dt) if isinstance(dt, str) else dt)
                ),
                "SHORT_DATETIME_FORMAT",
            ) if dt else "",
            "date": lambda dt: formats.date_format(
                timezone.localtime(
                    ensure_aware(parse_dt(dt) if isinstance(dt, str) else dt)
                ),
                "SHORT_DATE_FORMAT",
            ) if dt else "",
            "nl2br": nl2br,
            "identify_relation": identify_relation,
            "curformat": curformat,
            "format_edrpou": lambda code: str(code).rjust(8, "0"),
        }
    )
    env.globals.update(
        {
            "updated_querystring": updated_querystring,
            "parse_and_generate": parse_and_generate,
            "generate_all_names": generate_all_names,
        }
    )

    return env
