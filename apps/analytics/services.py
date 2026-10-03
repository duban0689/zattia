"""Minimal first-party event logging — no personal information is stored,
only an event type, an optional related product, the (anonymous) session
key, and small bits of metadata (e.g. a search query)."""


def log_event(request, event_type, product=None, metadata=None):
    from .models import Event

    if not request.session.session_key:
        request.session.save()

    return Event.objects.create(
        event_type=event_type,
        product=product,
        session_key=request.session.session_key or "",
        metadata=metadata or {},
    )
